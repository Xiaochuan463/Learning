#include<stdio.h>
#include<stdlib.h>

/****************
 * trans subtree u as v, and u's parents become v's; v becomes child of
 *      u's parents.
 * Overall, u is replaced with v;
 * 
 * Parameter:
 *      root: root of bst
 *      u: the node want to be replaced
 *      v: the node to replace u;
****************/
#ifndef BST
        #ifndef NULL
        #define NULL 0
        #endif
#define TRANSPLANT(root, u, v) \
        do{\
        if(!u->pare){\
                root = v;\
        }\
        else if(u == u->pare->left){\
                u->pare->left = v;\
        }\
        else{\
                u->pare->right = v;\
        }\
        if(v){\
                v->pare = u->pare;\
        }\
        }while(0);

struct node;
typedef struct node
{
        struct node *left;
        struct node *right;
        struct node *pare;
        int data;
} node;



/*******************************
 * Find the min value of a binary tree ergodded using inorder traversal
 * 
 * Parameters:
 *       node* r: pointer that points to binary search tree root
 * Return:
 *       node*: address of minimum node 
*******************************/
node* tree_minimum_recursion(node* r);

/*******************************
 * Find the max value of a binary tree ergodded using inorder traversal
 * Parameters:
 *       node* r: pointer that points to binary search tree root
 * Return:
 *       node*: address of minimum node 
*******************************/
node* tree_maximum_recursion(node* r);

/**************************************************
 * Find the predecesser of a binary search tree node ergodded using inorder traversal
 * 
 * Paramerents: 
 *      r: root of a subtree
 * Return:
 *      the predecessor of r under the order of inorder traversal 
**************************************************/
node *tree_predecessor(node *r);

/********************************************
 * insert a node into a binary search tree
 * 
 * Parameters:
 *      root: root of a tree
 *      n: the node want to insert
 * Returns:
 *      -1 to sign empty tree
 *      0 to sign succeed.
********************************************/
signed char tree_insert(node* root, node* n);

/********************************************
 * recursion version of tree_insert
 * 
 * Parameters:
 *      root: root of a tree root pointer's address
 *      n: the node want to insert
 * Returns:
 *      -1 to sign empty node pointer n
 *      0 to sign succeed.
********************************************/
signed char tree_insert_recursion(node** root, node* n);

/*******************************************
 * Delete a node in binary search tree
 * 
 * Parameters:
 *      root: root of bst
 *      n: node want to delete
*******************************************/
signed char tree_delete(node* root, node* n);

/*******************************************
 * Delete a node in binary search tree, but use predecesser
 * 
 * Parameters:
 *      root: root of bst
 *      n: node want to delete
*******************************************/
signed char tree_delete_use_predecesser(node* root, node* n);

/*******************************************
 * Inorder tranversal
 * 
 * Parameters: 
 *      root: root of tree or subtree
 * Return:
 *      void
*******************************************/
void inorder_tranversal(node* root);

/******************************************
 * free a tree after used
 * 
 * Parameters:
 *      root : root of tree or subtree
 * Return: 
 *      void
******************************************/
void tree_free(node** root);

/*******************************************
 * BST_sort: sort using bst
 * 
 * Parameters: 
 *      arr: array want to sort
 *      length: length of the array
 * Return:
 *      situation of sorting
*******************************************/
signed char BST_sort(int* arr, int length);
#endif