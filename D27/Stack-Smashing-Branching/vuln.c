#include <stdio.h>

void secretFunction(){
    printf("You have entered the secret function!\n");
}

void echo(){
    char buffer[20];
    printf("Enter some text:\n");
    scanf("%s", buffer);
    printf("You entered: %s\n", buffer);
}

int main(int argc, char **argv){
    echo();
    return 0;
}