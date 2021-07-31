#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

int main(int argc, char **argv)
{
    int opt; 
	int status = 0;
	int runLevel = 3;
	
    char* progname = argv[0];
	
    while ((opt = getopt(argc, argv, "r:")) != -1) {
	switch (opt) {
	case 'r':
		// Force run level to be only one char long
	    if (strlen(optarg) > 1) {
			status = 1;
		}
	    runLevel = atoi(optarg);
	    printf("run level is %d\n", runLevel);
	break;
	case '?':
	default:
		status = 2; // assuming getopt does this checking for me
	}
    }
	
	int args = argc - optind; // Number of given argumens
	
	if (args > 1) {
		fprintf(stderr, "usage: %s [-r runlevel] file\n", progname);
		status = 3;
		return status;
	} else if (status == 1) {
	    fprintf(stderr, "runlevel must be a single character\n");
		return status;
	}
	
	
}
