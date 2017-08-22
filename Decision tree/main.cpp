//
//  main.cpp
//  MLassignment
//
//  Created by Shikhar  on 08/11/16.
//  Copyright © 2016 Shikhar . All rights reserved.
//


#include <iostream>
#include <algorithm>
#include <sstream>
#include <fstream>
#include <string>
#include "table.h"
#include "tree.h"
#include "node.h"
#include <unistd.h>
using namespace std;
Table t;

void parser(string line,int id){
    stringstream l(line);
    string att_value;
    char delim=',';
    int att_number=1;
    
    while(getline(l,att_value,delim))
    {
        t.set(id,att_number,att_value);
        att_number++;
    }
}

vector<string> extractCells(string line){
	vector<string> ans;
	stringstream l(line);
    string att_value;
    char delim=',';
	while(getline(l,att_value,delim)){
		ans.push_back(att_value);
	}
	return ans;
}


int main(int argc, const char * argv[])
{
    //t.initFeature();
    string line;
    string filename="data.txt";
    ifstream file(filename);
    int idx=1;
    if(file.is_open())
    {
        while(getline(file,line) && idx<=RECORDS){
            //parse contents
            parser(line,idx);
            idx++;
        }
        file.close();
    }
    else
    {
        cout<<"Problem opening File!\n";
        return -1;
    }
    cout<<"Completed loading dataset\n";
    
    t.replaceUnknown();
    
    // Continuous values thresholding
    
    int cont[]={1,3,5,11,12,13};
    for(int i=0;i<6;i++){
    	t.modify_column(cont[i]);
	} 	

    node* root=builder(t);


	// TESTING DATA

	ifstream file2("test.txt");
	idx=1;
	
	vector<int> predicted;
	vector<int> actual;
	if(file2.is_open())
    {

        while(getline(file2,line)){
        
            vector<string> values = extractCells(line);
            actual.push_back(values.back() == " >50K.");
            values.pop_back();
            t.modifyTestdata(values);	// modifies continuous test data acc to Table t
			int p = predictClass(root,values);
			predicted.push_back(p);
        }
        file2.close();
    }
    else
    {
        cout<<"Problem opening testing File!\n";
        return -1;
    }
	double acc = findAccuracy(actual,predicted);
	cout<<acc<<endl;
    
    return 0;
}

