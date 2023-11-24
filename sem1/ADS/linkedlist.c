#include<stdio.h>
#include<stdlib.h>
struct node
{
 int info;
 struct node *link;
};
struct node* start=NULL;
void traverse()
{
  struct node* temp;
  if(start==NULL)
     printf("\nList is empty\n");
  else
     {
      temp=start;
      printf("The list is \n");
      while(temp!=NULL)
         {
           printf("%d-->",temp->info);
           temp=temp->link;
         }
      }
}
void insertAtFront()
{
  int data;
  struct node* temp;
  temp=malloc(sizeof(struct node));
  printf("\nEnter number to be inserted:");
  scanf("%d",&data);
  temp->info=data;
  temp->link=start;
  start=temp;
}
void insertAtEnd()
{
 int data;
 struct node *temp,*head;
 temp=malloc(sizeof(struct node));
 printf("\nEnter the number to be inserted:");
 scanf("%d",&data);
 temp->link=0;
 temp->info=data;
 head=start;
 while(head->link!=NULL)
   {
     head=head->link;
   }
  head->link=temp; 
}
void insertAtPosition()
{
 struct node *temp,*newnode;
 int pos,data,i=1;
 newnode=malloc(sizeof(struct node));
 printf("\nEnter position and data:");
 scanf("%d%d",&pos,&data);
 temp=start;
 newnode->info=data;
 newnode->link=0;
 while(i<pos-1)
 {
  temp=temp->link;
  i++;
 }
newnode->link=temp->link;
temp->link=newnode;
}
void deleteFirst()
{
 struct node *temp;
 if(start==NULL)
  printf("\nList is empty\n");
 else
  {
    temp=start;
    start=start->link;
    free(temp);
  }
}
void deleteEnd()
{
 struct node *temp,*prevnode;
 if(start==NULL)
   printf("\nList is empty\n");
 else
   {
     temp=start;
      while(temp->link!=0)
          {
            prevnode=temp;
            temp=temp->link;
          }
     free(temp);
     prevnode->link=0;
   }
}
void deletePosition()
{
  struct node *temp,*position;
  int i=1,pos;
   if(start==NULL)
     printf("\nList is empty\n");
   else
     {
       printf("\nEnter position:");
       scanf("%d",&pos);
       position=malloc(sizeof(struct node));
       temp=start;
       while(i<pos-1)
         {
          temp=temp->link;
          i++;
         }
        position=temp->link;
        temp->link=position->link;
        free(position);
      }
}
int main()
{
int choice;
while(1)
 {
  printf("\n1.To see list\n");
  printf("2.For insertion at starting\n");
  printf("3.For insertion at end\n");
  printf("4.For insertion at any position\n");
  printf("5.For deletion of first element\n");
  printf("6.For deletion of last element\n");
  printf("7.For deletion of element at any position\n");
  printf("8.To exit\n");
  printf("Enter choice:");
  scanf("%d",&choice);
  switch(choice)
    {
      case 1:
      traverse();
      break;
      case 2:
      insertAtFront();
      break;
      case 3:
      insertAtEnd();
      break;
      case 4:
      insertAtPosition();
      break;
      case 5:
      deleteFirst();
      break;
      case 6:
      deleteEnd();
      break;
      case 7:
      deletePosition();
      break;
      case 8:
      exit(0);
      default:
      printf("Incorrect choice\n");
    }
  }
return 0;
}
