from subprocess import check_output, check_call, run

class Container():
    def __init__(self, id):
        self.id = id

    def check(self):
        check_call(["docker", "exec", "-i", self.name,
                   "ls", "/sys/class/net/eth0"])
        return True

    def restart(self):
        print(f"Restarting {self.name}")
        run(["docker", "restart", self.name]) # If this fails, not much we can do...

    def restart_if_failed(self):
        try:
            if self.check_container():
                return  # Will throw or return false on error, so this exits the func on success
        except Exception as e:
            print(f"Error on check {self.name}: {e}")
        
        self.restart()

def list_containers():
    ids = check_output(["docker", "ps", "--format", "{{.ID}}"])
    return [Container(id) for id in ids]

def restart_failed_containers():
    for ct in list_containers():
        ct.restart_if_failed()

def prune_images():
    run(["docker", "image", "prune", "-f", "-a"])
