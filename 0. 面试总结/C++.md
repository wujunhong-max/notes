# 强制转换

# 四种智能指针

## 作用

用来管理一个指针，避免申请的空间在函数结束忘记释放，造成内存泄漏的问题

而智能指针是一个类，当超过类的作用域时，类会自动调用析构函数，析构函数会自动释放资源。所以智能指针在函数结束时会自动释放内存空间，不需要手动释放内存空间，这样就避免内存泄漏

- auto_ptr（C++98的方案，C11已抛弃）采用所有权模式
- unique_ptr （替换auto_ptr)
- shared_ptr（共享型，强引用）
- weak_ptr（弱引用）

## 用法

### 头文件

·#include<memory>`

### auto_ptr（所有权模式）

存在被管理资源的所有权转移问题，这导致多个std::auto_ptr类型的局部变量不能共享同一个资源

```cpp
#include<iostream>
#include<memory>
using namespace std;

int main()
{
    auto_ptr<std::string> p1 = new string("hello");
    auto_ptr<std::string> p2;
    p2 = p1;
    cout << *p2 << endl;	// hello
    cout << *p1 << endl;	// 编译通过，运行报错
    return 0;
}
```

p2 剥夺了 p1的所有权，当程序运行时访问 p1 将会报错。所以auto_ptr的缺点是：存在潜在的内存崩溃问题！



### unique_ptr（独占式）

实现独占式拥有，保证同一时间内只有一个智能指针可以指向该对象。

```cpp
	unique_ptr<std::string> p3  = new string("hello");
    unique_ptr<std::string> p4;
    // p4 = p3;     // 编译时就报错，禁止拷贝
```

编译器认为 p4 = p3 非法，避免了 p3不再指向有效数据的问题



使用：

```cpp
	// 智能指针的创建
    unique_ptr<std::string> p1 (new string("hello"));
    cout << *p1 << endl;        // hello
    
    // p接收了p1释放的内存
    // string* p2 = p1.release();
    // cout << *p2 << endl;        // hello

    // 所有权转移，p1所有权转移后，变成“空指针”
    unique_ptr<std::string> p3 = std::move(p1);
    // 所有权转移，与上式作用相同
    unique_ptr<std::string> p4;
    p4.reset(p1.release());

	if(upt.get()!=nullptr) {				// 判空操作更安全
		// do something
	}

    cout << *p3 << endl;  // hello
```



### share_ptr（共享型，强引用）

共享式拥有概念，多个智能指针可以指向相同对象

对被管理的资源进行引用计数，当一个shared_ptr对象要共享这个资源的时候，该资源的引用计数加1， 当这个对象的生命周期结束的时候，再把该引用计数减1，这样当最后一个引用它的对象被释放的时候，资源的引用计数减少到0，此时释放资源

使用：

```cpp
#include <iostream>
#include <memory>
using namespace std;
class A
{
public:
    int i;
    A(int n):i(n) { };
    ~A() { cout << i << " " << "destructed" << endl; }
};

int main()
{
    shared_ptr<A> sp1(new A(2)); //A(2)由sp1托管，
    shared_ptr<A> sp2(sp1);       //A(2)同时交由sp2托管
    shared_ptr<A> sp3;			
    sp3 = sp2;   //A(2)同时交由sp3托管	多个shared_ptr对象托管同一个指针.
    cout << sp1->i << "," << sp2->i <<"," << sp3->i << endl;
    A * p = sp3.get();      // get返回托管的指针，p 指向 A(2)
    cout << p->i << endl;  //输出 2
    sp1.reset(new A(3));    // reset导致托管新的指针, 此时sp1托管A(3)
    sp2.reset(new A(4));    // sp2托管A(4)
    cout << sp1->i << endl; //输出 3
    sp3.reset(new A(5));    // sp3托管A(5),A(2)无人托管，被delete
    cout << "end" << endl;
    return 0;
}
```

输出：

