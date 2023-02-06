#include "item.h"
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <termios.h>
#include <unistd.h>

#define W 80
#define H 40
#define MARGIN 2
#define WALL_U MARGIN
#define WALL_D (H - 1 - 2 * MARGIN)
#define WALL_L MARGIN
#define WALL_R (W - MARGIN)
#define DOOR_U ((WALL_D / 2) - 3)
#define DOOR_D ((WALL_D / 2) + 3)
#define DOOR_L ((WALL_R / 2) - 5)
#define DOOR_R ((WALL_R / 2) + 5)
#define LADDER_C_X (WALL_L + 3)
#define LADDER_C_Y (WALL_U + 2)
#define LADDER_F_X (WALL_R - 3)
#define LADDER_F_Y (WALL_D - 2)
#define ITEM_U (LADDER_C_Y + 1)
#define ITEM_D (LADDER_F_Y - 1)
#define ITEM_L (LADDER_C_X + 1)
#define ITEM_R (LADDER_F_X - 1)
#define BUFLEN 5
#define FLAGLEN 156

#define ESC '\033'
#define CSI "\033["
/* #define CUP(row, col) CSI row ";" col "H" */
/* #define CUP0 CSI "H" */
/* #define EL_ENTIRE CSI "2K" */
#define ED_ENTIRE CSI "2J"
#define ALT_ENA CSI "?1049h"
#define ALT_DIS CSI "?1049l"

typedef struct room_s {
    int id;
    struct room_s *u;
    struct room_s *d;
    struct room_s *l;
    struct room_s *r;
    struct room_s *c;
    struct room_s *f;
} room;

typedef struct gridcell_s {
    int x;
    int y;
    item *item;
    char *cg;
    int solid;
} gridcell;

/*
 *    [ ]
 * [ ][0][ ]
 *    [ ]
 * =========
 *    [1]
 * [2][3][4]
 *    [5]
 * =========
 *    [ ]
 * [ ][6][7]
 *    [ ]
 */
room map[] = {
    {.id = 0, .f = &map[3]},
    {.id = 1, .d = &map[3]},
    {.id = 2, .r = &map[3]},
    {.id = 3,
     .u = &map[1],
     .d = &map[5],
     .l = &map[2],
     .r = &map[4],
     .c = &map[0],
     .f = &map[6]},
    {.id = 4, .l = &map[3]},
    {.id = 5, .u = &map[3]},
    {.id = 6, .r = &map[7], .c = &map[3]},
    {.id = 7, .l = &map[6]},
};

gridcell grid[W * H] = {0};
char cgrid[W * H] = {0};
int in_buf[BUFLEN];
int in_p = 0;

int player_x = W / 2;
int player_y = H / 2;
room *player_room;
int player_items = 0;
uint8_t itemdata[FLAGLEN] = {0};

gridcell *g_pos(int x, int y) { return &grid[x + y * W]; }
char *cg_pos(int x, int y) { return &cgrid[x + y * W]; }

void display() {
    printf(ED_ENTIRE);
    for (int y = 0; y < H; y++) {
        for (int x = 0; x < W; x++) {
            fputc(*cg_pos(x, y), stdout);
        }
        putchar('\n');
    }
    fflush(stdout);
    return;
}

void update_move(gridcell *oldpos, gridcell *newpos) {
    if (oldpos) {
        *oldpos->cg = ' ';
    }
    *g_pos(LADDER_C_X, LADDER_C_Y)->cg = player_room->c ? '#' : ' ';
    *g_pos(LADDER_F_X, LADDER_F_Y)->cg = player_room->f ? '#' : ' ';
    *newpos->cg = '@';
    item *i = newpos->item;
    if (i) {
        for (int j = 0; j < flaglen - i->offset && j < sizeof(i->data); j++) {
            if (j + i->offset >= 0) {
                itemdata[j + i->offset] ^= i->data[j];
            }
        }
        player_items++;
        sprintf(cg_pos(WALL_R - 15, WALL_D + 2), "G: %d", player_items);
        newpos->item->rid = -1;
        newpos->item = NULL;
    }
    player_x = newpos->x;
    player_y = newpos->y;
    sprintf(cg_pos(WALL_L + 2, WALL_D + 2), "X: %d", player_x);
    sprintf(cg_pos(WALL_L + 14, WALL_D + 2), "Y: %d", player_y);
}

