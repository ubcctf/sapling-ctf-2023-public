#include <time.h>
#include <stdlib.h>
#include <stdio.h>

// 0x55baa5

int main() {
    for (unsigned int i=0;i<=4294967295;i++) {
        srand(i);
        for (int j=0;j<32;j++) {
            int v = rand();
            if (((v >> 8) == 0x55baa5)) {
                printf("find seed = 0x%x (%d), iter = %d\n",i,i,j+1);
                exit(0);
            }
        }
    }
}