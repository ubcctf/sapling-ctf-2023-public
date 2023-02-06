#include <stdio.h>
#include <sys/stat.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <ctype.h>
#include <errno.h>

//linked list for storing mapping
struct node {
    struct node* next;
    char* word;
    int size;
};

//int serialization that avoids null bytes
char* serialize_int(char* buf, unsigned int val) {
    //byte - size; vararr & 0b10000000 - actual values in big endian
    //32 bit needs ~4.57 bytes to encode, so 5 in total + 1 byte for size at most
    //special case - when val is 0 the while loop doesnt work well even though the logic is the same
    if(!val) {
        buf[0] = 1;
        buf[1] = 0x80;
        return buf + 2;
    }

    char* ptr = &buf[1];
    while(val) {
        *ptr++ = (val & 0b01111111) | 0b10000000;
        val >>= 7;
    }
    buf[0] = ptr - buf - 1;
    return ptr;
}

int node_index(struct node* node, char* word, int size) {
    //printf("%s\n", word);
    int i = 0;
    while(node) {
        if(!strncmp(node->word, word, size) && node->size == size) {
            return i;
        }
        i++;
        node = node->next;
    }
    return -i;   //negative signifies not found, and value is the next index in the list
}

char* strtok_symbols(char* buf) {
    //consider all symbols standalone tokens
    if(*buf && !isalpha(*buf)) return buf+1;

    while(*buf++) {
        if(!isalpha(*buf))
            return buf;
    }
    return NULL;
}


/**
 * a very simple token based compression algorithm that has the following properties:
 *   - 2 distinct non null segments separated by a single null byte
 *     - pointer mapping at the front
 *       - the pointers are integer indices of the word in the token mapping at the location where the token used to be
 *     - token mapping at the end
 *       - every token is prefixed by an integer storing the size instead of null terminated
 *   - integers are stored such that no null bytes is possible:
 *     - each integer is variable sized, with the size prepended to the actual data
 *     - this is followed by the integer in big endian format, except only occupying 7 bits with the uppermost bit always 1
 * this algorithm is pretty useless practically due to the inefficiency in storing integers, and the applied tokenization is also too simple to allow efficient compression
 * and also only really works on ascii code (strtok_symbols breaks up unicode into chunks thats unreadable)
 * but hey this isn't a leetcode problem this is a reversing challenge :) 
 * also totally not inspired by an actual serialization algorithm i saw irl recently (coughcoughIDAcough) so hey similar things are used in prod right now
 */
int main(int argc, char* argv[]) {
    if(argc < 3) {
        puts("Usage: ./canner <textfile> <outfile>");
        return -1;
    }

    int fd = open(argv[1], O_RDONLY, 0);

    if(fd < 0) {
        puts("Stuff to be canned not found, quitting...");
        return -1;
    }

    //get size
    struct stat st;
    stat(argv[1], &st);

    char* buf = calloc(1, st.st_size + 1);

    //in the worst case (a lot of cases actually since most repeating tokens are short enough or long tokens arent repeating so that this compression algorithm is making it worse instead)
    //this compression method can be bigger than the original size (if every character is a non-alphanumeric symbol)
    //but it wouldnt be bigger than a byte + 2 bytes storing the size of that word (size of the int + size itself)
    char* out = calloc(1, st.st_size * 2 + 1);

    //it's a play compressor, we don't expect huge text files
    read(fd, buf, st.st_size); 
    close(fd);

    //use calloc to avoid uninitialized values
    struct node* head = NULL, *tail = NULL;
    int dictsize = 0;

    char* prev, *ptr = buf, *outptr = out;  //we will initialize prev in the while loop anyway
    while((prev = ptr, ptr = strtok_symbols(ptr))) {
        int size = ptr - prev;
        int idx = node_index(head, prev, size);

        if(idx <= 0) {
            char* word = calloc(1, size+1);
            strncpy(word, prev, size);
            struct node* node = calloc(1, sizeof(struct node));
            node->size = size;
            node->word = word;
            
            if(!head) {
                head = node;
                tail = node;
            } else {
                tail->next = node;
                tail = node;
            }

            idx = -idx;
        }
        outptr = serialize_int(outptr, idx);
    }

    //we know for sure the array we encoded things with has no null in it by design, so null terminate it to signify start of lookup dict and append the lookup word list
    *outptr++ = '\0';

    //write 
    struct node* next = head;
    while(next) {
        struct node* curr = next;

        //printf("node %p: %d - '%s'\n", curr, curr->size, curr->word);

        //pascal string like encoding
        outptr = serialize_int(outptr, curr->size);
        strncpy(outptr, curr->word, curr->size);

        outptr += curr->size;
        next = curr->next;
        free(curr->word);
        free(curr);
    }

    int outfd = open(argv[2], O_WRONLY|O_TRUNC|O_CREAT, 0644);

    if (outfd < 0) {
        puts("Cannot find a place to store the can, quitting...");
        return -1;
    }

    int datasize = strlen(out);
    write(outfd, out, datasize);
    write(outfd, "\0", 1);

    char* mapptr = out+datasize+1;
    write(outfd, mapptr, strlen(mapptr));

    close(outfd);
    puts("Done! Enjoy your canned text for long term storage :)");

    free(out);
    free(buf);
}