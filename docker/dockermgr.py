from subprocess import check_output, check_call, run

class Container():
    def __init__(self, id):
        self.id = id

    def check(self):
        check_call(["docker", "exec", "-i", self.id,
                   "ls", "/sys/class/net/eth0"])
        return True

    def restart(self):
        print(f"Restarting {self.id}")
        run(["docker", "restart", self.id]) # If this fails, not much we can do...

    def restart_if_failed(self):
        try:
            if self.check():
                return  # Will throw or return false on error, so this exits the func on success
        except Exception as e:
            print(f"Error on check {self.id}: {e}")
        
        self.restart()

def list_containers():
    ids = check_output(["docker", "ps", "--format", "{{.ID}}"], encoding="utf8").strip().split("\n")
    return [Container(id.strip()) for id in ids]

def restart_failed_containers():
    for ct in list_containers():
        ct.restart_if_failed()

def prune_images():
    run(["docker", "image", "prune", "-f", "-a"])
