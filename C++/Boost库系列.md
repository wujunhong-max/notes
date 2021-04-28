# 并发编程

## 一、Boost.Asio入门

### 定义

Boost.Asio是一个跨平台的、主要用于网络和其他一些底层输入/输出编程的C++库。

Boost.Asio在网络通信、COM串行端口和文件上成功地抽象了输入输出的概念。你可以基于这些进行同步或者异步的输入输出编程。

```c++
read(stream, buffer [, extra options])
async_read(stream, buffer [, extra options], handler)
write(stream, buffer [, extra options])
async_write(stream, buffer [, extra options], handler)
```

从前面的代码片段可以看出，这些函数支持传入包含任意内容（不仅仅是一个socket，我们可以对它进行读写）的流实例。

作为一个跨平台的库，Boost.Asio可以在大多数操作系统上使用。能同时支持数千个并发的连接。其网络部分的灵感来源于**伯克利软件分发(BSD)socket**，它提供了一套可以支持**传输控制协议(TCP)**socket、**用户数据报协议(UDP)**socket和**Internet控制消息协议(IMCP)**socket的API，而且如果有需要，你可以对其进行扩展以支持你自己的协议。

### 依赖

Boost.Asio依赖于如下的库：

- **Boost.System**：这个库为Boost库提供操作系统支持(http://www.boost.org/doc/libs/1_51_0/doc/html/boost_system/index.html)
- **Boost.Regex**：使用这个库（可选的）以便你重载*read_until()*或者*async_read_until()*时使用*boost::regex*参数。
- **Boost.DateTime**：使用这个库（可选的）以便你使用Boost.Asio中的计时器
- **OpenSSL**：使用这个库（可选的）以便你使用Boost.Asio提供的SSL支持。

### 同步VS异步

首先，异步编程和同步编程是非常不同的。在同步编程中，所有的操作都是顺序执行的，比如从socket中读取（请求），然后写入（回应）到socket中。每一个操作都是阻塞的。因为操作是阻塞的，所以为了不影响主程序，当在socket上读写时，通常会创建一个或多个线程来处理socket的输入/输出。因此，**同步的服务端/客户端通常是多线程的**。

相反的，异步编程是事件驱动的。虽然启动了一个操作，但是你不知道它何时会结束；它只是提供一个回调给你，当操作结束时，它会调用这个API，并返回操作结果。因此，**在异步编程中，你只需要一个线程**。



因为中途做改变会非常困难而且容易出错，所以你在项目初期（最好是一开始）就得决定用同步还是异步的方式实现网络通信。不仅API有极大的不同，你程序的语意也会完全改变（异步网络通信通常比同步网络通信更加难以测试和调试）。你需要考虑是采用阻塞调用和多线程的方式（同步，通常比较简单），或者是更少的线程和事件驱动（异步，通常更复杂）。

- 一个基础的同步客户端例子

```c++
using boost::asio;
 //先创建一个io_service实例。Boost.Asio使用io_service同操作系统的输入/输出服务进行交互。通常一个io_service的实例就足够了
io_service service;       
ip::tcp::endpoint ep( ip::address::from_string("127.0.0.1"),2001);  //创建你想要连接的地址和端口
ip::tcp::socket sock(service);  // 建立socket
sock.connect(ep);       //把socket连接到你创建的地址和端口
```

- 简单的使用Boost.Asio的服务端

```c++
typedef boost::shared_ptr<ip::tcp::socket> socket_ptr;
io_service service;							//创建一个io_service 实例
ip::tcp::endpoint ep(ip::tcp::v4(), 2001);	//指定想要监听的端口
ip::tcp::acceptor acc(service, ep);		//创建一个接收器-------- 一个用来接收客户端连接的对象
while(true)
{
	socket_ptr sock(new ip::tcp::socket(service));		//创建虚拟的socket等待客户端的连接，用智能指针sock保存新创建的地址
	acc.accept(*sock);									// 接收连接
	boost::thread( bost::bind(client_session, sock));	// 创建一个线程来处理这个连接
}
void client_session(socket_ptr sock)		// 读取一个客户端的请求，进行解析，然后返回结果
{
	while( true)
	{
		char data[512];
		size_t len = sock->read_some(buffer(data));
		if(len > 0)
			write(*sock,buffer("ok",2));
	}
}
```

- 创建一个异步客户端















