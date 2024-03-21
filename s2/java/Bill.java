import java.util.Scanner;
interface calculate{
void totalbill(int id,String name,float uprice ,int quan);
void display();
}
class Bill implements calculate{
int id;
float unitprice;
int quantity;
String name;
public void totalbill(int id,String name,float uprice,int quan) {
this.id = id;
this.name = name;
this.unitprice = uprice;
this.quantity =quan;
}
public void display()
 {
System.out.println(id+ "\t   \t"+name+ " \t  \t "+quantity+"\t  \t"+ unitprice + "\t  \t"+(quantity*unitprice));
 }
public static void main(String[] args) {
Scanner scan = new Scanner(System.in);
int number;
int id;
String name;
float unitprice;
int  quantity;
float net=0;
System.out.println("enter the number of items : ");
number = scan.nextInt();
Bill[] bill = new Bill[number];
for (int i = 0 ; i < number ; i ++)
{
System.out.print("enter product id : ");
id =scan.nextInt();
System.out.print("enter the name of the product : ");
name= scan.next();
System.out.print("enter the quantity : ");
quantity = scan.nextInt();
System.out.print("enter the unitprice :");
unitprice = scan.nextFloat();
System.out.println("\n");
bill[i] = new Bill();
bill[i].totalbill(id, name, unitprice, quantity);
net = net + (quantity*unitprice);	
}
System.out.println("                               BILL                                           ");
System.out.println("date : 31/05/2021\n");
System.out.println("Product id\t  Product\t Quantity\t unitprice \t total ");
System.out.println("--------------------------------------------------------------------------------");
for(int i=0; i<number; i++) 
{
bill[i].display();
}
System.out.println("--------------------------------------------------------------------------------");		
System.out.println(" NET :\t "+net);
}	
}
