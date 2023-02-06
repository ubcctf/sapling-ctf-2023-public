#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>

char msgs[0x10][0x20];

int get_int() {
  char buffer[0x10];
  fgets(buffer, 0x10, stdin);
  return atoi(buffer);
}

void init_chall() {
    alarm(60);
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
}

void set_msg() {
    printf("index (0-15): ");
    int index = get_int();
    if (index > 15 && index < 0) {
        puts("invalid index.");
        return;
    }
    printf("leave your message here: ");
    read(0, msgs[index], 0x20);
}

void echo_msg() {
    printf("index (0-15): ");
    int index = get_int();
    if (index > 15 && index < 0) {
        puts("invalid index");
        return;
    }
    puts(msgs[index]);
}

int main(int argc, char const *argv[])
{
    init_chall();
    int choice = 0;
    puts("Echo Service v1.0 (mode: message board)");
    while (1) {
        printf("1. echo a message.\n2. leave a message\nchoice: ");
        choice = get_int();
        if (choice == 1) {
            echo_msg();
        }
        if (choice == 2) {
            set_msg();
        }
    }
    return 0;
}