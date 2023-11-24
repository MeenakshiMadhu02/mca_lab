#include<stdio.h>
void main()
{
int a,b,c;
printf("enter 2 numbers:");
scanf("%d%d",&a,&b);
printf("Before swapping\n");
printf("a=%d b=%d",a,b);
c=a;
a=b;
b=c;
printf("After swapping\n");
printf("a=%d b=%d",a,b);
}
