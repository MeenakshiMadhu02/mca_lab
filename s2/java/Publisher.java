import java.util.*;
public class Publisher {
      String pub_name;
      
      public Publisher(String pub) {
    	  pub_name = pub;
      }
     static class Book extends Publisher{
    	 String Title, Author;
    	 
    	 public Book(String pub, String title, String author) {
    		 super(pub);
    		 
    		 Title = title;
    		 Author = author;
    		
    	 }
     }    
     static class Literature extends Book{
    	  
    	 public Literature(String pub, String title, String author) {
    		 super(pub, title, author);
    	 }
    	 
    	 
    	 void Display() {
    		 System.out.println("\nTitle:"+Title);
    		 System.out.println("Author:"+Author);
    		 System.out.println("Publisher:"+pub_name);   		 
    	 }
     }     
     static class Fiction extends Book{
   	  
    	 public Fiction(String pub, String title, String author) {
    		 super(pub, title, author);
    	 }
    	  	 
    	 void Display() {
    		 System.out.println("\nTitle:"+Title);
    		 System.out.println("Author:"+Author);
    		 System.out.println("Publisher:"+pub_name);
    	 }
     }
	
	public static void main(String[] args) {
		
		Scanner l = new Scanner(System.in);
		
		Scanner sc = new Scanner(System.in);
		int i, N, n;
		String p, t, a;
		char genre;
		System.out.println("Enter the number of Literature records to be stored:");
        N = l.nextInt();
        
        Literature L[] = new Literature[N];
        
        for( i=0; i<N; i++)
		{
        	System.out.println("\nRecord No:"+(i+1));
        	System.out.println("Enter the Book title:");
            t = l.next();
            
            System.out.println("Enter the Author:");
            a = l.next();
        	
		    System.out.println("Enter the Publisher Name:");
            p = l.next();
        
           
            L[i] = new Literature(p,t,a);
        
		}
   Scanner f = new Scanner(System.in);
    	
		System.out.println("\nEnter the number of Fiction records to be stored:");
        n = f.nextInt();
        
        Fiction  F[] = new Fiction[n];
        
        for( i=0; i<n; i++)
		{
		  
        	System.out.println("\nRecord No:"+(i+1));
        	System.out.println("Enter the Book title:");
            t = f.next();
            
            System.out.println("Enter the Author:");
            a = f.next();
            
		    System.out.println("Enter the Publisher Name:");
            p = f.next();
        
           F[i] = new Fiction(p,t,a);
		

      	}
        
        System.out.println("\nSelect the Genre(L/F):\nL - Literature\nF - Fiction");
        genre = sc.next().charAt(0);
        
        if(genre=='L' || genre=='l')
        {
        	System.out.println("\n______LITERATURE BOOKS_____");
          	
		 for( i=0; i<N; i++)
		    {
			 System.out.println("\nBook No:"+(i+1));
			   L[i].Display();
		    }
        }
        
        else if(genre=='F' || genre=='f')
        {
        	System.out.println("\n______FICTION BOOKS_____");
         	
		for( i=0; i<n; i++)
	        {
			System.out.println("\nBook No:"+(i+1));
			   F[i].Display();
		    }
        }
		
	}      
        
}