```
2,2,2
2
3
2 destructed
end
5 destructed
4 destructed
3 destructed
```



### weak_ptr（弱引用）

不控制对象生命周期的智能指针，它指向一个share_ptr管理的对象

设计的目的是为了协助 share_ptr工作，解决share_ptr 相互引用时的死锁问题（两个share_ptr相互引用，那么这两个指针的引用计数永远不可能降为0，也就是资源永远不会释放）

它和share_ptr 之间可以相互转化，share_ptr可以直接赋值给它，它可以通过调用lock函数来获得share_ptr

 当两个智能指针都是 shared_ptr 类型的时候，析构时两个资源引⽤计数会减⼀，但是两者引⽤计数还是为 1，导 致跳出函数时资源没有被释放（的析构函数没有被调⽤），解决办法：把其中⼀个改为weak_ptr就可以 

用法：

```cpp
weak_ptr<T> w;	 	//创建空 weak_ptr，可以指向类型为 T 的对象
weak_ptr<T> w(sp);	//与 shared_ptr 指向相同的对象，shared_ptr 引用计数不变。T必须能转换为 sp 指向的类型
w=p;				//p 可以是 shared_ptr 或 weak_ptr，赋值后 w 与 p 共享对象
w.reset();			//将 w 置空
w.use_count();		//返回与 w 共享对象的 shared_ptr 的数量
w.expired();		//若 w.use_count() 为 0，返回 true，否则返回 false
w.lock();			//如果 expired() 为 true，返回一个空 shared_ptr，否则返回非空 shared_ptr
```

## 比起auto_ptr，unique_ptr拥有的功能

（a）unique_ptr可放在容器中，弥补了auto_ptr不能作为容器元素的缺点

```cpp
// 方式一
vector<unique_ptr<string>> vs { new string{“Doug”}, new string{“Adams”} };  

// 方式二
vector<unique_ptr<string>>v;  
unique_ptr<string> p1(new string("abc")); 
```

（b) 管理动态数组， 因为 unique_ptr 有 unique_ptr<X[]> 重载版本，销毁动态对象时调用 delete[] 

```cpp
unique_ptr<int[]> p (new int[3]{1,2,3});  
p[0] = 0;// 重载了operator[]
```

 （c) 自定义资源删除操作（Deleter）。unique_ptr 默认的资源删除操作是 delete/delete[]，若需要可以进行自定义： 

```cpp
void end_connection(connection *p) { disconnect(*p); } // 资源清理函数  

// 资源清理器的类型
unique_ptr<connection, decltype(end_connection)*> p(&c, end_connection);// 传入函数名，会自动转换为函数指针
```

## 参考链接

 [(21条消息) C++ STL 四种智能指针_Dablelv的博客专栏-CSDN博客_stl 智能指针](https://blog.csdn.net/K346K346/article/details/81478223) 

# 队列如果满了，产生积压的情况

1. 增加消费者，增加消费速度
2. 扩容
3. 丢弃不重要的信息

# const常量

>  const int a = 100;

**const常量与#define宏定义常量的区别：**

const常量具有数据类型，编译器可以进行安全检查；#define宏定义没有数据类型，只是简单的字符串替换，不能进行安全检查

**作用**：防止修改，起保护作用，增加程序健壮性。节省空间，避免不必要的内存分配。

const定义的常量在程序运行阶段只有一份拷贝，而#define定义的常量在内存中有若干个拷贝

**const对象默认为文件局部变量**，要使const变量能够在其他文件中访问，必须在文件中**显式地指定它为extern**。  非const变量默认为extern。 

常量在定义后就不能修改，所以定义时必须初始化

**指针与const**

如果const位于*的左侧，则const就是用来修饰指针所指向的变量，即指针指向为常量

如果const位于*的右侧，const就是修饰指针本身，即指针本身为常量

**函数中使用const**

const修饰函数返回值，const修饰形参列表， const在函数后面

const对象只能访问const成员，常函数不可以修改成员属性

