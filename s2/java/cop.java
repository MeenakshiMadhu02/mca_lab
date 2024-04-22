import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

public class cop
{

    public static void main(String[] args) throws IOException {
      

        FileInputStream source = new FileInputStream ("source.txt");
        FileOutputStream destination_odd = new FileOutputStream ("odd.txt");
        FileOutputStream destination_even = new FileOutputStream ("even.txt");
        int i;
        while((i = source.read()) != -1){
            if(i%2==0) {

                destination_even.write(i);
            }
            else {
                destination_odd.write(i);
            }
        }
        System.out.println("copied");
        source.close();
        destination_even.close();
        destination_odd.close();



    }

}
