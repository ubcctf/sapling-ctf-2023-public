#include <stdlib.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>

const int flag_len = 0x1c;

int get_int() {
  char buffer[0x10];
  fgets(buffer, 0x10, stdin);
  return atoi(buffer);
}

// check if flag exists and verify flag is the right length
int is_flag_exits() {
    char flag[0x20];
    int fd = open("flag.txt",O_RDONLY);
    if (fd == -1){
        return 0;
    }
    if (read(fd,flag,0x20) != flag_len) {
        return 0;
    };
    close(fd);
    return 1;
}

// my cool random generator
int rand_generator() {
    char seed;
    int fd;
    char rand_values[0x20];
    fd = open("/dev/urandom", O_RDONLY);
    if (fd == -1){
        return 0;
    }
    read(fd,&seed,1);
    close(fd);
    puts("How many random number you want: ");
    fd = get_int();
    if (fd < 0 || fd > 0x20) {
        puts("we can only generate 32 random values now.");
    }
    puts("here is your random values");
    for (int i=0;i<fd;i++) {
        printf("%hhu ",rand_values[i]^seed);
    }
    puts("\nThanks for using my new random generator!");
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
    if (is_flag_exits()){
        rand_generator();
    }else {
        printf("Contact admin\n");
    }
    return 0;
}