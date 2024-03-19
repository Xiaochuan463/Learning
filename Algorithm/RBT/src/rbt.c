#include "../inc/rbt.h"

rbt* rbt_new(){
        rbt* tmp = (rbt*)malloc(sizeof(rbt));
        
        if(tmp){
                tmp->insert = rbt_insert;
                tmp->insert_fixup = rbt_insert_fixup;
                tmp->left_rotate = rbt_left_rotate;
                tmp->right_rotate = rbt_right_rotate;
        
                tmp->NIL = (node*)malloc(sizeof(node));
                tmp->root = NULL;

                if(tmp->NIL){
                        tmp->NIL->color = 'b';
                        tmp->NIL->left = NULL;
                        tmp->NIL->right = NULL;
                        tmp->NIL->parent = NULL;
                }
                else{
                        free(tmp);
                }
        }
        return tmp;
}

void rbt_left_rotate(rbt* obj, node* x){
        node* y;
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

void rbt_right_rotate(rbt* obj,node* x){
        node* y;
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

void rbt_insert_fixup(rbt* obj, node* insert_node){
        node* tmp;
        while(insert_node->parent->color == 'r'){
                if(insert_node->parent == insert_node->parent->parent->left){
                        tmp = insert_node->parent->parent->right;
                        if(tmp->color == 'r'){
                                tmp->color = 'b';
                                insert_node->color = 'b';
                                tmp->parent->color = 'r';
                                insert_node = insert_node->parent->parent;
                        }
                        else if(insert_node == insert_node->parent->right){
                                insert_node = insert_node->parent;
                                obj->left_rotate(obj, insert_node);
                        }
                        insert_node->parent->color = 'b';
                        insert_node->parent->parent = 'r';
                        obj->right_rotate(obj, insert_node->parent->parent);
                }
                else{
                        tmp = insert_node->parent->parent->left;
                        if(tmp->color == 'r'){
                                tmp->color = 'b';
                                insert_node->parent->color = 'b';
                                insert_node->parent->parent->color = 'r';
                                insert_node = insert_node->parent->parent;
                        }
                        else if(insert_node == insert_node->parent->left){
                                insert_node = insert_node->parent;
                                obj->right_rotate(obj, insert_node);
                        }
                        insert_node->parent->color = 'b';
                        insert_node->parent->parent->color = 'r';
                        obj->left_rotate(obj, insert_node->parent->parent);
                }
        }
        obj->root->color = 'b';
}

void rbt_insert(rbt* obj,node* insert_node){
        node* x = obj->root, *y = obj->NIL;
        if(!x){
                obj->root = insert_node;
                obj->root->parent = obj->NIL;
        }
        else{
                while (x != obj->NIL)
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
        }
        insert_node->left = obj->NIL;
        insert_node->right = obj->NIL;
        insert_node->color = 'r';
        rbt_insert_fixup(obj, insert_node);
}