#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include <sys/stat.h>

static void wait_for_x11()
{
    struct stat statbuf;
    while(stat("/tmp/.X11-unix/X0", &statbuf)) {
        sleep(1);
    }
}

int main(int argc, char *argv[])
{
    setenv("DISPLAY", ":0", 1);
    wait_for_x11();
    execvp(argv[1], argv + 1);
    return 1;
}
