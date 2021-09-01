# 一、C++函数指针和函数类型
## 1. 定义
- **函数指针**指向的是函数而非对象。和其他指针类型一样，函数指针指向某种特定类型
- **函数类型**由它的返回值和参数类型决定，与函数名无关

```cpp
bool length_compare(const string &, const string &);
```

上述函数类型是：`bool (const string &, const string &)`;

上述函数指针pf：`bool (*pf)(const string &, const string &)`;

## 2. 使用函数指针
- 当把函数名作为一个值使用时，该函数自动的转换成指针，如：

```cpp
pf = length_compare <=>等价于pf = &length_compare
```
## 3. 函数指针形参
- **函数类型**不能定义为形参，但是形参可以是指向函数的指针
- 函数作为实参使用时，会自动的转换成函数指针
## 4. 返回指向函数的指针
返回执行函数类型的指针。和函数参数不同，编译器不会自动地将函数返回类型当作指针类型处理，必须**显示的**将返回类型**指定为指针**，如下

```cpp
using F = int(int*, int);	F是函数类型
using PF = int(*)(int*,int);	PF是函数指针类型
// 需要指定返回类型是指针
F  f1(int);    //错误： F是函数类型
PF  f1(int);   //正确： PF是函数指针类型
```
# 二、异步客户端和同步客户端
## 1. 同步客户端

比如一个连接有两个请求，请求1 和 请求2，请求1 先发起请求，请求2后发起请求

则请求2 要等待请求1 响应完成才能接收到响应。

举个枣子，httpclient 发送get请求，线程会一致阻塞，直到有响应结果。

## 2. 异步客户端

比如一个连接有两个请求，请求1 和 请求2，请求1 先发起请求，请求2后发起请求，请求1 和 请求2 可以并发的获取响应。

举个枣子，asynhttpclient 发送get请求，线程不会阻塞，程序往下走。

# 三、回调函数
**回调函数**就是一个通过**函数指针**调用的函数，如果你把函数的指针（地址）作为**参数**传递给另一个函数，当这个指针被用来调用其所指向的函数时，我们就说这是回调函数。
# 四、 无锁队列
## 1. 定义
**（单读单写）**

两个线程同步操作某种数据时，不能加锁；因为加锁是会拖慢效率，造成延时。

## 2. 什么场景需要用到无锁队列？

生产者和消费者模型，**要求生产者生产的同时，进行消费**，这就要求足够的低延时，此时可以使用无锁队列

## 3. 无锁队列的实现

```cpp
#define MAX_NUMBER 1000
#define OK 0
#define ERROR -1

typedef struct _QUEUE_DATA
{
	int iData[MAX_NUMBER];
	int head;
	int tail;
}QUEUE_DATA;

QUEUE_DATA* pHead = new QUEUE_DATA;

pHead->head = 0;
pHead->tail = 0;

//从队尾加入数据，队列是一个环形队列
int push_data(QUEUE_DATA* pHead, int data)
{
	if(pHead == NULL || (pHead->head ==((pHead->tail +1) % MAX_NUMBER)))
	{
		return ERROR;
	}
	pHead->iData[pHead->tail] = data;
	pHead->tail = (pHead->tail+1) % MAX_NUMBER;
	return OK;
}

int pop_data(QUEUE_DATA* pHead)
{
	if(pHead == NULL || (pHead->head == pHead->tail))
	{
		return 	ERROR;
	}
	pHead->iData[pHead->head] = 0;
	pHead->head = (pHead->head+1)% 	MAX_NUMBER;
	return OK;
} 
```

# 四、#if 0 ... #endif 注释
块注释符（/*...*/）是不可以嵌套使用的。

可以使用 #if 0 ... #endif 来实现注释，且可以实现嵌套，格式为：

```cpp
#if 0
 code
#endif 
```
你可以把 #if 0 改成 #if 1 来执行 code 的代码。
这种形式对程序调试也可以帮助，测试时使用 #if 1 来执行测试代码，发布后使用 #if 0 来屏蔽测试代码。
#if 后可以是任意的条件语句。

# 五、防止头文件重复引用
在C/C++中，在使用预编译指令**#include**的时候，为了防止重复引用造成二义性，通常有两种方式
第一种是 **#ifndef** 指令防止代码块重复引用，比如说

