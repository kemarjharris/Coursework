#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
int main() {

    int i = 1;
    int  j = 10;
    int k = 20;
    int x;
    while(i < 3 && i > -1) {
        x = fork();
	if (x == -1) {
	    perror("fork");
	    return 1;
	} else if (x == 0) {
	// Children loops
	// Both children should be running simoultaneously 
	while (j ++ < 20 && k ++ < 30) {
	usleep(200);
	if (i ==1) { // Child one should be running
	        printf("I'm child one, my pid is %d and my current number is %d\n", getpid(), j);
	} else if (i == 2) { // Child two chould be running
		 printf("I'm child two, my pid is %d and my current number is %d\n", getpid(), k);
	}
	}
	    i = -1;
	} else { // Parent, continue loop and wait on children
	  i++;
	}
	 
    }

    if (x > 0) {
	int a;
	for (a =1; a < i; a++) {
            /* parent */
            int status; 
	    int pid;
            if ((pid = wait(&status)) == -1) {
	        perror("wait");
	    } else {
                printf("pid %d exit status %d\n", pid, WEXITSTATUS(status));
	    }
	}
	printf("parent terminating with pid %d\n", getpid());
        return(0);
    }

    // Children do this, so return 1
    return 1;
}
