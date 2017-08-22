#ifndef NODE_H_INCLUDED
#define NODE_H_INCLUDED
#include <vector>
#include <map>
#include <string.h>

using namespace std;
struct node{
	vector<int> data_index; //index of data items pertaining to this node
	int divide_f;
    bool att_present[15];
    map<string, node*> children;
    int target_v;
    node(){
        target_v=-1; //Not a leaf node hence not 0 or 1
        divide_f=-1;
        memset(att_present, false, sizeof(att_present));
        
    }
};


#endif
