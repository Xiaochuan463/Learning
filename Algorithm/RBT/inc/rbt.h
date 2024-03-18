#ifndef RBT
#define RBT

typedef struct rbt_node
{
        struct rbt_node* parent;
        struct rbt_node* left;
        struct rbt_node* right;

        int data;
        char color;
}rbt_node;


void rbt_left_rotate(rbt_node*);
void rbt_right_rotate(rbt_node*);
void rbt_insert_fixup(rbt_node* root, rbt_node* insert_node);
void rbt_insert(rbt_node* root, rbt_node* insert_node);
#endif
