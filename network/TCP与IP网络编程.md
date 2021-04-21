# TCP与IP网络编程

## 第一章   理解网络编程和套接字

### 1.1理解网络编程和套接字

- 网络编程就是编写程序使两台连网的计算机相互交换数据
- 套接字（socket）：网络数据传输用的软件设备

#### 调用socket函数（相当于安装电话机）

```c
#include<sys/socket.h>
int socket(int domain, int type, int protocol);
成功时返回文件描述符，失败时返回-1
```

#### 调用bind函数（分配电话号码）

```c
# 用该函数给创建好的套接字分配地址信息（IP地址和端口号）
#include<sys/socket.h>
int bind(int sockfd, struct sockaddr *myaddr, socklen_t addrlen);
成功时返回0，失败时返回-1
```

#### 调用listen函数(连接电话线)

```c
# 这时其他人可以请求连接到该机，同样，需要把套接字转化成可接收连接的状态
#include<sys/socket.h>
int listen(int sockfd, int backlog);
成功时返回0，失败时返回-1
```

#### 调用accept函数(拿起话筒)

```c
# 如果有人请求连接，就调用以下函数受理
#include<sys/socket.h>
int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);
成功时返回文件描述符，失败时返回-1
```

#### 小总结

1.调用socket函数创建套接字

2.调用bind函数分配IP地址和端口号

3.调用listen函数转为可接收请求状态

4.调用accept函数受理连接请求

#### 在Linux平台下运行

编写一个hello_server服务端和hello_client客户端

```
gcc hello_server.c -o hserver
# 编译hello_server.c文件并生成可执行文件hserver
./hserver
# 运行当前目录下的hserver文件

#另外开一个终端
gcc hello_client.c -o hclient
./hclient 127.0.0.1 9190 
# 127.0.0.1是ip地址，9190是端口号
```

### 1.2基于Linux的文件操作

- **linux系统不区分文件和套接字 **，所以在linux系统中可以用文件I/O的相关函数

- window系统就有区分，因此在window中需要调用特殊的数据传输相关函数

**文件描述符**是系统分配给文件或套接字的整数

#### 打开文件

#### 关闭文件

#### 将数据写入文件

#### 读取文件中的数据

#### 文件描述符与套接字











