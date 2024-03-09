#include "../inc/BST.h"

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

signed char tree_insert(node*root, node* n){
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

signed char tree_insert_recursion(node** root, node* n){
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

signed char tree_delete(node* root, node* n){
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

signed char tree_delete_use_predecesser(node* root, node* n){
        node* tmp;
        if(!n->left){
                TRANSPLANT(root, n, n->right);
        }
        else if(!n->right){
                TRANSPLANT(root, n, n->left);
        }
        else{
                tmp = tree_predecessor(n);
                if(tmp == n->left){
                        TRANSPLANT(root, n, tmp);
                        tmp->right = n->right;
                }
                else{
                TRANSPLANT(root, n, tmp);
                tmp->left = n->left;
                tmp->right = n->right;
                }
        }
        free(n);
        return 0;
}

void inorder_tranversal(node* root){
        if(!root){
                return;
        }
        inorder_tranversal(root->left);
        printf("%d ", root->data);
        inorder_tranversal(root->right);
}

void tree_free(node** root){
        if(!(*root)){
                return;
        }
        if((*root)->left){
                tree_free(&((*root)->left));
        }
        if((*root)->right){
                tree_free(&((*root)->right));
        }
        free(*root);
        *root = 0;
        return;
}

signed char BST_sort(int* arr, int length){
        int i = 0;
        node Root;
        node *root = &Root; 
        node *tmp = 0;
        root->left = 0;
        root->right = 0;
        root->data = arr[i];
        for(i = 1; i < length; i++){
                printf("ready to insert!\n");
                tmp = (node*)malloc(sizeof(node));
                if(!tmp){
                        return -1;
                }
                tmp->data = arr[i];
                tmp->left = 0;
                tmp->right = 0;
                tmp->pare = 0;
                tree_insert(root, tmp);
                printf("insert!\n");
        }
        inorder_tranversal(root);
        printf("\nready to free memory!\n");
        tree_free(&root);
        printf("freed!\n");
        return 0;
}