// from adjusts player's position in room
void update_room(room *r, char from) {
    if (!r)
        return;

    for (int y = WALL_U + 1; y < WALL_D; y++) {
        gridcell *lw = g_pos(WALL_L, y);
        gridcell *rw = g_pos(WALL_R, y);
        lw->solid = 1;
        *lw->cg = ']';
        if (r->l && y > DOOR_U && y < DOOR_D) {
            lw->solid = 0;
            *lw->cg = ' ';
        }

        rw->solid = 1;
        *rw->cg = '[';
        if (r->r && y > DOOR_U && y < DOOR_D) {
            rw->solid = 0;
            *rw->cg = ' ';
        }
    }

    for (int x = WALL_L; x <= WALL_R; x++) {
        gridcell *uw = g_pos(x, WALL_U);
        gridcell *dw = g_pos(x, WALL_D);
        uw->solid = 1;
        *uw->cg = '=';
        if (r->u && x > DOOR_L && x < DOOR_R) {
            uw->solid = 0;
            *uw->cg = ' ';
        }

        dw->solid = 1;
        *dw->cg = '=';
        if (r->d && x > DOOR_L && x < DOOR_R) {
            dw->solid = 0;
            *dw->cg = ' ';
        }
    }

    for (int j = 0; j < item_total; j++) {
        item *i = &items[j];
        if (player_room && i->rid == player_room->id &&
            (i->x >= ITEM_L && i->x < ITEM_R) &&
            (i->y >= ITEM_U && i->y < ITEM_D)) {
            g_pos(i->x, i->y)->item = NULL;
            *g_pos(i->x, i->y)->cg = ' ';
        }
        if (i->rid == r->id && (i->x >= ITEM_L && i->x < ITEM_R) &&
            (i->y >= ITEM_U && i->y < ITEM_D)) {
            g_pos(i->x, i->y)->item = i;
            *g_pos(i->x, i->y)->cg = 'O';
        }
    }

    player_room = r;

    int newx = player_x;
    int newy = player_y;
    switch (from) {
    case 'l':
        newx = WALL_L + 1;
        break;
    case 'r':
        newx = WALL_R - 1;
        break;
    case 'u':
        newy = WALL_U + 1;
        break;
    case 'd':
        newy = WALL_D - 1;
        break;
    case 'f':
        newx = LADDER_F_X;
        newy = LADDER_F_Y;
        break;
    case 'c':
        newx = LADDER_C_X;
        newy = LADDER_C_Y;
        break;
    default:
        break;
    }
    update_move(g_pos(player_x, player_y), g_pos(newx, newy));
}

void init_grid() {
    for (int y = 0; y < H; y++) {
        for (int x = 0; x < W; x++) {
            gridcell *cell = g_pos(x, y);
            cell->x = x;
            cell->y = y;
            cell->cg = cg_pos(x, y);
            *cell->cg = ' ';
        }
    }
}

int bufcmp(char *cmd) {
    int p = in_p;
    for (int i = strlen(cmd) - 1; i >= 0; i--) {
        if (cmd[i] != in_buf[p]) {
            return 1;
        }
        p = p == 0 ? BUFLEN - 1 : p - 1;
    }
    return 0;
}

int main(void) {
    FILE *log = fopen("log.txt", "a");
    setvbuf(stdout, NULL, _IOFBF, 0);
    printf(ALT_ENA);
    fflush(stdout);

    static struct termios oldt, newt;
    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;
    newt.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);

    init_grid();
    update_room(&map[3], 0);
    display();

    while (1) {
        in_buf[in_p] = getchar();

        int oldx = player_x;
        int oldy = player_y;

        int newx = player_x;
        int newy = player_y;

        if (in_buf[in_p] == 'q') {
            break;
        } else if (in_buf[in_p] == 'w') {
            newy--;
        } else if (in_buf[in_p] == 'a') {
            newx--;
        } else if (in_buf[in_p] == 's') {
            newy++;
        } else if (in_buf[in_p] == 'd') {
            newx++;
        }

        gridcell *tp = g_pos(newx, newy);

        if (tp->solid) {
            // do nothing
        } else if (tp->x <= WALL_L) {
            update_room(player_room->l, 'r');
        } else if (tp->x >= WALL_R) {
            update_room(player_room->r, 'l');
        } else if (tp->y <= WALL_U) {
            update_room(player_room->u, 'd');
        } else if (tp->y >= WALL_D) {
            update_room(player_room->d, 'u');
        } else if (player_room->c && !bufcmp("climb") &&
                   player_x == LADDER_C_X && player_y == LADDER_C_Y) {
            update_room(player_room->c, 'f');
        } else if (player_room->f && !bufcmp("climb") &&
                   player_x == LADDER_F_X && player_y == LADDER_F_Y) {
            update_room(player_room->f, 'c');
        } else {
            update_move(g_pos(player_x, player_y), g_pos(newx, newy));
        }

        in_p = (in_p + 1) % BUFLEN;

        display();

        if (player_items == item_req) {
            break;
        }
    }

    if (player_items == item_req) {
        memcpy(cg_pos(WALL_L + MARGIN + MARGIN, DOOR_U + 1), itemdata, 62);
        memcpy(cg_pos(WALL_L + MARGIN + MARGIN, DOOR_U + 2), itemdata + 62, 54);
        memcpy(cg_pos(WALL_L + MARGIN + MARGIN, DOOR_U + 3), itemdata + 116, 40);

        while (1) {
            memcpy(cg_pos(WALL_L + MARGIN + MARGIN, DOOR_U + 5), "Type 'q' to quit", 16);
            if (getchar() == 'q') {
                break;
            }
            display();

        }
    }


    printf(ALT_DIS);
    tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
    return 0;
}
