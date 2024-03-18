#include "../inc/rbt.h"

void rbt_left_rotate(rbt_node* x){
        rbt_node* y;
        if(!x || !x->right){
                return;
        }
        y = x->right;
        
        y->parent = x->parent;
        x->parent = y;
        if(y->left){
                y->left->parent = x;
        }
        x->right = y->left;
        y->left = x;
}

void rbt_right_rotate(rbt_node* x){
        rbt_node* y;
        if(!x || !x->left){
                return;
        }
        y = x->left;
        y->parent = x->parent;
        x->parent = y;
        if(y->right){
                y->right->parent = x;
        }
        x->left = y->right;
        y->right = x;
}

void rbt_insert_fixup(rbt_node* root, rbt_node* insert_node){

}

void rbt_insert(rbt_node* root, rbt_node* insert_node){
        rbt_node* x = root, *y = 0;
        while (x)
        {
                y = x;
                if(x->data > insert_node->data){
                        x = x->left;
                }
                else{
                        x = x->right;
                }
        }
        insert_node->parent = y;
        if(y->data > insert_node->data){
                y->left = insert_node;
        }
        else{
                y->right = insert_node;
        }
        insert_node->left = 0;
        insert_node->right = 0;
        insert_node->color = 0;
        rbt_insert_fixup(root, insert_node);
}