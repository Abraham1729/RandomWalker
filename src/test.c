#include <stdlib.h>
#include <stdio.h>
#include <sys/resource.h>

int main() {
    printf("Size of double*:\t%d\nSize of int*:\t%d\n",sizeof(double*),sizeof(int*));
    return 0;
}