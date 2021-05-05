# 平时遇到的一些知识点

## C++程序中#if 0 ... #endif的用法

块注释符（/*...*/）是不可以嵌套使用的。

可以使用 #if 0 ... #endif 来实现注释，且可以实现嵌套，格式为：


    #if 0
     
       code
     
    #endif 

你可以把 #if 0 改成 #if 1 来执行 code 的代码。
这种形式对程序调试也可以帮助，测试时使用 #if 1 来执行测试代码，发布后使用 #if 0 来屏蔽测试代码。
#if 后可以是任意的条件语句。

## memcmp函数

>  int memcmp(const void *buf1, const void *buf2, unsigned int count);
>
>  参数
>
>  buf 1 - 比较串1 
>  buf2  - 比较串2 
>  count - 比较字节数
>
>  功能
>
>  比较内存区域buf1和buf2的前count个字节区分字母的大小写
>
>  返回值
>
>  当buf1<buf2时，返回值<0 
>
>  当buf1=buf2时，返回值=0 
>
>  当buf1>buf2时，返回值>0

## memcpy函数

c和c++使用的内存拷贝函数，memcpy函数的功能是从源src所指的内存地址的起始位置开始拷贝n个字节到目标dest所指的内存地址的起始位置中

**头文件**

所在头文件 <string.h>或< cstring >

**函数原型**

```c++
_CRTIMP int __cdecl __MINGW_NOTHROW 	memcmp (const void*, const void*, size_t) __MINGW_ATTRIB_PURE;
第一个参数:目的地址
第二个参数：源地址
第三个参数：所需要复制的字节数
```

## 防止重复引用

#pragma指令与#ifndef指令

在C/C++中，在使用预编译指令**#include**的时候，为了防止重复引用造成二义性，通常有两种方式——

第一种是**#ifndef**指令防止代码块重复引用，比如说

```c++
#ifndef _CODE_BLOCK
#define _CODE_BLOCK

// code

#endif// _CODE_BLOCK 
```

第二种就是**#pragma once**指令，在想要保护的文件开头写入

```c++
#pragma once
```

同一个文件不会被包含多次。这里所说的”同一个文件”是指物理上的一个文件，而不是指内容相同的两个文件。无法对一个头文件中的一段代码作#pragma once声明，而只能针对文件

缺点是如果某个头文件有多份拷贝，此方法不能保证它们不被重复包含

总结：**\#ifndef可以针对一个文件中的部分代码，而#pragma once只能针对整个文件。相对而言，#ifndef更加灵活，兼容性好，#pragma once操作简单，效率高**

## C++使用初始化列表来初始化字段

使用初始化列表来初始化字段：

```c++
Line::Line( double len): length(len)
{
    cout << "Object is being created, length = " << len << endl;
}
```

上面的语法等同于如下语法：

```c++
Line::Line( double len)
{
    length = len;
    cout << "Object is being created, length = " << len << endl;
}
```

## std::nothrow

**在内存不足时，new (std::nothrow)并不抛出异常，而是将指针置NULL**

分配失败是非常普通的，它们通常在植入性和不支持异常的可移动的器件中发生更频繁。因此，应用程序开发者在这个环境中使用nothrow new来替代普通的new是非常安全的

> p = new(std :: nothrow)char[1024*1024];
>
> p = new(std::nothrow)char[2047 *1024 *1024];

## 在C语言中把string类型编成char*类型

c_str()函数**就是把string编成了char*类型**

const char*c_str();

返回一个指向正规C字符串的指针, 内容与本string串相同,这是为了与c语言兼容，在c语言中没有string类型，故必须通过string类对象的成员函数c_str()把string 对象转换成c中的字符串样式。

## 释放空间

​		int *a = new int;

​        delete a;  //释放单个int的空间

​     	int *a = new int[5];

​        delete [] a; //释放int数组空间

要访问new所开辟的结构体空间,无法直接通过变量名进行,只能通过赋值的指针进行访问.

## msg

msg就是一个字符串，表示信息的意思

## vector

### push_back()

将一个新的元素加到vector的最后面，位置为当前最后一个元素的下一个元素

**push_back() 在Vector最后添加一个元素（参数为要插入的值）**

```c++
//在vec尾部添加10
vector<int> vec;
vec.push_back(10);
//在容器中添加10
int num = 10;
vector<int> vec;
vec.push_back(num);
```

类似的：

pop_back() //移除最后一个元素

clear() //清空所有元素

empty() //判断vector是否为空，如果返回true为空

erase() // 删除指定元素

## std::size_t

它是一个与机器相关的unsigned类型，其大小足以保证存储内存中对象的大小.

在32位系统中size_t是4字节的，而在64位系统中，size_t是8字节的，这样利用该类型可以增强程序的可移植性。

四种类型都是无符号类型，是用以表示元素个数或者数组索引的最佳类型

## auto类型

auto被解释为一个自动存储变量的关键字，也就是申明一个临时的变量内存

