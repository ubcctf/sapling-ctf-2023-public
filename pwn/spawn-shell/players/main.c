#include <stdlib.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>

void init_chall() {
    alarm(60);
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
}

int main(int argc, char const *argv[])
{
    char buf[0x20];
    puts("Enter a command: ");
    fgets(buf,0x20,stdin);
    system(buf);
    return 0;
}