#include "tree.h"
// returns entropy of a att_nimber column
static int c=0;
double getEntropy(int att_number,node &current,Table &t)
{
    unordered_map<string,int> pos_neg[2];
    unordered_map<string,int> counts;
    double S=0;
	for(int i=0;i<current.data_index.size();i++)
	{
        S++;
		counts[t.data[current.data_index[i]][att_number]]++;
        if (t.result[current.data_index[i]]==0) {
            pos_neg[0][t.data[current.data_index[i]][att_number]]++;
        }
        else
        {
            pos_neg[1][t.data[current.data_index[i]][att_number]]++;
        }
	}
	double entropy=0;
	
	for(unordered_map<string, int>::iterator it=counts.begin();it!=counts.end();it++)
	{
		double Sv=(it->second); //Sv
        double denom=pos_neg[0][it->first]+pos_neg[1][it->first];
        double pos=pos_neg[1][it->first];
        double neg=pos_neg[0][it->first];
        if(pos==0)pos=1;
        if(neg==0)neg=1;
        entropy+=(Sv/S)*(-(pos/denom)*(log(pos/denom)/log(2))-(neg/denom)*(log(neg/denom)/log(2)));
	}
	return entropy;
}
void initDivide_f(node &current,Table &t)
{
	double min_entropy=numeric_limits<double>::max();
	for(int i=1;i<15;i++)
	{
		if(current.att_present[i])
		{
			double temp=getEntropy(i,current,t);
            /*if(temp!=temp)
            {
                current.divide_f=i;
                break;
            }*/
			if(min_entropy>temp)
			{
				min_entropy=temp;
				current.divide_f=i;
			}
		}
	}
}
node* getNode(bool present[],vector<int> &Examples)
{
    node *temp=new node;
	for(int i=0;i<15;i++)
	temp->att_present[i]=present[i];
    temp->data_index=Examples;
	return temp;
}
node* buildTree(vector<int> &Examples,Table &t,bool attributes[])
{

	int s=0;
	bool flag=false;
	//initDivide_f(current,t);
    node *current=getNode(attributes,Examples);
    for(int i=1;i<15;i++)
        flag|=attributes[i];
	for(int i=0;i<Examples.size();i++)
	{
		s+=t.result[Examples[i]];
		
	}
	if(!flag || s==0 || s==Examples.size())
	{
		current->target_v=(s>(Examples.size()/2.0));
		return current;
	}
    initDivide_f(*current, t);
    current->att_present[current->divide_f]=false;
    unordered_map<string, vector<int> > subsets;
	for(int i=0;i<Examples.size();i++)
	{
		subsets[t.data[Examples[i]][current->divide_f]].push_back(Examples[i]); //val of att
	}
    
    for(unordered_map<string, vector<int> >::iterator it=subsets.begin();it!=subsets.end();it++)
	{
        
            current->children[it->first]=buildTree(it->second, t, current->att_present);
            

        
	}
    return current;
}
node* builder(Table &t)
{
	vector<int> dataset;
	for(int i=1;i<=RECORDS;i++)
		dataset.push_back(i);
	bool all_true[15];
	memset(all_true,true,sizeof all_true);
    //all_true[3]=false;all_true[1]=false;all_true[13]=false;all_true[11]=false;all_true[5]=all_true[12]=false;
	node* root=buildTree(dataset,t,all_true);
	return root;
}
void printNode(node *toPrint)
{
    cout<<"Result "<<toPrint->target_v<<endl;
    cout<<"Dividing atrribute "<<toPrint->divide_f<<endl;
    
}
void printTree(node *current)
{
    if (current==nullptr) {
        return;
    }
    printNode(current);
    for (map<string,node*>::iterator it=current->children.begin();it!=current->children.end();it++) {
        printTree(it->second);
    }
}
int predictClass(node *root, vector<string> values){
	if (root == NULL)
		return 0;
			
    if(root->target_v != -1 || root->divide_f==-1)		// if leaf node
    	return root->target_v;
    
    string splitting_col_value = values[root->divide_f - 1];			// values is 0 indexed
    
	return predictClass(root->children[splitting_col_value],values);
}

double findAccuracy(vector<int> actual,vector<int> predicted){
	if(actual.size()!=predicted.size()){
		cout<<" \nDIFFERENT SIZES OF RESULTS\n";
		return -1.0;
	}
	int cnt=0;
	for(int i=0;i<actual.size();i++){
		cnt += (predicted[i]==actual[i]);
	}
	return ((double)(cnt)*100)/actual.size();
}