```cpp
#ifndef _CODE_BLOCK		// _CODE_BLOCK是头文件的文件名大写
#define _CODE_BLOCK

// code

#endif// _CODE_BLOCK 
```
第二种就是 **#pragma once**指令，在想要保护的文件开头写入

```cpp
#pragma once
```
同一个文件不会被包含多次。这里所说的”同一个文件”是指物理上的一个文件，而不是指内容相同的两个文件。无法对一个头文件中的一段代码作#pragma once声明，而只能针对文件

缺点是如果某个头文件有多份拷贝，此方法不能保证它们不被重复包含

> 总结：**\#ifndef可以针对一个文件中的部分代码，而#pragma once只能针对整个文件。相对而言，#ifndef更加灵活，兼容性好，#pragma once操作简单，效率高**
# 六、C++使用初始化列表来初始化字段
使用初始化列表来初始化字段：

```c++
Line::Line( double len): length(len)
{
    cout << "Object is being created, length = " << len << endl;
}
```

上面的语法等同于如下语法：

```cpp
Line::Line( double len)
{
    length = len;
    cout << "Object is being created, length = " << len << endl;
}
```
# 七、main函数标准写法
`main( int argc, char* argv[], char **env )` 是UNIX、Linux以及Mac OS*

 操作系统中C/C++的main函数标准写法

 第一个参数：统计程序运行时发送给main函数的命令行参数的个数，在VS中默认值为1*

 第二个参数：用来存放指向的字符串参数的指针数组，每一个元素指向一个参数。各成员含义如下：

    argv[0]指向程序运行的全路径名
    
    argv[1]指向在DOS命令行中执行程序名后的第一个字符串
    
    argv[2]指向执行程序名后的第二个字符串
    
    argv[3]指向执行程序名后的第三个字符串
    
    argv[argc]为NULL

  第三个参数：char**型的env，为字符串数组。env[]的每一个元素都包含ENVVAR=value形式的字符串，

  其中ENVVAR为环境变量，value为其对应的值。平时使用到的比较少
# 八、C++异常处理
我们通常希望自己编写的程序能够在异常的情况下也能作出相应的处理，而不至于程序莫名其妙地中断或者中止运行了。在设计程序时应充分考虑各种异常情况，并加以处理。

在C++中，一个函数能够检测出异常并且将异常返回，这种机制称为**抛出异常**。

当抛出异常后，函数调用者捕获到该异常，并对该异常进行处理，我们称之为**异常捕获**。

C++新增**throw**关键字用于**抛出异常**，新增**catch**关键字用于**捕获异常**，新增**try**关键字尝试**捕获异常**。**通常将尝试捕获的语句放在 try{ } 程序块中，而将异常处理语句置于 catch{ } 语句块中**
抛出异常的基本语法：

> **throw 表达式;**

抛出异常后需要捕获异常以及异常处理程序，其基本语法如下：

```cpp
try
{
    //可能抛出异常的语句
}
catch (异常类型1)
{
    //异常类型1的处理程序
}
catch (异常类型2)
{
    //异常类型2的处理程序
}
// ……
catch (异常类型n)
{
    //异常类型n的处理程序
}
```
由try程序块捕获throw抛出的异常，然后依据异常类型运行catch程序块中的异常处理程。catch程序块顺序可以是任意的，不过均需要放在try程序块之后。

> 在C语言中，异常通常是通过函数返回值获得，但这样一来，函数是否产生异常则需要通过检测函数的返回值才能得知。而在C++中，当函数抛出一个返回值时，即使不用try和catch语句，异常还是会被处理的，系统会自动调用默认处理函数unexpected来执行。

# 九、std::nothrow
**在内存不足时，new (std::nothrow)并不抛出异常，而是将指针置NULL**

分配失败是非常普通的，它们通常在植入性和不支持异常的可移动的器件中发生更频繁。因此，应用程序开发者在这个环境中使用nothrow new来替代普通的new是非常安全的

> p = new(std :: nothrow)char[1024*1024];
>
> p = new(std::nothrow)char[2047 *1024 *1024];

# 十、C++中的一些类型
## 1. C++ 什么是有符号，什么是无符号
整型有无符号(unsigned)和有符号(signed)两种类型。

