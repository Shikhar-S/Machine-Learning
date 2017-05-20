import java.util.*;
class Node{
	Vector<Node> children;
	Node crossLink;
	Node parent;
	int count;
	String item;
	Node(String attr)
	{	
		this.item=attr;
		count=1;
		children=new Vector<Node>();
		parent=null;
	}
}
class FPTree{
	final int NumberOfBins=10;
	Node Root;
	public int call;
	public int mcall;
	int totalItems; ///////add this
	FPTree()
	{
		Root=null;
		mcall=0;call=0;
	}
	FPTree(Node t)
	{
		Root=new Node(t.item);
		Root.count=t.count;
		Root.item=t.item;
		call=0;
		mcall=0;
	}
	void addPath(String items[]) 
	{
		if(Root==null)Root=new Node("");
		int currentIndex=0;
		Node currentNode=Root;
		while(currentIndex<items.length)
		{
			boolean flag=true;
			for(int i=0;i<currentNode.children.size() && flag;i++)
			{
				Node thisNode=currentNode.children.get(i);
				if(thisNode.item.equals(items[currentIndex]))
				{
					thisNode.count++;
					currentNode=thisNode;
					currentIndex++;
					flag=false;
				}
			}
			if(flag)
			{
				Node temp=new Node(items[currentIndex]);
				temp.parent=currentNode;
				currentNode.children.addElement(temp);
				currentNode=temp;
				currentIndex++;
			}
		}

	}
	Node findConnection(Node x,Node root)
	{
		if(root==null)return null;
		Node answer=null;
		for(int i=0;i<root.children.size();i++)
		{
			Node current=root.children.get(i);
			mcall++;
			if(current.item.equals(x.item) && mcall>call)
				return current;
			else
				answer=findConnection(x,current);
			if(answer!=null)return answer;
		}
		return answer;
	}
	void setUpCrossLinks(Node root)  
	{
		if(root==null)
			return;
		for(int i=0;i<root.children.size();i++)
		{
			Node x=root.children.get(i);
			call++;
			mcall=0;
			Node toConnect=findConnection(x,Root);
			x.crossLink=toConnect;
			setUpCrossLinks(x);
		}
	}
	void printTree(Node current,String x)
	{
		if(current==null)return;
		if(current!=Root)
		System.out.println(" ( "+x+" ) "+current.item+" : "+current.count+" ( "+current.crossLink+" ) ");
		for(int i=0;i<current.children.size();i++)
		{
			printTree(current.children.get(i),x+"."+(i+1));
		}

	}
	Node findStart(Node root,String item)
	{
		if(root==null)return null;
		Node answer=null;
		for(int i=0;i<root.children.size();i++)
		{
			Node x=root.children.get(i);
			if(x.item.equals(item))
				return x;
			answer=findStart(x,item);
			if(answer!=null)return answer;
		}
		return null;
	}
	int sumItemFreq(String item)
	{
		Node start=findStart(Root,item);
		int ans=0;
		while(start!=null)
		{
			ans+=start.count;
			start=start.crossLink;
		}
		return ans;
	}
}
class FPgrowth
{
	Vector<String> sortedOrder=new Vector<String>();
	HashMap< String, Integer> sets=new HashMap< String, Integer >();
	private boolean includeBranch;
	void loadOrder(Scanner sc)
	{
		String x=sc.next();
		while(!(x.equals("EOF")))
		{
			sortedOrder.addElement(x);
			x=sc.next();
		}	
		//System.out.println(sortedOrder.size());	
	}
	void correctCounts(Node x)
	{
		if(x==null)
			return;
		int c=0;
		for(int i=0;i<x.children.size();i++)
		{
			correctCounts(x.children.get(i));
			c+=x.children.get(i).count;
		}
		if(c!=0)
			x.count=c;
	}
	void removeInfrequentNodes(FPTree x,int threshold,int endAt)
	{
		for(int i=sortedOrder.size()-1;i>=endAt;i--)
		{
			int cnt=x.sumItemFreq(sortedOrder.get(i));
			//System.out.println(cnt);
			if(cnt<threshold)
			{
				//remove this cross chain
				Node start=x.findStart(x.Root,sortedOrder.get(i));
				if(start==null || start.parent==null)
				{
					start=null;
					break;
				}
				else
					while(start!=null)
					{
						
						start.parent.children.remove(start);
						for(int j=0;j<start.children.size();j++)
						{
							Node child=start.children.get(j);
							child.parent=start.parent;
							start.parent.children.addElement(child);
						}
						start=start.crossLink;
					}
			}
		}
	}
	FPTree constructSubtree(Node tree,String check_item)
	{
		if(tree==null)
		{
			return null;
		}
		if(tree.item.equals(check_item))
		{
			includeBranch=true;
			FPTree t=new FPTree(tree); //copy constructor
			return t;
		}
		FPTree temp=null;
		temp=new FPTree(tree);
		boolean evertrue=false; 
		for(int i=0;i<tree.children.size();i++)
		{
			includeBranch=false;
			FPTree x=constructSubtree(tree.children.get(i),check_item);
			//x.printTree(x.Root,"");
			//System.out.println("**************");
			evertrue=evertrue || includeBranch;
			//System.out.println(includeBranch +" for "+ tree.children.get(i).item);
			if(includeBranch)
			{
				temp.Root.children.addElement(x.Root);
				x.Root.parent=temp.Root;
			}
		}
		//System.out.println(evertrue);
		includeBranch=evertrue;
		return temp;
	}

