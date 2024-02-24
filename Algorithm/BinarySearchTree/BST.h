#include <stdio.h>
typedef struct
{
        node *left;
        node *right;
        node *pare;
        int data;
} node;

node* tree_minimum_recursion(node* root);

node* tree_maximum_recursion(node* root);

node *tree_predecessor(node *root);

void insert(node* n);

void delete(node* n);