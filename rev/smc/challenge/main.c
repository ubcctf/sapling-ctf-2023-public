#include <sys/mman.h>
#include <stdio.h>
#include <errno.h>
#include <unistd.h>
#include <string.h>



void init(unsigned char* buf, int buf_len, unsigned char* key, int key_len){
    int PAGE_SIZE = sysconf (_SC_PAGE_SIZE);
    void* page_start = (void*) ((unsigned long) buf & ~(PAGE_SIZE-1));

    if(mprotect(page_start, PAGE_SIZE, PROT_READ | PROT_WRITE | PROT_EXEC)){
        fprintf(stderr, "mprotect: %s\n", strerror(errno));
    }

    for(int i = 0; i < buf_len; i++){
        buf[i] = buf[i] ^ (key[i % key_len]);
    }

    mprotect(page_start, PAGE_SIZE, PROT_READ | PROT_EXEC);
}

int main(int argc, char** argv){
    unsigned char key[] = {146, 77, 249, 203, 246, 182, 174, 118, 220, 101, 43, 32, 141, 93, 159, 234, 31, 120, 117, 82, 25, 91, 176, 79, 143, 42, 38, 20, 186, 55, 246, 167};
    init((unsigned char*)&&prog_start,(int)(&&prog_end - &&prog_start), key, sizeof(key));

    prog_start:;
    char err_msg[] = "Usage: ./smc FLAG\n";
    int flag_arr[] = {2154409207, 1935128327, 404088430, 3304081820, 2442991766, 1632504486, 1030181976, 1908459548, 2473750124};
    int k[] = {1630049007, 821987277, 364436290, 1183191165, 1718032019, 1615246736, 973660722, 1488014256, 372453177};
    
    if(argc != 2){
        puts(err_msg);
        return 0;
    }

    int len = strlen(argv[1]);
    if(len != sizeof(flag_arr) ){
        puts("Nope!");
        return 0;
    }
    len = len / sizeof(int);
    int* input = (int*) argv[1];
    
    for(int i = 0; i < len-1; i++){
        input[i] = (input[i] ^ input[i+1]) + k[i];
    }
    input[len-1] += k[len-1];

    if(memcmp(input, flag_arr, sizeof(flag_arr))){
        puts("Nope!");
    } else {
        puts("Wow that is right!");
    }
    prog_end:
    return 0;
}