#include<iostream>
#include<algorithm>
#include<cmath>
#include<vector>
using namespace std;

#if 0
int main()
{
    vector<int> num = {1,2,0,0};
    int k=34;
    // for(vector<int>::iterator it= num.begin(); it!= num.end(); it++)
    // {
    //     cout << *it << endl;  // 1, 2, 0, 0  从左往右
    // }
    int count = 0;
    // for(int i=0; i<num.size(); i++)
    // {
    //     count += num[i] * pow(10, num.size()-i-1);
    // }
    // count += k;
    cout << count <<endl;
    vector<int> num1;
    while(count)
    {
        num1.push_back(count%10);
        count /= 10;
    }
    std::reverse(num1.begin(), num1.end());
     for(vector<int>::iterator it= num1.begin(); it!= num1.end(); it++)
    {
        cout << *it << endl;  // 1, 2, 0, 0  从左往右
    }
    return 0;
}
# endif

int main()
{
    vector<int> num = {2,1,5};
    int k=806;

    vector<int> num1;

    int n= num.size();
    for(int i = n-1; i>=0; i--)
    {
        int sum = num[i]+k%10;
        k /= 10;
        if(sum>=10)
        {
            k++;
        }
        num1.push_back(sum%10);
        sum = 0;
    }
    cout << k;
    while(k>0)
    {
        num1.push_back(k%10);
        k /= 10;
    }
    reverse(num1.begin(), num1.end());

    for(vector<int>::iterator it= num1.begin(); it!= num1.end(); it++)
    {
        cout << *it << " ";  // 1, 2, 0, 0  从左往右
    }
    cout << endl;
    return 0;
}