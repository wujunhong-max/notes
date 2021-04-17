# LeetCode刷题

## 函数

### 看数组的大小

```c++
int nums[100];
nums.size();
```

## 数据结构

### 二分法查找

一种在**有序数组中查找特定元素**的**搜索算法**

二分法查找的思路如下：

（1）首先，从数组的中间元素开始搜索，如果该元素正好是目标元素，则搜索过程结束，否则执行下一步。

（2）如果目标元素大于/小于中间元素，则在数组大于/小于中间元素的那一半区域查找，然后重复步骤（1）的操作。

（3）如果某一步数组为空，则表示找不到目标元素。

- 二分法查找的时间复杂度O(logn)。
- 版本A

```c++
// 二分查找算法(版本A)
// 在有序向量的区间[lo,hi)内查找元素e, 0 <= lo <= hi <= _size
template <typename T>
static Rank binSearch(T* A,T const& e, Rank lo, Rank hi)
{
    while(lo < hi)
    {
        //每步迭代可能要做两次比较判断,有三个分支
        Rank mi = (lo + hi) >> 1; //以中点为轴，这个是右移一位，相对于除以2
        if (e < A[mi]) hi = mi;   // 深入前半段[l0,mi]继续查找
        else if (A[mi] > e) lo = mi + 1;   //深入后半段(mi,hi)继续查找
        else        return mi;          //在mi处命中
    }   //成功查找可以提前终止
    return -1; //查找失败
}
```

- 版本B

```c++
#include <iostream>
using namespace std;
// 二分查找算法(版本B)
// 在有序向量的区间[lo,hi)内查找元素e, 0 <= lo <= hi <= _size
template <typename T>
static Rank binSearch(T* A,T const& e, Rank lo, Rank hi)
{
    while(1 < hi-lo)
    {
        //每次迭代仅需做一次判断，有两个分支；成功查找不能提前终止
        (e < A[mi]) ? hi = mi: lo = mi; //经比较后确定深入[lo, mi)或[mi, hi)
    }   //出口时hi = lo + 1,查找区间仅含一个元素A[lo]
    return (e == A[lo]) ? lo : -1; //查找成功时返回对应的秩，否则返回-1
}  //有多个命中元素时，不能保证返回秩最大者；查找失败时，简单地返回-1，而不能指示失败的位置
```

- 版本C

```c++
#include <iostream>
using namespace std;
// 二分查找算法(版本C)
// 在有序向量的区间[lo,hi)内查找元素e, 0 <= lo <= hi <= _size
template <typename T>
static Rank binSearch(T* A,T const& e, Rank lo, Rank hi)
{
    while(lo < hi)
    {
        //每次迭代仅需做一次判断，有两个分支
        Rank mi = (lo + hi) >> 1; //以中点为轴点
        ( e < A[mi])? hi = mi : lo = mi + 1; //经比较后确定深入[lo, mi)或(mi , hi]
    }   //成功查找不能提前终止
    return --lo;//循环结束时，lo为大于e的元素的最小秩，故lo-1即不大于e的元素的最大秩
}  // 有多个命中元素时，总能保证返回秩最大者；查找失败时，能够返回失败的位置
```

