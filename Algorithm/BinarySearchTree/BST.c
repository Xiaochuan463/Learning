#include "BST.h"

node *tree_minimum_recursion(node *r)
{
        if(!r){
                return NULL;
        }
        if(r->left){
                return tree_minimum_recursion(r->left);
        }
        if(r->right){
                return tree_minimum_recursion(r->right);
        }
        return r;
}

node *tree_maximum_recursion(node *r)
{
        if(!r){
                return NULL;
        }
        if(r->right){
                return tree_maximum_recursion(r->right);
        }
        if(r->left){
                return tree_maximum_recursion(r->left);
        }
        return r;
}

node *tree_predecessor(node *r){
        node* tmp;
        if(!r){
                return NULL;
        }
        if(r->left){
                return tree_maximum_recursion(r->left);
        }
        else{
                tmp = r->pare;
                while(tmp && tmp->left == r){
                        r = tmp;
                        tmp = tmp->pare;
                }
                return tmp;
        }
}

int8 tree_insert(node*root, node* n){
        node* tmp = NULL;
        node* x = root;
        while(x){
                tmp = x;
                if(n->data > tmp->data){
                        x = x->right;
                }
                else{
                        x = x->left;
                }
        }
        n->pare = tmp;
        if(!tmp){
                return -1;
        }
        else if(n->data < tmp->data){
                tmp->left = n;
        }
        else{
                tmp->right = n;
        }
        return 0;
}

int8 tree_insert_recursion(node** root, node* n){
        if(!*root){
                *root = n;
        }
        if(!n){
                return -1;
        }
        if(n->data < (*root)->data){
                if((*root)->left){
                        return tree_insert_recursion(&((*root)->left), n);
                }
                else{
                        (*root)->left = n;
                        return 0;
                }
        }
        else{
                if((*root)->right){
                        return tree_insert_recursion(&((*root)->right), n);
                }
                else{
                        (*root)->right = n;
                        return 0;
                }
        }
}

int8 tree_delete(node* root, node* n){
        node* tmp;
        if(!n->left){
                TRANSPLANT(root, n, n->right);
        }
        else if(!n->right){
                TRANSPLANT(root, n, n->left);
        }
        else{
                tmp = tree_minimum_recursion(n->right);
                if(tmp->pare != n){
                        TRANSPLANT(root, tmp, tmp->right);
                        tmp->right = n->right;
                        tmp->right->pare = tmp;
                }
                TRANSPLANT(root, n, tmp);
                tmp->left = n->left;
                tmp->left->pare = tmp;
        }
        free(n);
        return 0;
}
