#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#define FLAG_LEN 0x30
// admin id should have least significant byte be 0x00
#define ADMIN_ID 0x55baa500

typedef struct clock_user {
    char name[64];
    int id;
} user_t;

time_t current_time = 0;
user_t admin;
user_t user;

int get_str(char * s,int size) {
    char c;
    int i;
    for(i=0;i<size;i++)
    {
        c = getchar();
        if (c == '\n') {
            break;
        }
        s[i]= c;
    }
    s[i] = '\x00';
    return i;
}

int get_int() {
  char buffer[0x10];
  fgets (buffer, 0x10, stdin);
  return atoi(buffer);
}

void set_current_time(unsigned int time) {
    current_time = time;
    srand(time);
}

void reset_user(user_t *user) {
    // user id should have least significant byte be 0x01
    user->id = (rand() & 0xffffff00) | 0x1;
    printf("hello, please put your name (max 64 character): \n");
    get_str(user->name, 64);

    printf("Welcome to clock system %s\n",user->name);
    printf("Your account has been reset. Your new id is %x\n",user->id);
}

void get_secret(user_t *user) {
    if (user->id != ADMIN_ID) {
        puts("You are not admin!!!!");
        exit(0);
    }
    char flag[FLAG_LEN];
    FILE* fp = fopen("flag.txt", "r");

    if (fp == NULL) {
        puts("Could not open flag file");
        exit(1);
    }
    fgets(flag, FLAG_LEN, fp);
    printf("Here is your secret: %s\n",flag);
}

void init_chall() {
    alarm(60);
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
}

void setup() {
    set_current_time(time(0));
    strncpy(admin.name,"admin\x00",6);
    admin.id = ADMIN_ID;
}

int main() {
    init_chall();
    setup();
    user_t *current_user = &user;
    puts("Please login: ");
    puts("1. new account");
    puts("2. admin");
    int l = get_int();
    if (l == 2) {
        puts("you are not admin");
        exit(0);
        current_user = &admin;
    }
    if (l != 1) {
        puts("invalid account");
        exit(0);
    }
    reset_user(current_user);
    puts("Welcome to my clock system, you can: ");
    puts("1. get current time");
    puts("2. set current time");
    puts("3. reset your account");
    puts("4. exit");
    while (1) {
        printf("> ");
        int op = get_int();
        switch (op) {
        case 1 : 
            {
                printf("Current time is %s",ctime(&current_time));
                break;
            }
        case 2: 
            {
                printf("please enter current time: ");
                set_current_time(get_int());
                break;
            }
        case 3:
            {
                reset_user(current_user);
                break;
            }
        case 4:
            {
                puts("bye~~~");
                exit(0);
                break;
            }
        case 0x1337:
            {
                get_secret(current_user);
                break;
            }
        }
    }
}