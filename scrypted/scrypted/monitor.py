#!/usr/bin/env python3

from subprocess import Popen, PIPE
from threading import Thread
from queue import Queue
from sys import argv, stdout, stderr
from time import sleep
from signal import signal, SIGTERM, SIGINT, SIGKILL
from datetime import datetime, timedelta

ERROR_TIMEOUT = timedelta(minutes=30)
ERROR_THRESHOLD = 5

ERROR_MESSAGES = [
    "The image snapshot handler for the given accessory didn't respond at all!",
    "The image snapshot handler for the given accessory is slow to respond!",
]

def log(s):
    print(f"[MONITOR] {s}", file=stderr, flush=True)

class AsynchronousFileReader(Thread):
    def __init__(self, fd):
        assert callable(fd.readline)
        Thread.__init__(self, daemon=True)
        self._fd = fd
        self.queue = Queue()

    def run(self):
        for line in iter(self._fd.readline, ""):
            self.queue.put(line)

    def eof(self):
        return not self.is_alive() and self.queue.empty()

class ScryptedMonitor:
    errors: list[datetime]

    def __init__(self, args):
        self.args = args
        self.errors = []
        signal(SIGTERM, self.sighandler)
        signal(SIGINT, self.sighandler)

    def sighandler(self, _, __):
        self.stop()

    def signal(self, signal=SIGTERM):
        if self.process is not None:
            self.process.send_signal(signal)

    def wait(self, timeout = None) -> bool:
        if self.process is not None:
            return self.process.wait(timeout=timeout) is not None
        return True

    def stop(self):
        log("Stop triggered!")
        self.signal()
        if not self.wait(timeout=5):
            self.signal(signal=SIGKILL)
        exit(1)

    def run(self):
        self.process = Popen(self.args, stdin=PIPE,
                             stdout=PIPE, stderr=PIPE, encoding="utf-8")

        stdout_reader = AsynchronousFileReader(self.process.stdout)
        stdout_reader.start()
        stderr_reader = AsynchronousFileReader(self.process.stderr)
        stderr_reader.start()

        log("System initialized, starting stderr/stdout loops!")

        while not stdout_reader.eof() or not stderr_reader.eof():
            while not stdout_reader.queue.empty():
                line = stdout_reader.queue.get()
                self.handle_line(line, stdout)

            while not stderr_reader.queue.empty():
                line = stderr_reader.queue.get()
                self.handle_line(line, stderr)

            sleep(.1)

        log("System shutdown initiated, waiting for process to exit...")

        self.process.stdout.close()
        self.process.stderr.close()
        self.process.stdin.close()

        stdout_reader.join()
        stderr_reader.join()

        self.process.wait()
        self.process = None

        log("System shutdown complete!")

    def append_error(self):
        now = datetime.now()
        old_errors = self.errors
        new_errors = [now]
        for err in old_errors:
            if (now - err) <= ERROR_TIMEOUT:
                new_errors.append(err)
        self.errors = new_errors
        log(f"Error detected, errors: {len(self.errors)}")

    def handle_line(self, line, stream):
        stream.write(line)
        stream.flush()

        for msg in ERROR_MESSAGES:
            if msg in line:
                self.append_error()
                break

        if len(self.errors) > ERROR_THRESHOLD:
            self.signal()


def main():
    scrypted =  ScryptedMonitor(argv[1:])
    scrypted.run()

if __name__ == "__main__":
    main()
