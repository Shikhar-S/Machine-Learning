import java.io.*;
import java.util.*;



public class Rule{


        static Float min_conf = new Float(0.6);
                
        static Map< Vector<Integer>, Float > map = new HashMap<Vector<Integer>, Float>();

         static void print_vector(Vector<Integer> v){
                for(int i=0;i<v.size();i++){
                  System.out.print(v.get(i)+" ");
                }
        }


        public static void gen_rule( Vector<Integer> v){


                if(map.get(v)==null){
                        System.out.println(v+"NULL");
                        return;
                }
                Float num  =  map.get(v);
                
                List< Vector<Integer> > new_set,v_set = new ArrayList< Vector<Integer> >();

                
                for(int i=0;i<v.size();i++){
                 Vector<Integer> temp = new Vector<Integer>(v);                
                        temp.remove(i);
                        if(map.get(temp)==null){
                        System.out.println(temp+"NULL");
                        return;
                }
                        if(num/map.get(temp) < min_conf) continue;
                        print_vector(temp);
                        System.out.print(", ");
                        v_set.add(temp);
                        temp = new Vector<Integer>();
                        temp.add(v.get(i));
                        print_vector(temp);
                        System.out.println();
                        v_set.add(temp);
                }
        
        int l=1;         

         while(true){
                new_set = new ArrayList< Vector<Integer> >();

                for(int i=0;i<v_set.size();i+=2){
                        Vector<Integer> v1 = new Vector<Integer>(v_set.get(i));                        
                        Vector<Integer> v2 = new Vector<Integer>(v_set.get(i+1));

                        for(int j=i+2;j<v_set.size();j+=2){

                                
                                Vector<Integer> u1 = new Vector<Integer>(v_set.get(j));
                                Vector<Integer> u2 = new Vector<Integer>(v_set.get(j+1));

                                Vector<Integer> w1 = new Vector<Integer>(v1);
                                Vector<Integer> w2 = new Vector<Integer>(v2);

                                int uu2 = u2.get(u2.size()-1);
                                int ww2 = w2.get(w2.size()-1);
                        
                                u2.remove(u2.size()-1);
                                w2.remove(w2.size()-1);


                                if(!u2.equals(w2)) continue;


                                
                                int a = u1.indexOf(ww2);
                                int b = w1.indexOf(uu2);

                                

                                if(a==-1||b==-1) continue;


                                u2.add(ww2);
                                u2.add(uu2);

                                u1.remove(a);
                        
                                if(u1.size()==0) continue;

                                if(map.get(u1)==null){
                        System.out.println(u1+"NULL");
                        return;
                }
                                if(num/map.get(u1)<min_conf) continue;

                                print_vector(u1);
                                System.out.print(",");
                                print_vector(u2);
                                System.out.println();
                                new_set.add(u1);
                                new_set.add(u2);


                                
                        }
                

                }
                v_set = new_set;
                if(v_set.size()==0) break;


          }


        }


        public static void main(String [] args) throws Exception{
                BufferedReader br = new BufferedReader (new FileReader("a.txt"));
                String string;                
                string = br.readLine();
                while(string!=null){
                        Vector<Integer> v = new Vector<Integer>(); 
                        String[] parts  = string.split(",");
                        for(int i=0;i<parts.length-1;i++){
                                v.addElement(Integer.parseInt(parts[i]));
                        }
                        if(parts[parts.length-1].charAt(0)!=' '){
                                String[] parts2 = parts[parts.length-1].split(" ");
                                v.addElement(Integer.parseInt(parts2[0]));
                        }
                        String[] parts2 = parts[parts.length-1].split("SUP:");
                        map.put(v,Float.parseFloat(parts2[1]));
                        string= br.readLine();
                }
                br.close();

                        
                BufferedReader brr = new BufferedReader( new FileReader("a.txt"));
                if(brr==null){
                        return;
                }
                string = brr.readLine();
                while(string!=null){
                        Vector<Integer> v = new Vector<Integer>(); 
                        String[] parts  = string.split(",");
                        for(int i=0;i<parts.length-1;i++){
                                v.addElement(Integer.parseInt(parts[i]));
                        }
                        if(parts[parts.length-1].charAt(0)!=' '){
                                String[] parts2 = parts[parts.length-1].split(" ");
                                v.addElement(Integer.parseInt(parts2[0]));
                        }
                        if(v.size()<2){
                                string=brr.readLine();
                                continue;
                        }
                        gen_rule(v);     
                        string= brr.readLine();

                }
                


        }
}
