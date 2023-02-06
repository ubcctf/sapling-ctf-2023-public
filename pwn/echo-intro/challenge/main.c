#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


void init_chall() {
    alarm(60);
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
}

int main(int argc, char const *argv[])
{
    init_chall();
    printf("Echo Service v0.0\n");
    printf("echo once\n");
    char buf[0x100];
    char * flag = malloc(0x30);
    FILE * f = fopen("flag.txt", "r");
    if (f == NULL) {
        printf("no flag, contact admin\n");
        exit(-1);
    }
    fread(flag,1,0x30,f);
    fclose(f);
    fgets(buf,0x100, stdin);
    printf(buf);
    return 0;
}
