#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main()
{
    int x = fork();
    if (x == -1) {
        perror("fork");
        return(1);
    } else if (x == 0) {
        /* child */
        execl("/bin/sh", "sh", "-c", "echo Aha, run-level 4!", (char *)NULL);
        perror("/bin/sh");
        return(1);
    } else {
        /* parent */
        int status, pid;
        pid = wait(&status);
        printf("pid %d exit status %d\n", pid, WEXITSTATUS(status));
        return(0);
    }
}
