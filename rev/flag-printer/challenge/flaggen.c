#define _GNU_SOURCE

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
    //maple{r3v3r_0r_p4tch3r?}
    const char* flag[] = {"maple", "r3v3r", "0r", "p4tch", "3r"};

    long data[5] = {0};

    for(int i = 0; i < 5; i++) {
        data[i] = a64l(flag[i]);
    }

    memfrob(data, sizeof(data));

    printf("Result buffer: {");
    for (int i = 0; i < sizeof(data); i++) {
        printf("0x%hhx, ", ((unsigned char*)data)[i]);
    }
    printf("};\n");
}