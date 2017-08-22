#include "table.h"
#include <cstring>
#include <map> 
using namespace std;

void Table::set(int idx,int attribute,string att_value)
{
	if(attribute==15)
	{
		if (att_value==" >50K")
			Table::result[idx]=1;
		else
			Table::result[idx]=0;
	}
	else
		Table::data[idx][attribute]=att_value;
}

void Table::printData()
{
    for(int i=0;i<=RECORDS;i++)
    {
        for(int j=1;j<=14;j++)
            cout<<Table::data[i][j]<<" ";
        cout<<endl;
    }
}
void Table::printResult()
{
    for(int i=1;i<=RECORDS;i++)
    {
        cout<<Table::result[i]<<"\n";
    }
}

// NEW FUNCTIONS

void Table::replaceUnknown(){
	
	for(int col=1;col<15;col++){
		map<string,int> count;
		for(int i=1;i<=RECORDS;i++){
			if(count.find(data[i][col])==count.end())
				count[data[i][col]]=1;
			else
				count[data[i][col]]++;
		}
		string mostFreq;
		int maxfreq=0;
		map<string,int>::iterator it;
		for(it=count.begin();it!=count.end();it++){
			if(it->second > maxfreq){
				maxfreq = it->second;
				mostFreq = it->first;
			}
		}
		for(int i=1;i<=RECORDS;i++){
			if(data[i][col]==" ?")
				data[i][col]=mostFreq;
		}
	}
}

void Table::modify_column(int col){
	long long total=0;
	for(int i=1;i<=RECORDS;i++){
		total += (long long)stoi(data[i][col].substr(1));
	}
	long long threshold = (total/RECORDS);	
	average[col]=threshold;
	for(int i=1;i<=RECORDS;i++){
		if((long long)stoi(data[i][col].substr(1)) > threshold){
			data[i][col]=" 1";		// Class1
		}
		else{
			data[i][col]=" 0";		//Class0
		}
	}
}

// CONTINUOUS TEST DATA

void Table::modifyTestdata(vector<string> &values){
	int cont[]={1,3,5,11,12,13};
	for(int i=0;i<6;i++){
		if(cont[i]!=1)	
			values[cont[i]-1]= values[cont[i]-1].substr(1);	// remove space
		values[cont[i]-1] = " "+to_string(  (long long) stoi(values[cont[i]-1]) > average[cont[i]]);
	}
}

