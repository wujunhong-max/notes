#include<iostream>
#include<algorithm>
#include<cmath>
#include<string>
#include<vector>
using namespace std;

class CustomStack{
public:
    vector<int> stk;
    int top;

    CustomStack(int maxSize)
    {
        stk.resize(maxSize);
        top = -1;
    }
    void push(int x)
    {
        if(top != stk.size()-1)
        {   
            top++;
            stk[top] = x;
        }
    }
    int pop()
    {
        if(top == -1)
        {
            return -1;
        }
        top--;
        return stk[top + 1];
    }
    void increment(int k, int val)
    {
        int lim = min(k, top+1);
        for(int i=0; i<lim; i++)
        {
            stk[i] += val;
        }
    }
    
public:
    vector<int> stk;
    int top;    
};
 