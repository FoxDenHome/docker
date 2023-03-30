#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include <sys/stat.h>

#define TRUE 1
#define FALSE 0

static int check_nvidia()
{
    int pid = fork();
    if(pid == 0) {
        execlp("nvidia-smi", "nvidia-smi", "--query-gpu=uuid", "--format=csv", NULL);
        return 1;
    }

    int status;
    if (waitpid(pid, &status, 0) == -1) {
        return FALSE;
    }

    return WIFEXITED(status) && (WEXITSTATUS(status) == 0);
}

int main(int argc, char *argv[])
{
    while (check_nvidia()) {
        sleep(5);
    }

    execl("/apps/kill-all.sh", "/apps/kill-all.sh", NULL);
    return 1;
}
