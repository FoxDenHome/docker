#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char *argv[])
{
    if (getpid() != 1) {
        return 1;
    }

    setresgid(0, 0, 0);
    setresuid(0, 0, 0);

    execl("/usr/bin/supervisord", NULL);
    
    return 2;
}
