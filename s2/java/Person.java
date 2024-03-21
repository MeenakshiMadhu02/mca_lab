import java.util.*;

public class Person {
	String Name, Gender, Address;
	int Age;
	
	public Person(String n, String g, String ad, int age){
		Name = n;
		Gender = g;
		Address = ad;
		Age = age;
	}

	static class Employee extends Person{
	     int Emp_id;
	     String Co_name, Qualification;
	     float Salary;
	     
	     public Employee(String n, String g, String ad, int age, int e_id, String c_name, String qualif, float sal) {
	    	 super(n, g, ad, age);
	    	 
	    	 Emp_id = e_id;
	    	 Co_name = c_name;
	    	 Qualification = qualif;
	    	 Salary = sal;
	     }
}	     
	static class Teacher extends Employee{
	     int teach_id;
	     String Subject, Department;
	  
	     public Teacher(String n, String g, String ad, int age, int e_id, String c_name, String qualif, float sal, int t_id, String sub, String dept) {
	    	 super(n, g, ad, age, e_id, c_name, qualif, sal);
		  
	    	 teach_id = t_id;
	    	 Subject = sub;
	    	 Department = dept;
		 }
	  
	  
	      void Display() {
			System.out.println("\nName: "+Name);
			System.out.println("Gender: "+Gender);
			System.out.println("Address: "+Address);
			System.out.println("Age: "+Age);
			System.out.println("Employee_Id "+Emp_id);
			System.out.println("Company Name "+Co_name);
			System.out.println("Qualification: "+Qualification);
			System.out.println("Salary: "+Salary);
			System.out.println("Teacher_Id: "+teach_id);
			System.out.println("Subject: "+Subject);
			System.out.println("Department: "+Department);
			
	    }
 
  }		

	public static void main(String[] args) {
		
		Scanner sc = new Scanner(System.in);
		int N, age, e_id, t_id,i;
		float sal;
		String nam,gen,adr,cname,qual,dep,sub;
		
		System.out.println("Enter the number of records to be stored:");
        N = sc.nextInt();
        
        Teacher[] t = new Teacher[N];
        
        for( i=0; i<N; i++)
		{
		
		System.out.println("Enter the Name:");
        nam= sc.next();
        
        System.out.println("Enter the Gender:");
        gen= sc.next();
        
        System.out.println("Enter the address:");
        adr= sc.next();
        
        System.out.println("Enter the Age:");
        age= sc.nextInt();
        
        System.out.println("Enter the Employee ID:");
        e_id= sc.nextInt();
        
        System.out.println("Enter the Company Name:");
        cname= sc.next();
        
        System.out.println("Enter the Qualification:");
        qual= sc.next();
        
        System.out.println("Enter the Salary:");
        sal= sc.nextFloat();
        
        System.out.println("Enter the Teacher ID:");
        t_id= sc.nextInt();
        
        System.out.println("Enter the Department:");
        dep= sc.next();
        
        System.out.println("Enter the Subject:");
        sub= sc.next();
        
        t[i] = new Teacher(nam,gen,adr,age,e_id,cname,qual,sal,t_id,sub,dep);
	  }
       
      System.out.println("\n______EMPLOYEE DETAILS_____");
		for( i=0; i<N; i++)
	        {
			   t[i].Display();
		    }
		
   }
	
 }

