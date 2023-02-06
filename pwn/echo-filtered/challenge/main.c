#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

// void here() {
//     char flag[0x30];
//     memset(flag,0,0x30);
//     FILE * f = fopen("flag.txt", "r");
//     if (f == NULL) {
//         printf("no flag, contact admin\n");
//         exit(-1);
//     }
//     fread(&flag,1,sizeof(flag),f);
//     fclose(f);
//     printf("%s\n",flag);
// }


void send_feedback() {
    char buf[0x10];
    printf("Thanks for using our echo system, please share your feedback:\n");
    gets(buf);
    printf("Thanks, we have received your feedback!\n");
}

int contains_illegal(char * s, int len) {
    for (int i=0;i<len;i++) {
        if (109 <= s[i] && s[i] <=122) {
            return 1;
        }
    }
    return 0;
}

void init_chall() {
    alarm(60);
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
}

int main(int argc, char const *argv[])
{
    init_chall();
    char allowed[16] = "abcdefghijklm\x00";
    char * buf = malloc(0x100);
    printf("Echo Service v0.5 (mode: filtered)\n");
    printf("Character allowed: ");
    for (int i=0;i<strlen(allowed);i++) {
        printf("%c ",allowed[i]);
    }
    printf("\n");
    while (1) {
        fgets(buf,0x100,stdin);
        if (contains_illegal(buf,strlen(buf))) {
            printf("contains illegal character!!!\n");
            break;
        }
        printf(buf);
    }
    send_feedback();
    return 0;
}