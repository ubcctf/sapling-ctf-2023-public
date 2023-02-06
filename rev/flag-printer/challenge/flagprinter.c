#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char data[] = {0x98, 0x73, 0xed, 0x0, 0x2a, 0x2a, 0x2a, 0x2a, 0x5d, 0x9b, 0x3d, 0x1d, 0x2a, 0x2a, 0x2a, 0x2a, 0xe8, 0x27, 0x2a, 0x2a, 0x2a, 0x2a, 0x2a, 0x2a, 0x9f, 0xbb, 0x89, 0x7, 0x2a, 0x2a, 0x2a, 0x2a, 0xef, 0x27, 0x2a, 0x2a, 0x2a, 0x2a, 0x2a, 0x2a};

int main() {
    long workbuf[5] = {0};

    memcpy(workbuf, data, sizeof(data));
    memfrob(workbuf, sizeof(workbuf));

    char flag[25] = {0};

    strcat(flag, l64a(workbuf[0]));
    flag[5] = '{';
    strcat(flag, l64a(workbuf[1]));
    flag[11] = '_';
    strcat(flag, l64a(workbuf[2]));
    flag[14] = '_';
    strcat(flag, l64a(workbuf[3]));
    strcat(flag, l64a(workbuf[4]));
    flag[22] = '?';
    flag[23] = '}';
    
    printf("Here's your flag: %s\n", flag);
}