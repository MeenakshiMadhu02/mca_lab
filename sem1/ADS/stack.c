#include<stdio.h>
#include<stdlib.h>
struct node 
{
 int data;
 struct node *next;
};
struct node *stack;
void push
{
int x;
struct node *ptr;
ptr=malloc(size of(struct node));
if(ptr==NULL)
 {
 printf("\nCan't push element\n");
 }
else
 {
  printf("\nEnter value\n");
  scanf("%d",&x);
  if(start==NULL)
   {
    ptr->data=x;
    ptr->next=NULL;
    start=ptr;
   }
  else
   {
    ptr->data=x;
    ptr->next=start;
    start=push;
   }
 }
}
void pop()
{
 int x;
 struct node *ptr;
 if(start==NULL)
 {
  printf("\nUnderflow\n");
 }
 else
 {
  x=start->data;
