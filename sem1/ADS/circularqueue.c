#include<stdio.h>
#include<stdlib.h>
int a[10],front=-1,rear=-1,n;
void insert();
void display();
void del();
void search();
int main()
 {
  int ch;
  printf("Enter the size of queue:\n");
  scanf("%d",&n);
  while(1)
   {
    printf("\n1.Insertion\n");
    printf("2.Deletion\n");
    printf("3.Display\n");
    printf("4.Search\n");
    printf("5.Exit\n");
    printf("Enter your choice:\n");
    scanf("%d",&ch);
    switch(ch)
      {
        case 1:
        insert();
        break;
        case 2:
        del();
        break;
        case 3:
        display();
        break;
        case 4:
        search();
        break;
        case 5:
        printf("Press any key to exit\n");
        exit(0);
        default:
        printf("Invalid choice\n");
      }
   }
return 0;
}
void insert()
 {
  int x;
  if((front==0 && rear==n-1)||(front==rear+1))
     {
       printf("Queue is full");
     }
  else
     {
       printf("Enter the element to insert:");
       scanf("%d",&x);
        if(front==-1 && rear==-1)
           front=rear=0;
        else if(rear==n-1 && front!=0)
           rear=0;
        else
            rear=(rear+1)%n;
            a[rear]=x;
     }
}
void display()
{
 int i;
 printf("Front=%d\nRear=%d\n",front,rear);
 if(front==-1)
    printf("\nQueue is empty\n");
 else if(front<=rear)
   {
     for(i=front;i<=rear;i++)
         printf("%d ",a[i]);
   }
 else
   {
    for(i=front;i<n;i++)
        printf("%d ",a[i]);
    for(i=0;i<=rear;i++)
        printf("%d ",a[i]);
   }
}
void del()
{
  if(front==-1)
    printf("Queue is empty\n");
  else 
    {
      printf("Deleted element:%d",a[front]);
      if(front==rear)
         front=rear=-1;
       else
          {
             if(front==n-1)
                front=0;
             else
                front+=1;
          }
     }
}
void search()
 {
  int x,i,j;
  printf("Enter the element to search:");
  scanf("%d",&x);
  if(front<=rear)
     {
       int f1=0;
       for(i=front;i<=rear;i++)
           {
             if(a[i]==x)
                {
                printf("Element found at position %d",i);
                f1=1;
                break;
                }
           }
           if(f1==0)
             printf("Element not found");
     }
   else
     {
      int f=0;
      for(i=front,j=1;i<n;i++,j++)
         {
          if(a[i]==x)
            {
             f=1;
             printf("Element found at position %d",j);
             break;
            }
          }
      if(f==0)
       {
        int f2=0;
        for(i=0;i<=rear;i++)
         {
          if(a[i]==x)
            {
              printf("Element found at position %d",i+n-1);
              f2=1;
              break;
            }
          }
          if(f2==0)
             printf("Element not found");
         }
      }
}

