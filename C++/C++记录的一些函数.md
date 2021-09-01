# memcmp函数  比较
**功能**

比较内存区域buf1和buf2的**前count个字节**，区分字母的大小写

`int memcmp(const void *buf1, const void *buf2, unsigned int count);`

**参数**
- buf 1 - 比较串1 
- buf2  - 比较串2 
- count - 比较字节数


**返回值**

当buf1<buf2时，返回值<0 

当buf1=buf2时，返回值=0 

当buf1>buf2时，返回值>0

# memcpy函数  拷贝
c和c++使用的内存拷贝函数，memcpy函数的功能是**从源src所指的内存地址的起始位置**开始拷贝n个字节到**目标dest所指的内存地址的起始位置中**

头文件：`<string.h>`或`<cstring>`
函数原型：

```cpp
memcmp (const void*, const void*, size_t);
第一个参数: 目的地址
第二个参数：源地址
第三个参数：所需要复制的字节数
```
# c_str()函数  转化
c_str()函数**就是把string编成了char*类型**

const char* c_str();

返回一个指向正规C字符串的指针, 内容与本string串相同,这是为了与c语言兼容，在c语言中没有string类型，故必须通过**string类对象的成员函数**c_str() 把string 对象转换成c中的字符串样式。

# usleep()函数  暂停
usleep函数能把线程挂起一段时间， 单位是微秒（千分之一毫秒）。本函数可暂时使程序停止执行。参数 micro_seconds 为要暂停的微秒数(us)。

这个函数不能工作在windows 操作系统中。用在Linux的测试环境下面。