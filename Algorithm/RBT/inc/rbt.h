#ifndef RBT
#define RBT

#include<stdlib.h>

#define RED 'r'
#define BLACK 'b'

typedef struct node node;
typedef struct rbt rbt;

void rbt_left_rotate(rbt* obj, node*);
void rbt_right_rotate(rbt* obj, node*);
void rbt_insert_fixup(rbt* obj,node* insert_node);
void rbt_insert(rbt* obj, node* insert_node);
void rbt_delete(rbt* obj, node* node);
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
        void (*left_rotate)(rbt* obj, node* node); // Function pointer for left rotation
        void (*right_rotate)(rbt* obj, node* node);
        void (*delete)(rbt* obj, node* node);
}rbt;

#endif
