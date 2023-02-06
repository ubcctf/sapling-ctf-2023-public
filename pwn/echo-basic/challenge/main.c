#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <unistd.h>

#define FLAG_LEN 64

char flag[FLAG_LEN];

void h3re() {
    char flag[0x30];
    memset(flag,0,0x30);
    FILE * f = fopen("flag.txt", "r");
    if (f == NULL) {
        printf("no flag, contact admin\n");
        exit(-1);
    }
    fread(&flag,1,sizeof(flag),f);
    fclose(f);
    printf("%s\n",flag);
}

void init_chall() {
    alarm(60);
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
}

int main(int argc, char const *argv[])
{
    init_chall();
    srand(time(0));

    char * buf = malloc(0x30);
    int * owo = malloc(0x8);
    int ovo = abs(rand())+0x1337;
    *owo = ovo;
    printf("Echo Service v0.1 (mode: basic)\n");
    printf("echo whatever you want!\n");
    while (1) {
        fgets(buf,0x30,stdin);
        printf(buf);
        if (*owo+0x1337 == ovo) {
            printf("O.O: ");
            h3re();
        }
    }

    return 0;
}
