#include<stdio.h>
void main()
{
int n,r,sum=0,temp;
printf("enter the number:");
scanf("%d",&n);
temp=n;
while(n>0)
{
r=n%10;
sum=sum+(r*r*r);
n=n/10;
}
if(temp==sum)
printf("Is amstrong number");
else
printf("Is not amstrong number");
}
