#!/usr/bin/env python3

from subprocess import CalledProcessError, check_call, check_output

def test_nvidia_ct(id: str):
    try:
        res = check_output(["docker", "exec", id, "nvidia-smi", "-L"]).decode("utf8")
        return "GPU 0" in res 
    except CalledProcessError:
        return False

def check_ct(id: str):
    id = id.strip()
    if len(id) < 1:
        return
    if not test_nvidia_ct(id):
        check_call(["docker", "restart", id])

for ct in check_output(["docker", "ps", "-f", "label=net.doridian.nvidia-check", "-f", "status=running", "--format", "{{.ID}}"]).decode("utf8").strip().split("\n"):
    check_ct(ct)
