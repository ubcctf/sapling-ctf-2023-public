#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#define FLAG_LEN 0x30

char flag[FLAG_LEN];

int get_int() {
  char buffer[0x10];
  fgets(buffer, 0x10, stdin);
  return atoi(buffer);
}

void load_flag() {
    FILE * f = fopen("flag.txt", "r");
    if (f == NULL) {
        printf("no flag, contact admin\n");
        exit(-1);
    }
    fread(&flag,1,FLAG_LEN,f);
    fclose(f);
}

void init_chall() {
    alarm(60);
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
}

void wrong() {
    puts("Wrong!");
    exit(0);
}

void q1() {
    int val = -1;
    puts("Q1: 1+1=");
    printf("Answer: ");
    val = get_int();
    if (val != 2) {
        wrong();
    }
    puts("Correct!");
}

void q2() {
    int x = -1;
    int y = -1;
    int answer = 0;
    puts("Q2: solve X+Y=-123456 for X > 0 and Y > 0");
    printf("X: ");
    x = get_int();
    printf("Y: ");
    y = get_int();
    if (x <= 0 || y <= 0) {
        puts("X and Y must be positive integers!");
        wrong();
    }
    answer = x + y;
    printf("%d + %d = %d\n",x,y,answer);
    if (answer != -123456) {
        wrong();
    }
    puts("Correct!");
}

void q3() {
    char answer[0x30];
    puts("Q3: What is the longest word in any of the major English language dictionaries is?");
    printf("Answer: ");
    gets(answer);
    if (strcmp(answer,"pneumonoultramicroscopicsilicovolcanoconiosis") != 0) {
        printf("%s is not correct!\n",answer);
        wrong();
    }
    puts("Correct!");
}

void q4() {
    char answer[0x30];
    char correct_answer[0x30];
    strncpy(correct_answer,flag,0x30);
    puts("Q4: What is the flag?");
    printf("Answer: ");
    gets(answer);
    if (strncmp(answer,correct_answer,0x30) != 0) {
        printf("%s is not correct!\n",answer);
        wrong();
    }
    puts("Correct!");
}

int main(int argc, char const *argv[])
{
    init_chall();
    load_flag();
    puts("Quiz start! complete all question and get the flag!");
    puts("                                  - Prof. Owoflovo.");
    q1();
    q2();
    q3();
    q4();
    puts("Congratulations! You pass the quiz!");
    printf("Here is the flag: %s",flag);
    return 0;
}