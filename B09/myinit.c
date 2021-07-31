#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
int main(int argc, char** argv) {
    
    int opt;
    int status = 0;
    char *runLevel = "3";

    while ((opt = getopt(argc, argv, "r:")) != -1) {
        switch (opt) {
        case 'r':
            // Force run level to be only one char long
            if (strlen(optarg) > 1) {
                  status = 10;
            }
            runLevel = optarg;
        break;
        case '?': // Odd case where invalid option is entered
        default:
            status = 2;
        }
    }

    int args = argc - optind; // Number of given argumens

    if (argc == optind || args > 1) {
        fprintf(stderr, "usage: myinit [-r runlevel] file\n");
        status = 3;
        return status;
    } else if (status == 10) {
        fprintf(stderr, "runlevel must be a single character\n");
        return status;
    }

    int colonCount;	
    FILE *fp;
    char *p;
    char buf[300];
    char config[3][300];
    int pCount = 0;
    int x = 1;
	
    if ((fp = fopen(argv[optind], "r")) == NULL) {
        perror(argv[args]);
        return 1;
    }

    while (fgets(buf, sizeof buf, fp) != NULL && x) {
	// Remove new line and comments from the string on this line
      if ((p = strchr(buf, '#')))
        *p = '\0';
      if ((p = strchr(buf, '\n')))
	*p = '\0';
      if (buf[0] != '\0' ) { // If this line is solely the terminating character (ie a newline or comment), ignore it
	
	char *a = buf;
	char *b = buf;
	char *c = buf;
	colonCount = 0;
	int valid = 0;
	// Move c to the end of the string, and count the number of colons
	while ( *c != '\0') {
	    if (*c == ':') {
		colonCount ++;
	    } 
	    c++;
	}
	// If the correct number of colons are seen, then continue, otherwise output error and go on to next iteration
	if (colonCount >=2) {
	    valid = 1;
	} else {
	    fprintf(stderr, "myinit: unparseable line '%s', ignored\n", buf);
	}
	
	// Correct number of colons seen, split the given string into three seperate parts
	if (valid) {	
    	    colonCount = -1;
	    
	    while (b < c) {
                if ( colonCount < 1  ) {
    	            if ((b = strchr(b, ':')))  {
		        *b = '\0';
		        b ++;
		    }
	            colonCount++;
		    } else {
		        colonCount++;
		        b = c;
		    } 
	        strcpy(config[colonCount], a);
	        a = b; 
	     }

	     int respawn = strcmp("respawn", config[1]) ? 0 : 1;
	     int once = strcmp("once", config[1]) ? 0 : 1;
	     
	     // Run this if its same run level or nothing at all
	     if ((strchr(config[0], *runLevel)) || config[0][0] == '\0') {
	         pCount ++;	   
	         x = fork();
	         if (x == -1) {
	 	    perror("fork");
		    return(5);
	         } else if (x == 0) {
		     // Child process
		     usleep(100);
		     // Case of once, run the process only once then terminate
		     if (once) {
		         execl("/bin/sh", "sh", "-c", config[2], (char *)NULL);
		         perror("/bin/sh");
                         exit(9);
		     } else if (respawn) {
		     // Respawn case, child forks, grandchild waits for child to finish. 
			do {
		            x = fork();
		    	    usleep(100);
		    	    if (x == -1) { 
				perror("fork"); 
				return 5;
	            	    } else if (x == 0) { // Child 2 runs
				execl("/bin/sh", "sh", "-c", config[2], (char *)NULL);
				perror("/bin/sh");
				exit(9);	
		    	    } else { // Child 1 waits on child2, and when child two finishes it retarts this loop
			        int c2status, c2pid;
				if ((c2pid = wait(&c2status)) == -1 ) {
			    	    perror("wait");
			            return 7;
				} 
		    	    }	
			} while (respawn);

		     } else {// Second spot in config wasnt respawn or once, fatal error
			 fprintf(stderr, "myinit: invalid action '%s', second field must be either respawn or once\n", config[1]);
		     }
	         } 
	    }
	}
      }
    }
    
    if (x) { // Parent waits for children
    fclose(fp);
    int i;
    for (i = 0; i < pCount; i++) {
        int childStatus, pid;
        if ((pid = wait(&childStatus)) == -1){ 
	    perror("wait");
	    return 7;
	}
    }
    return 0;
    }
}
