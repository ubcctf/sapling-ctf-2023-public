#include "font.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void print_4bit_char_row(char c) {
    putchar(c & 0b1000 ? '#' : '_');
    putchar(c & 0b0100 ? '#' : '_');
    putchar(c & 0b0010 ? '#' : '_');
    putchar(c & 0b0001 ? '#' : '_');
}

void set_4bit_char_row(char *b, char c) {
    b[0] = c & 0b1000 ? '#' : '_';
    b[1] = c & 0b0100 ? '#' : '_';
    b[2] = c & 0b0010 ? '#' : '_';
    b[3] = c & 0b0001 ? '#' : '_';
}

void print_char(char c) {
    char temp = 0;
    for (int rleft = char_height - 1; rleft >= 0; rleft--) {
        temp = bitmap_font[c] >> (rleft * char_width);
        print_4bit_char_row(temp);
        putchar('\n');
    }
    putchar('\n');
}

char get_art_pixel(char *a, int alen, int r, int x) {
    return a[(r * alen * char_width) + x];
}

void set_art_pixel(char *a, char v, int alen, int r, int x) {
    a[alen * char_width * r + x] = v;
}

char *make_base_art(char *s, int len) {
    int awidth = len * char_width;
    int asz = char_height * awidth;
    char *art = malloc(asz);
    char temp = 0;
    for (int rleft = char_height - 1; rleft >= 0; rleft--) {
        for (int c = 0; c < len; c++) {
            temp = bitmap_font[s[c]] >> (rleft * char_width);
            set_4bit_char_row(
                &art[((char_height - 1 - rleft) * awidth) + (c * char_width)],
                temp);
        }
    }
    return art;
}

void reflect_art_1(char *a, int alen) {
    int max_row = char_height - 1;
    int max_col = alen * char_width - 1;
    for (int r = 0; r < char_height / 2; r++) {
        for (int x = 0; x <= max_col; x++) {
            char orig = get_art_pixel(a, alen, r, x);
            char refl = get_art_pixel(a, alen, max_row - r, x);
            set_art_pixel(a, refl, alen, r, x);
            set_art_pixel(a, orig, alen, max_row - r, x);
        }
    }
}

void reflect_art_2(char *a, int alen) {
    int max_row = char_height - 1;
    int max_col = alen * char_width - 1;
    for (int r = 0; r < char_height; r++) {
        for (int x = 0; x <= max_col / 2; x++) {
            char orig = get_art_pixel(a, alen, r, x);
            char refl = get_art_pixel(a, alen, r, max_col - x);
            set_art_pixel(a, refl, alen, r, x);
            set_art_pixel(a, orig, alen, r, max_col - x);
        }
    }
}

void rotate_art(char *a, int alen) {
    int max_col = alen * char_width - 1;
    for (int dr = 0; dr < char_height - 1; dr += 2) {
        for (int dx = 0; dx < max_col; dx += 2) {
            char c1 = get_art_pixel(a, alen, dr, dx);
            char c2 = get_art_pixel(a, alen, dr, dx + 1);
            char c3 = get_art_pixel(a, alen, dr + 1, dx + 1);
            char c4 = get_art_pixel(a, alen, dr + 1, dx);
            set_art_pixel(a, c2, alen, dr, dx);
            set_art_pixel(a, c3, alen, dr, dx + 1);
            set_art_pixel(a, c4, alen, dr + 1, dx + 1);
            set_art_pixel(a, c1, alen, dr + 1, dx);
        }
    }
}

void print_art(char *a, int alen) {
    int awidth = alen * char_width;
    for (int r = 0; r < char_height; r++) {
        for (int x = 0; x < awidth; x++) {
            putchar(get_art_pixel(a, alen, r, x));
        }
        putchar('\n');
    }
    putchar('\n');
}

void art(char *s) {
    int l = (int)strlen(s);
    char *a = make_base_art(s, l);
    reflect_art_1(a, l);
    reflect_art_2(a, l);
    for (int i = 0; i < (l % 3 + 1); i++) {
        rotate_art(a, l);
    }
    print_art(a, l);
    free(a);
}

/* char *flag = "maple{who_gave_computers_the_right?}"; */

char input[100] = {0};

int main(int argc, char **argv) {
    putchar('>');
    putchar(' ');
    scanf("%99s", input);
    art(input);
}
