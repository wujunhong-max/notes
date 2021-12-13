#include<iostream>
#include<algorithm>
#include<cmath>
#include<string>
#include<vector>
using namespace std;


int main()
{
    string  s = "loveleetcode";
    char c = 'e';

    vector<int> answer;
    vector<int> a;
    // 将相同字符的位置放进数组a中
    for(int i=0; i<s.length(); i++)
    {
        if(s[i] == c)
        {
            a.push_back(i);
        }
    } 
    int k = a.size();

    for(vector<int>::iterator it = a.begin(); it != a.end();it++)
    {
        cout << *it << " ";  // 3 5 6 11
    }
    cout << endl;
    cout << k << endl;
    int x=0, y=0;
    // 遍历数组answer
    for(int i=0; i<s.size(); i++)
    {
        if(i+1>a[y+1])
            y++;
        if(k <= 0)  break;
        if(k>0 && i == a[x])
        {
            answer.push_back(0);
            if(x<k-1)
                x++;
        }
        else if(k>0 && i<a[0])
        {
            answer.push_back(abs(i-a[0]));
        }
        else if(k>1 && a[0] < i < a[k-1])
        {
            int num = min(abs(i-a[y]), abs(a[y+1]-i));
            answer.push_back(num);
            if(i==7) 
            {
                cout << y<<  " " <<abs(i-a[y]) << " " << abs(a[y+1]-i) << " " << num <<endl;
            }
            
            num = 0;
        }
        else if(k>0 && i>a[k-1])
        {
            answer.push_back(abs(i-a[k-1]));
        }
    }
    cout << endl;
    for(vector<int>::iterator it = answer.begin(); it != answer.end();it++)
    {
        cout << *it << " ";  // 3 5 6 11
    }
    cout << endl;
    return 0;
}