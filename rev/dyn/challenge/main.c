#include <stdio.h>
#include <string.h>

unsigned char key[5][5] = {
    {'S', 'A', 'P', 'L', 'I'},
    {'N', 'G', 'B', 'C', 'D'}, 
    {'E', 'F', 'H', 'J', 'K'},
    {'M', 'O', 'Q', 'R', 'T'},
    {'U', 'V', 'W', 'X', 'Y'}
};
unsigned char key_map[25] = {1, 18, 19, 20, 32, 33, 17, 34, 4, 35, 36, 3, 48, 16, 49, 2, 50, 51, 0, 52, 64, 65, 66, 67, 68};
unsigned char flag[] = "VQVBNCSALQKMYIEMIO";
int flag_len = sizeof(flag) - 1;

int main(int argc, char** argv){
    
    if(argc != 2){
        puts("Usage: ./dyn FLAG");
        return 0;
    }

    if(strlen(argv[1]) != flag_len + strlen("maple{}") || memcmp(argv[1], "maple{", strlen("maple{")) || argv[1][strlen(argv[1])-1] != '}'){
        puts("Try again!");
        return 0;
    }

    for(int i = 0; i < flag_len; i += 2){
        int row_0 = (key_map[flag[i] - 0x41] & 0xf0) >> 4;
        int col_0 = key_map[flag[i] - 0x41] & 0x0f;

        int row_1 = (key_map[flag[i+1] - 0x41] & 0xf0) >> 4;
        int col_1 = key_map[flag[i+1] - 0x41] & 0x0f;

        if (col_0 == col_1){
            int row_0_idx = (5 + ( (row_0-1) % 5)) % 5;
            int row_1_idx = (5 + ( (row_1-1) % 5)) % 5;
            flag[i] = key[row_0_idx][col_0];
            flag[i+1] = key[row_1_idx][col_0];
        } else if (row_0 == row_1){
            int col_0_idx = (5 + ( (col_0-1) % 5)) % 5;
            int col_1_idx = (5 + ( (col_1-1) % 5)) % 5;
            flag[i] = key[row_0][col_0_idx];
            flag[i+1] = key[row_0][col_1_idx];
        } else {
            flag[i] = key[row_0][col_1];
            flag[i+1] = key[row_1][col_0];
        }
    }

    if(memcmp(argv[1]+strlen("maple{"), flag, flag_len)){
        puts("Try again");
    } else {
        puts("Correct!");
    }
    return 0;
}