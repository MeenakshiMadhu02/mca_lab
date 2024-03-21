class product{
 int pcode;
 String pname;
 double price;
 }
 class getProduct{
 public static void main(String args[]){
  product p1=new product();
  product p2=new product();
  product p3=new product();
  p1.price=1001;
  p1.pcode=101;
  p1.pname="A";
  p2.price=2000;
  p2.pcode=102;
  p2.pname="B";
  p3.price=1000;
  p3.pcode=103;
  p3.pname="C";
  if(p1.price<p2.price && p1.price<p3.price){
   System.out.println("Product code is "+p1.pcode);
   System.out.println("Product name is "+p1.pname);
   System.out.println("Smallest value is "+p1.price);
   }
   else if(p2.price<p1.price && p2.price<p3.price){
   System.out.println("Product code is "+p2.pcode);
   System.out.println("Product name is "+p2.pname);
   System.out.println("Smallest value is "+p2.price);
   }
   else{
   System.out.println("Product code is "+p3.pcode);
   System.out.println("Product name is "+p3.pname);
   System.out.println("Smallest value is "+p3.price);
   }
 }
}
