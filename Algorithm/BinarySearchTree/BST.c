#include "BST.h"

node *tree_minimum_recursion(node *root)
{
/*******************************
 * Find the min value of a binary tree ergodded using inorder traversal
 * Parameters:
 *       node* root: pointer that points to binary search tree 
 * Return:
 *       node*: address of minimum node 
*******************************/
        if(!root){
                return NULL;
        }
        if(root->left){
                return tree_minimum_recursion(root->left);
        }
        if(root->right){
                return tree_minimum_recursion(root->right);
        }
        return root;
}

node *tree_maximum_recursion(node *root)
{
/*******************************
 * Find the max value of a binary tree ergodded using inorder traversal
 * Parameters:
 *       node* root: pointer that points to binary search tree 
 * Return:
 *       node*: address of minimum node 
*******************************/
        if(!root){
                return NULL;
        }
        if(root->right){
                return tree_maximum_recursion(root->right);
        }
        if(root->left){
                return tree_maximum_recursion(root->left);
        }
        return root;
}

node *tree_predecessor(node *root){
/**************************************************
 * Find the predecesser of a binary search tree node ergodded using inorder traversal
 * Paramerents: 
 *      root: root of a subtree
 * Return:
 *      the predecessor of root under the order of inorder traversal 
**************************************************/
        node* tmp;
        if(!root){
                return NULL;
        }
        if(root->left){
                return tree_maximum_recursion(root->left);
        }
        else{
                tmp = root->pare;
                while(tmp && tmp->left == root){
                        root = tmp;
                        tmp = tmp->pare;
                }
                return tmp;
        }
}
