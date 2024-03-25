#include "../inc/rbt.h"

void rbt_transplant(rbt* obj, node* u, node* v){
        if(u->parent == obj->NIL){
                obj->root = v;
        }
        else if(u == u->parent->left){
                u->parent->left = v;
        }
        else{
                u->parent->right = v;

        }
        v->parent = u->parent;
}

void tree_free(node* x){
        if(x){
                if(x->left){
                        tree_free(x->left);
                        free(x->left);
                        x->left = 0;
                }
                if(x->right){
                        tree_free(x->right);
                        free(x->right);
                        x->right = 0;
                }
        }
}

node *tree_minimum_recursion(rbt* obj,node *r)
{
        if(!r){
                return obj->NIL;
        }
        if(r->left != obj->NIL){
                return tree_minimum_recursion(obj,r->left);
        }
        if(r->right != obj->NIL){
                return tree_minimum_recursion(obj,r->right);
        }
        return r;
}

rbt* rbt_new(){
        rbt* tmp = (rbt*)malloc(sizeof(rbt));
        
        if(tmp){
                tmp->insert = rbt_insert;
                tmp->delete = rbt_delete;
                tmp->left_rotate = rbt_left_rotate;
                tmp->right_rotate = rbt_right_rotate;
        
                tmp->NIL = (node*)malloc(sizeof(node));
                tmp->root = NULL;

                if(tmp->NIL){
                        tmp->NIL->color = BLACK;
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
        while(insert_node->parent->color == RED){
                if(insert_node->parent == insert_node->parent->parent->left){
                        tmp = insert_node->parent->parent->right;
                        if(tmp->color == RED){
                                tmp->color = BLACK;
                                insert_node->color = BLACK;
                                tmp->parent->color = RED;
                                insert_node = insert_node->parent->parent;
                        }
                        else if(insert_node == insert_node->parent->right){
                                insert_node = insert_node->parent;
                                obj->left_rotate(obj, insert_node);
                        }
                        insert_node->parent->color = BLACK;
                        insert_node->parent->parent->color = RED;
                        obj->right_rotate(obj, insert_node->parent->parent);
                }
                else{
                        tmp = insert_node->parent->parent->left;
                        if(tmp->color == RED){
                                tmp->color = BLACK;
                                insert_node->parent->color = BLACK;
                                insert_node->parent->parent->color = RED;
                                insert_node = insert_node->parent->parent;
                        }
                        else if(insert_node == insert_node->parent->left){
                                insert_node = insert_node->parent;
                                obj->right_rotate(obj, insert_node);
                        }
                        insert_node->parent->color = BLACK;
                        insert_node->parent->parent->color = RED;
                        obj->left_rotate(obj, insert_node->parent->parent);
                }
        }
        obj->root->color = BLACK;
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
        insert_node->color = RED;
        rbt_insert_fixup(obj, insert_node);
}

void rbt_delete_fixup(rbt* obj, node* x){
        node* w;
        while (x != obj->root && x->color == BLACK)
        {
                if(x == x->parent->left){
                        w = x->parent->right;
                        if(w->color == RED){
                                w->color = BLACK;
                                x->parent->color = RED;
                                rbt_left_rotate(obj, x->parent);
                                w = x->parent->right;
                        }
                        if(w->left->color == BLACK && w->right->color == BLACK){
                                w->color  = RED;
                                x = x->parent;
                        }
                        else if(w->right->color == BLACK){
                                w->left->color = BLACK;
                                w->color = RED;
                                rbt_right_rotate(obj, w);
                                w = w->parent->right;
                        }
                        w->color = x->parent->color;
                        x->parent->color = BLACK;
                        w->right->color = BLACK;
                        rbt_left_rotate(obj,x->parent);
                        x = obj->root;
                }
                else{
                        w = x->parent->left;
                        if(w->color == RED){
                                w->color = BLACK;
                                w->parent->color = RED;
                                rbt_right_rotate(obj, x->parent);
                                w = x->parent->left;
                        }
                        if(w->left->color == BLACK && w->right->color == BLACK){
                                w->color = RED;
                                x = x->parent;
                        }
                        else if(w->left->color == BLACK){
                                w->right->color = BLACK;
                                w->color = RED;
                                rbt_left_rotate(obj, w);
                                w = w->parent->right;
                        }
                        w->color = x->parent->color;
                        w->left->color = BLACK;
                        x->parent->color = BLACK;
                        rbt_right_rotate(obj, x->parent);
                        x = obj->root;
                }
        }
        
}

void rbt_delete(rbt* obj, node* z){
        node *y = z, *x;
        char init_color = y->color;
        if(z->left == obj->NIL){
                x = z->right;
                rbt_transplant(obj, z, z->right);
        }
        else if(z->right == obj->NIL){
                x = z->left;
                rbt_transplant(obj, z, z->left);
        }
        else{
                y = tree_minimum_recursion(obj, z->right);
                init_color = y->color;
                x = y->right;
                if(y->parent == z){
                        x->parent = y;
                }
                else{
                        rbt_transplant(obj, y, y->right);
                        y->right = z->right;
                        y->right->parent = y;
                }
                rbt_transplant(obj, z, y);
                y->left = z->left;
                y->left->parent = y;
                y->color = z->color;
                if(init_color == BLACK){
                        rbt_delete_fixup(obj, x);
                }
        }
}

void rbt_free(rbt* obj){
        if(obj->root){
                if(obj->root->left){
                        tree_free(obj->root->left);
                        free(obj->root->left);
                        obj->root->left = 0;
                }
                if(obj->root->right){
                        tree_free(obj->root->right);
                        free(obj->root->right);
                        obj->root->right = 0;
                }
                free(obj->root);
                free(obj->NIL);
        }
}

