#ifndef TREE_H_INCLUDED
#define TREE_H_INCLUDED

#include "node.h"
#include <algorithm>
#include "table.h"
#include <limits>
#include <vector>
#include <cmath>
#include <cstring>


double getEntropy(int idx,node &current,Table &t);
void initDivide_f(node &current,Table &t);
node* getNode(bool present[],vector<int> &Examples);
node* buildTree(vector<int> &Examples,Table &t,bool tr[]);
node* builder(Table &t);
void printTree(node *root);
void printNode(node *n);
int predictClass(node *,vector<string>);
double findAccuracy(vector<int>,vector<int>);
#endif
