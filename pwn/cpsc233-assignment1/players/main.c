#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>
#include <time.h>

typedef int student_func(int,int,int);

void get_flag() {
    char flag[0x30];
    memset(flag,0,0x30);
    FILE * f = fopen("flag.txt", "r");
    if (f == NULL) {
        printf("no flag, contact admin\n");
        exit(-1);
    }
    fread(&flag,1,sizeof(flag),f);
    fclose(f);
    printf("Congratulations! You have completed your assignment, here is your flag: %s\n",flag);
}

int read_shellcode(char * dest, int length) {
    char * hex_str = malloc(length*2+1);
    ssize_t n_bytes = read(0,hex_str,length*2);
    for (ssize_t i=0;i<n_bytes/2;i++){
        if (!sscanf(&hex_str[i*2],"%2hhx",&dest[i])) {
            return 0;
        };
    }
    free(hex_str);
    return 1;
}

int auto_grader(int test_id, student_func * func,int p1,int p2,int p3, int soln) {
    int grade = 0;
    int result = func(p1,p2,p3);
    printf("==== Test %d ====\n",test_id);
    if (result == soln){
        puts("Score: 1/1");
        grade = 1;
    }else {
        puts("Score: 0/1");
        grade = 0;
    }
    puts("");
    printf("Expected: %d\nYour Reuslt: %d\n",soln,result);
    puts("===================\n");
    return grade;
}

int assignment_1(void * func, int full_mark) {
    srand(time(NULL));
    int grade = 0;
    int p1,p2,p3;
    for (int i=0;i<full_mark;i++){
        p1 = rand() % 0x100;
        p2 = rand() % 0x100;
        p3 = rand() % 0x100;
        grade += auto_grader(i+1,((student_func *)func),p1,p2,p3,p1+p2+p3);
    }
    if (grade == full_mark){
        get_flag();
    }
    return grade;
}

void init_chall() {
    alarm(60);
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
}


int main() {
    init_chall();
    char * func = mmap((void *)0x2333000,0x1000,7,0x21,0,0);
    puts("please put your function shellcode here: ");
    if (!read_shellcode(func,0x200)) {
        puts("fail to read shellcode, please check your shellcode");
        exit(-1);
    };
    int total = 0x10;
    int grade =assignment_1((void*) func, total);
    printf("Your Grade: %d/%d\n",grade,total);
}