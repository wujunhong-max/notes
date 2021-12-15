#include<iostream>
#include<algorithm>
#include<cmath>
#include<string>
#include<vector>
using namespace std;


class Solution {
public:
    string decodeString(string s)
    {
        str.push_back(""); // 创建空的一层
        for(int i=0; i<s.size(); i++)   // 遍历字符串s
        {
            if(isalpha(s[i]))   // 判断字符是否为字母
                str.back() += s[i];  // 字母直接加在一层中
            else if(isdigit(s[i]))  // 判断字符是否为数字
            {
                int x=0;
                while(isdigit(s[i]))
                {
                    // 若s[i] == '0', 转化为整型数字是48, 不符合，所以要 -'0'转化
                    x = x*10 + s[i] - '0'; 
                    i++;            //考虑后面的字符也是数字
                } // 读取重复次数，此时已经遍历过一个'['
                num.push_back(x);
                str.push_back(""); //因为遍历过一个'[', 所以新开一层
            }
            else // 如果是']'则出栈一次
            {
                int a = num.back();
                string sstr = str.back();
                str.pop_back();
                num.pop_back();
                while (a -- ) str.back() += sstr;//更新最内一层的字符串
            }
        }
        return str.back();  //最后的结果是栈底
    }
private:
    vector<int> num; // 数字栈，存储重复的次数的栈
    vector<string> str; // 记录最内一层字符串的栈， 有'【'就开一层
};

int main()
{
    Solution so;
    //string wb = "3[a2[c]]";
    string wb = "3[a]2[bc]";
    cout << so.decodeString(wb) << endl;

    return 0;
}