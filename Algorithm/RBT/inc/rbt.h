#ifndef RBT
#define RBT

#include<stdlib.h>

typedef struct node node;
typedef struct rbt rbt;

void rbt_left_rotate(rbt* obj, node*);
void rbt_right_rotate(rbt* obj, node*);
void rbt_insert_fixup(rbt* obj,node* insert_node);
void rbt_insert(rbt* obj, node* insert_node);
rbt* rbt_new();
rbt* rbt_free();

typedef struct node
{
        struct node* parent;
        struct node* left;
        struct node* right;

        int data;
        char color;
}node;

typedef struct rbt
{
        struct node* root;
        struct node* NIL;

        void (*insert)(rbt* obj, node* insert_node); // Function pointer for insertion
        void (*insert_fixup)(rbt* obj, node* insert_node); // Function pointer for insertion fixup
        void (*left_rotate)(rbt* obj, node* node); // Function pointer for left rotation
        void (*right_rotate)(rbt* obj, node* node);
}rbt;

#endif