	void findFrequentSets(FPTree tree,double support_threshold,String x,int startidx) //call(tree,spth,"",0)
	{
		for(int i=startidx;i<sortedOrder.size();i++)
		{
			int count=tree.sumItemFreq(sortedOrder.get(i));
			//System.out.println("Considering-->"+x+" "+sortedOrder.get(i)+" count--> "+count);
			if(count<support_threshold*tree.totalItems)
			{
				continue;
			}
			String itemset=x+" "+sortedOrder.get(i);
			//System.out.println("Working for --> "+itemset);
			FPTree subtree=constructSubtree(tree.Root,sortedOrder.get(i));
			//subtree.printTree(subtree.Root,"");
			
			
			

			//System.out.println("---------Changed values-------");
			//subtree.printTree(subtree.Root,"");
			tree.call=0;tree.mcall=0;
			subtree.setUpCrossLinks(subtree.Root);
			removeInfrequentNodes(subtree,(int)(support_threshold*tree.totalItems),i);
			/*if(sortedOrder.get(i).equals("E2"))
			System.out.println("Before=> "+subtree.sumItemFreq("D3"));*/
			correctCounts(subtree.Root);
			/*if(sortedOrder.get(i).equals("E2"))
			System.out.println("After=> "+subtree.sumItemFreq("D3"));*/
			sets.put(itemset,count);
			//System.out.println(itemset+" "+count);
			subtree.totalItems=tree.totalItems;
			findFrequentSets(subtree,support_threshold,itemset,i+1);
		}		
	}
	void displaySets(FPTree fpt)
	{
		Iterator it = sets.entrySet().iterator();
		//System.out.println("Shikhar");
	    while (it.hasNext()) {
	        Map.Entry pair = (Map.Entry)it.next();
	        System.out.println(pair.getKey()+ " #SUP: " + Integer.parseInt(pair.getValue().toString())/(fpt.totalItems*1.0));
	    }
	}
}
public class FPDemo
{
	public static void main(String args[])
	{
		FPTree fpt=new FPTree();
		Scanner sc=new Scanner(System.in);
		String x=sc.next();
		fpt.Root=null;
		while(x.equals("T"))
		{
			fpt.totalItems+=1;
			int j=9;
			int k=j;
			String arr_s[]=new String[j];
			while(j>0)
			{
				arr_s[k-j]=sc.next();
				j--;
			}
			fpt.addPath(arr_s);
			//System.out.println("Continue? T : F");
			x=sc.next();
		}
		fpt.call=0;
		fpt.mcall=0;
		fpt.setUpCrossLinks(fpt.Root);
		//fpt.printTree(fpt.Root,"");
		FPgrowth fpg=new FPgrowth();
		fpg.loadOrder(sc);
		int threshold=(int)(0.2*fpt.totalItems);
		//System.out.println("Thrshold="+threshold);
		//System.out.println("Total="+fpt.totalItems);
		fpg.findFrequentSets(fpt,0.25,"",0);
		fpg.displaySets(fpt);
	}
}