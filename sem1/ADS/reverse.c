#include<stdio.h>
void main()
{
int n,m;
printf("enter the number:");
scanf("%d",&n);
while(n>0)
{
m=n%10;
n=n/10;
printf("%d",m);
}
}
