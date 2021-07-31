#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
int main(int argc, char** argv) {
    
    int opt;
    int status = 0;
    char *runLevel = "3";
    char* progname = argv[0];

    while ((opt = getopt(argc, argv, "r:")) != -1) {
        switch (opt) {
        case 'r':
                // Force run level to be only one char long
            if (strlen(optarg) > 1) {
                  status = 1;
            }
            runLevel = optarg;
        break;
        case '?':
        default:
                status = 2; // assuming getopt does this checking for me
        }
    }

        int args = argc - optind; // Number of given argumens

        if (argc == optind) {
                fprintf(stderr, "usage: %s [-r runlevel] file\n", progname);
                status = 3;
                return status;
        } else if (status == 1) {
            fprintf(stderr, "runlevel must be a single character\n");
                return status;
        }

    printf("run level is %c\n", *runLevel);

    int colonCount;	
    FILE *fp;
    char *p;
    char buf[300];
    char config[3][300];
    
    if ((fp = fopen(argv[optind], "r")) == NULL) {
        perror(argv[args]);
        return 1;
    }

    while (fgets(buf, sizeof buf, fp) != NULL) {
	// Clean input
	if ((p = strchr(buf, '#')))
	    *p = '\0';
	if ((p = strchr(buf, '\n')))
	    *p = '\0';
	if (buf[0] != '\0' ) { 		
	printf("%s\n", buf);

	char *a = buf;
	char *b = buf;
	char *c = buf;
	colonCount = -1;
	while ( *c != '\0') { c++;}

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

	if ((strchr(config[0], *runLevel)) || config[0][0] == '\0') {
	    int i =0;
	    for (i = 0; i < 3; i++) {
                printf("%s\n", config[i]);
    	    }
	}
	}
    }

    fclose(fp);
	
	return 0;
}
