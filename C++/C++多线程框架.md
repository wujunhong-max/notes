# C++多线程框架

## 定义

线程可以理解为一个特立独行的函数。其存在的意义，就是并行，避免了主线程的阻塞

## 线程启动

## 头文件

> #include<thread>

线程对象的创建，意味着线程的开始

(1) 同步

```c++
#include <iostream>
#include <thread>
#include <unistd.h>

using namespace std;

void func()
{
	cout<<"thread id:"<<this_thread::get_id()<<endl;
    cout<<"do some work"<<endl;
    sleep(3);
}
int main()
{
    cout<<"maint thread id:"<<this_thread::get_id()<<endl;
    thread t(func);
    t.join();
    return 0;
}
```

运行结果：