在默认情况下声明的整型变量都是有符号的类型(char有点特别),如果需声明无符号类型的话就需要在类型前加上**unsigned**.

**区别**：无符号类型能保存2倍于有符号类型的数据。

比如16位系统中一个int能存储的数据的范围为-32768 ~ 32767，而unsigned能存储的数据范围则是0~65535。在一些不可能取值为负数的时候，可以定义为unsigned，
## 2. auto类型
auto被解释为一个自动存储变量的关键字，也就是申明一个临时的变量内存
## 3. size_t类型
 size_t是一些C/C++标准在stddef.h中定义的。**这个类型足以用来表示对象的大小。**

 size_t的真实类型与操作系统有关。
在32位架构中被普遍定义为：
`typedef   unsigned int size_t;`
而在64位架构中被定义为：
`typedef  unsigned long size_t;`

size_t在32位架构上是4字节，在64位架构上是8字节，在不同架构上进行编译时需要注意这个问题。而**int在不同架构下都是4字节**，与size_t不同；**且int为带符号数，size_t为无符号数。**

**为什么有时候不用int，而是用size_type或者size_t**

与int固定四个字节不同有所不同,size_t的取值range是目标平台下最大可能的数组尺寸,一些平台下size_t的范围小于int的正数范围,又或者大于unsigned int. 使用Int既有可能浪费，又有可能范围不够大。

## 4. int16, int32, int64



| int16 | 16位整数(16bit integer)  | 相当于short  占2个字节       | -32768 ~ 32767                             |
| ----- | ------------------------ | ---------------------------- | ------------------------------------------ |
| int32 | 32位整数(32bit integer)  | 相当于 int      占4个字节    | -2147483648 ~ 2147483647                   |
| int64 | 64位整数(64bit interger) | 相当于 long long   占8个字节 | -9223372036854775808 ~ 9223372036854775807 |
| Byte  |                          | byte(unsigned char)          | 0 ~ 255                                    |
| WORD  |                          | unsigned short               | 0 ~ 65535                                  |

## 5. unit8_t、unit16_t、unit32_t、unit64_t


| unit8_t  | 无符号1个字节的整型 |
| -------- | ------------------- |
| unit16_t | 无符号2个字节的整型 |
| unit32_t | 无符号4个字节的整型 |
| unit64_t | 无符号8个字节的整型 |

注：一个字节有8位。

# 十一、将数据存储在数组中，并转化为string类型

```cpp
// 将数据存储到数组中
char buff[100] = {0};
sprintf((char*)buff, " height = %-10f    x = %-10f   y = %-10f   angle = %-10f",x,y,z,angle);
// 将数组转化为string类型
int size_buff = sizeof(buff) / sizeof(char);
string str = "";
for(int x = 0; x < size_buff; x++) 
 {
     str = str + buff[x];
 }
```
# 十二、链表问题: 虚拟节点dummy
在链表操作中，使用一个dummy结点，可以少掉很多边界条件的判断。

在链表的头部加入一个哨兵，然后连上head节点

**之后就把head节点当做普通节点，不用单独考虑了**

```cpp
ListNode *dummy = new ListNode(-1);
dummy -> next = head;
```
最后返回

```cpp
return dummy->next;
```

# 十三、预编译指令
c语言中条件编译相关的预编译指令，包括#define、 #undef、 #ifndef、#if、#elif、#else、#endif、defined

```bash
#define   定义一个预处理宏
#undef    取消宏的定义

#if       编译预处理中的条件命令，相当于C语法中的if语句
#ifdef    判断某个宏是否被定义，若已定义，执行随后的语句
#ifndef   与#ifdef相反,判断某个宏是否未被定义
#elif     与#if、#ifdef、#ifndef或前面的#elif条件不满足，则执行#elif之后的语句，相当于C语法中的else if
#else     与#if、#ifdef、#ifndef对应，若这些条件不满足，则执行#else之后的语句，相当于C语法中的else
#endif    #if、#ifdef、#ifndef这些命令的结束标志
defined   与#if、#elif配合使用，判断某个宏是否被定义
		 defined(name): 若宏被定义，则返回1，否则返回0。
```









## 









