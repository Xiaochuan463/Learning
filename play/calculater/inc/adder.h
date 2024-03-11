

#ifndef ADDER
#define ADDER
typedef struct string
{
    char* ch;
    unsigned int len;
};
/*
 *use a, b, cin get s, cout
*/
void adder(char* a, char* b, char* s, char* cin, char* cout);

/*
 *add b to a;
*/
void add(string a, string b);

#endif