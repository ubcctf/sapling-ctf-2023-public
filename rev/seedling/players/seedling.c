#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* a linked-list node type for representing strings */
typedef struct cnode_s {
  char c;
  struct cnode_s *next;
} cnode;

/* store your strings in trees */
typedef struct treenode_s {
  char c;
  char c_rotated;
  struct treenode_s *left;
  struct treenode_s *right;
} treenode;

char rotate_char(char c, int n) { return (c - 32 + n) % (127 - 32) + 32; }

cnode *cnode_create(char c) {
  cnode *l = malloc(sizeof(cnode));
  l->c = c;
  return l;
}

void cnodes_delete(cnode *l) {
  if (l) {
    cnodes_delete(l->next);
    free(l);
  }
}

cnode *cnodes_join(cnode *l1, cnode *l2) {
  if (l1 == NULL) {
    return l2;
  }
  l1->next = cnodes_join(l1->next, l2);
  return l1;
}

cnode *cnodes_join3(cnode *l1, cnode *l2, cnode *l3) {
  return cnodes_join(l1, cnodes_join(l2, l3));
}

int cnodes_difference(cnode *l1, cnode *l2) {
  if (l1 == NULL && l2 == NULL) {
    return 0;
  }
  if (l1 == NULL || l2 == NULL) {
    return 1;
  }

  return (l1->c != l2->c) + cnodes_difference(l1->next, l2->next);
}

void cnodes_print(cnode *l) {
  for (cnode *i = l; i != NULL; i = i->next) {
    putchar(i->c);
  }
  putchar('\n');
}

cnode *str_to_cnodes(char *s) {
  if (s[0] == '\0') {
    return NULL;
  }
  cnode *c = cnode_create(s[0]);
  c->next = str_to_cnodes(s + 1);
  return c;
}

treenode *treenode_create(char c, int rot, treenode *l, treenode *r) {
  treenode *tn = malloc(sizeof(treenode));
  tn->c = c;
  tn->c_rotated = rotate_char(c, rot);
  tn->left = l;
  tn->right = r;
  return tn;
}

void treenode_delete(treenode *t) {
  if (t) {
    treenode_delete(t->left);
    treenode_delete(t->right);
    free(t);
  }
}

cnode *treenode_traverse(treenode *t) {
  if (t == NULL) {
    return NULL;
  }
  return cnodes_join3(treenode_traverse(t->left), cnode_create(t->c),
                      treenode_traverse(t->right));
}

cnode *treenode_traverse1(treenode *t) {
  if (t == NULL) {
    return NULL;
  }
  return cnodes_join3(treenode_traverse1(t->left), cnode_create(t->c_rotated),
                      treenode_traverse1(t->right));
}

treenode *str_to_tree(char *str, int len, int level) {
  if (len <= 0) {
    return NULL;
  }
  int mid = len / 2;
  return treenode_create(str[mid], level, str_to_tree(str, mid, level + 1),
                         str_to_tree(str + mid + 1, len - mid - 1, level + 1));
}

char *check_str = "iqexvngduyvzfywdbshdizrhvnssvdjtre~szudzng|msjdtqffwzujcnpdkmlivf";
char input[100] = {0};

int main(int argc, char **argv) {
  cnode *check_cns = str_to_cnodes(check_str);

  puts("Input flag: ");
  putchar('>');
  putchar(' ');
  scanf("%99s", input);
  treenode *input_t = str_to_tree(input, strlen(input), 0);
  cnode *input_cns = treenode_traverse1(input_t);

  if (cnodes_difference(check_cns, input_cns)) {
    puts("Nope\n");
  } else {
    printf("Correct! The flag is: maple{%s}\n", input);
  }

  cnodes_delete(check_cns);
  cnodes_delete(input_cns);
  treenode_delete(input_t);

  return 0;
}