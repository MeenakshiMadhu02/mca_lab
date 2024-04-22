import java.io.*;
public class CopyFile {

	public static void main(String[] args) {
		
		try {
			FileReader fr = new FileReader("/home/student/pgm1/file1.txt");
			BufferedReader br = new BufferedReader(fr);
			FileWriter fw = new FileWriter("/home/student/pgm1/file2.txt", true);
			String s;
 
			while ((s = br.readLine()) != null) { // read a line
				fw.write(s); // write to output file
				fw.flush();
			}
			br.close();
			fw.close();
            
			System.out.println("FILE COPIED");
		} catch (IOException e) {
			
			System.out.println("An error occurred. . ."+e);
		}

	}

}