## main函数标准写法

 main( int argc, char\* argv[], char **env ) 是UNIX、Linux以及Mac OS*

 操作系统中C/C++的main函数标准写法

 第一个参数：统计程序运行时发送给main函数的命令行参数的个数，在VS中默认值为1*

 第二个参数：用来存放指向的字符串参数的指针数组，每一个元素指向一个参数。各成员含义如下：

​    argv[0]指向程序运行的全路径名

​    argv[1]指向在DOS命令行中执行程序名后的第一个字符串

​    argv[2]指向执行程序名后的第二个字符串

​    argv[3]指向执行程序名后的第三个字符串

​    argv[argc]为NULL

  第三个参数：char**型的env，为字符串数组。env[]的每一个元素都包含ENVVAR=value形式的字符串，

  其中ENVVAR为环境变量，value为其对应的值。平时使用到的比较少

## C++异常处理

我们通常希望自己编写的程序能够在异常的情况下也能作出相应的处理，而不至于程序莫名其妙地中断或者中止运行了。在设计程序时应充分考虑各种异常情况，并加以处理。

在C++中，一个函数能够检测出异常并且将异常返回，这种机制称为**抛出异常**。

当抛出异常后，函数调用者捕获到该异常，并对该异常进行处理，我们称之为**异常捕获**。

C++新增**throw**关键字用于**抛出异常**，新增**catch**关键字用于**捕获异常**，新增**try**关键字尝试**捕获异常**。**通常将尝试捕获的语句放在 try{ } 程序块中，而将异常处理语句置于 catch{ } 语句块中**

抛出异常的基本语法：

> **throw 表达式;**

抛出异常后需要捕获异常以及异常处理程序，其基本语法如下：

```C++
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

在C语言中，异常通常是通过函数返回值获得，但这样一来，函数是否产生异常则需要通过检测函数的返回值才能得知。而在C++中，当函数抛出一个返回值时，即使不用try和catch语句，异常还是会被处理的，系统会自动调用默认处理函数unexpected来执行。

## usleep()函数

usleep函数能把线程挂起一段时间， 单位是微秒（千分之一毫秒）。本函数可暂时使程序停止执行。参数 micro_seconds 为要暂停的微秒数(us)。

这个函数不能工作在windows 操作系统中。用在Linux的测试环境下面。

## size_t 类型

 size_t是一些C/C++标准在stddef.h中定义的。这个类型足以用来表示对象的大小。size_t的真实类型与操作系统有关。

在32位架构中被普遍定义为：

typedef   unsigned int size_t;

而在64位架构中被定义为：

typedef  unsigned long size_t;
        size_t在32位架构上是4字节，在64位架构上是8字节，在不同架构上进行编译时需要注意这个问题。而int在不同架构下都是4字节，与size_t不同；且int为带符号数，size_t为无符号数。

**为什么有时候不用int，而是用size_type或者size_t**

与int固定四个字节不同有所不同,size_t的取值range是目标平台下最大可能的数组尺寸,一些平台下size_t的范围小于int的正数范围,又或者大于unsigned int. 使用Int既有可能浪费，又有可能范围不够大。

## int16,int32,int64

Int16  意思是16位整数(16bit integer)，相当于short  占2个字节   -32768 ~ 32767

Int32  意思是32位整数(32bit integer), 相当于 int      占4个字节   -2147483648 ~ 2147483647

Int64  意思是64位整数(64bit interger), 相当于 long long   占8个字节   -9223372036854775808 ~ 9223372036854775807

Byte  相当于byte(unsigned char)   0 ~ 255

WORD 等于  unsigned short     0 ~ 65535

| int16 | 16位整数(16bit integer)  | 相当于short  占2个字节       |
| ----- | ------------------------ | ---------------------------- |
| int32 | 32位整数(32bit integer)  | 相当于 int      占4个字节    |
| int64 | 64位整数(64bit interger) | 相当于 long long   占8个字节 |
| Byte  |                          | byte(unsigned char)          |
| WORD  |                          | unsigned short               |

os开发中经常遇到的数据如下的数据类型，unit8_t、unit16_t、unit32_t、unit64_t

| unit8_t  | 无符号1个字节的整型 |
| -------- | ------------------- |
| unit16_t | 无符号2个字节的整型 |
| unit32_t | 无符号4个字节的整型 |
| unit64_t | 无符号8个字节的整型 |

注：一个字节有8位。

## C++ 什么是有符号，什么是无符号

整型有无符号(unsigned)和有符号(signed)两种类型。

在默认情况下声明的整型变量都是有符号的类型(char有点特别),如果需声明无符号类型的话就需要在类型前加上unsigned.

**区别**：无符号类型能保存2倍于有符号类型的数据。

比如16位系统中一个int能存储的数据的范围为-32768~32767，而unsigned能存储的数据范围则是0~65535。在一些不可能取值为负数的时候，可以定义为unsigned，

## 将数据存储在数组中

```c++
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

## 链表问题: 虚拟节点dummy

在链表操作中，使用一个dummy结点，可以少掉很多边界条件的判断。

在链表的头部加入一个哨兵，然后连上head节点

之后就把head节点当做普通节点，不用单独考虑了

```c++
ListNode *dummy = new ListNode(-1);
dummy -> next = head;
```

最后返回

```c++
return dummy->next;
```

