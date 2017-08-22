#ifndef TABLE_H_INCLUDED
#define TABLE_H_INCLUDED
#include <iostream>
#include <algorithm>
#include <string.h>
#include <vector>
#include <unordered_map>
#define RECORDS 32561
#define TSIZE 16281
using namespace std;
class Table{
	public:
		 
		//arrays to store feature values
		 string data[RECORDS+1][15]; //1 indexed
		 int result[RECORDS+1];
		 long long average[15];
	public:
	Table(){
		memset(average,0,sizeof(average));
	}
	void initFeature();
	void set(int idx,int attribute,string att_value);
    void printData();
    void printResult();
    
	void modify_column(int);
	void replaceUnknown();
	void modifyTestdata(vector<string> &);
};

#endif
