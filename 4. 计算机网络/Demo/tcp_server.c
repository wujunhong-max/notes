//这是TCP协议来实现服务端的程序
//1.创建socket
//2.为socket绑定地址
//3.开始监听，可以接受客户端的链接请求
//4.获取连接成功的socket
//5.接受数据
//6.发送数据
//7.关闭socket
//
//标准头文件
#include<stdio.h>
// 标准输入输出头文件
//动态内存相关的malloc,realloc,zalloc,calloc,free等
#include<stdlib.h>
//用于linux/unix系统的调用
#include<unistd.h>
/*定义了通过错误码来回报错误信息的宏
    提供错误号errno的定义，用于错误处理
    errno本身是一个整型的全局变量，当使用errno的库函数，在执行出错时，只通过函数
    返回值返回一个表示出错的标识，如-1或NULL等，具体的出错原因会被赋值到errno中。
    通过查询errno可以确定具体的出错原因。*/
#include<errno.h>
/*内存处理及字符串处理函数
1 .内存处理相关函数，包括memcmp, memcpy, memset等。
2 .字符串处理函数，包括strcpy, strcmp, strlen,strstr等*/
#include<string.h>
// linux系统下提供socket函数及数据结构
#include<sys/socket.h>  
/*互联网地址族
1.定义socketaddr_in 结构体
*/
#include<netinet/in.h>
//提供IP地址转换函数
#include<arpa/inet.h>
 
 /*main( int argc, char* argv[], char **env ) 是UNIX、Linux以及Mac OS
 操作系统中C/C++的main函数标准写法
 第一个参数：统计程序运行时发送给main函数的命令行参数的个数，在VS中默认值为1
 第二个参数：用来存放指向的字符串参数的指针数组，每一个元素指向一个参数。各成员含义如下： 
        argv[0]指向程序运行的全路径名 
        argv[1]指向在DOS命令行中执行程序名后的第一个字符串 
        argv[2]指向执行程序名后的第二个字符串 
        argv[3]指向执行程序名后的第三个字符串 
        argv[argc]为NULL 
    第三个参数：char**型的env，为字符串数组。env[]的每一个元素都包含ENVVAR=value形式的字符串，
    其中ENVVAR为环境变量，value为其对应的值。平时使用到的比较少。*/
int main(int argc,char *argv[])
{
   if(argc!=3)
   {
       printf("please input:tcp ip port\n");
       return -1;                    //表示该函数失败
   }
   /*AF_INET又称PF_INET,是IPv4网络协议的套接字类型
   第一个参数：套接字中使用的协议族（Protocol Family）信息
                            （IPV4，IPV6,本地通信的协议族，底层套接字的协议族,IPX Novel协议族）
                            （PF_INET, PF_INET6, PF_LOCAL, PF_PACKET, PF_IPX ）
   第二个参数：套接字数据传输类型信息(面向连接还是面向消息)
                                (SOCK_STREAM，SOCK_DGRAM)
    第三个参数：主要是作为第一个，第二个参数无法指定类型的时的一种附加
                                (IPPROTO_TCP,IPPROTO_UDP)
    */
   int sockfd=socket(AF_INET,SOCK_STREAM,IPPROTO_TCP);
   if(sockfd<0)
   { 
      perror("socker error\n");
      return -1;
   }
   struct sockaddr_in ser_addr;
   ser_addr.sin_family=AF_INET; //IP地址家族
   ser_addr.sin_port=htons(atoi(argv[2]));      //填写端口    //atoi：将str所指字符串转换为int型整数。
   //htons：host to network short  字节转换函数，短整数从主机字节序到网络字节序的转换
   //短整型占两个字节，范围从0到65535或-32768到32767
   //短型（两个字节）和长型（四个字节）
   ser_addr.sin_addr.s_addr=inet_addr(argv[1]);         //填写IP
   //inet_addr函数，将点分十进制的IP转换为网络字节序的长整型数
   socklen_t len=sizeof(struct sockaddr_in);        
   int ret=bind(sockfd,(struct sockaddr*)&ser_addr,len);//bind设置对象，绑定IP地址和端口
   /*int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen)
   第一个参数：创建新套接字socket返回的文件描述符
   第二个参数：绑定 IP地址 和 端口号 给 sockfd ，指向含有本机 IP 地址及端口号等信息的 sockaddr 类型
   的指针，指向要绑定给sockfd 的协议地址结构，这个地址结构根据创建 socket 时的地址协议族的不同而不同
   &ser_addr是ser_addr的地址
   （struct sockaddr*）是把ser_addr的地址强制转换为sockaddr*类型
   */
   if(ret<0)
   {
   perror("bind error\n");
   return -1;
   }
   //服务端开始监听 这时候服务端可以请求链接
   // int listen(int sockfd,int backlog)
   //sockfd:socket系统调用返回服务端的 socket 描述符
   //backlog:指可以连接该服务端的最大个数，设置网络访问的请求最大值
   if(listen(sockfd,5)<0)
   {
      //listen 函数服务端用来监听
      //第一个参数为socket描述符
      //第二个参数为 最大的同时并发连接数
      perror("listen error\n");
      return -1;
   }
   while(1)
   {
      int new_sockfd; 
      struct sockaddr_in addr;
      len=sizeof(struct sockaddr_in);
      new_sockfd=accept(sockfd,(struct sockaddr*)&addr,&len);
      //获取连接成功的socket int accept
      //第一个参数为socket描述符
      //第二个参数为新建立链接的客户端地址信息
      //第三个参数为地址信息的长度,是指针，加上&
      //返回值如果成功返回新的描述符，如果失败返回-1
      //accept是一个阻塞函数链接成功队列中如果没有新的链接
      //那就会一直阻塞直到有新的客户端链接到来
      //这里我们通过创建新的socket来接受数据
      //客户端发送的数据都在这个新的socket缓冲区中
      //以前的socket被用来处理链接，链接成功的socket
      //发送数据都在新的socket的缓冲区
      if(new_sockfd<0)
      {
          perror("accept error\n");
          continue;//这里不能直接退出，因为这个链接失败了可以链接别的socket
      }
      printf("new socket:%s,%d,\n",inet_ntoa(addr.sin_addr),ntohs(addr.sin_port));
      //这里我们输出一下链接过来的socket的ip地址和port端口号
      //inet_ntoa将网络字节序IP（结构体in_addr型）转化为点分十进制的IP地址
      while(1)
      {
          //接受数据
          char buff[1024]={0};
          ssize_t rlen=recv(new_sockfd,buff,1023,0);
          //recv 接受数据 
          //第一个为sockfd描述符
          //第二个参数为接受数据的缓冲区, 指针
          //第三个为接受数据的长度，1023可能是因为char中有个'/0'
          //第四个参数为0是代表阻塞式接受
          //对于返回值有三种情况 如果错误返回-1，链接关闭返回0，正确的话返回的是接受的长度
          if(rlen<0)
          {
              perror("recv error\n");
              close(new_sockfd);
              continue;//这里和客户端不同不能直接关闭你的程序
          }
          else if(rlen==0)
          {
              printf("perr shutdown\n");
              close(new_sockfd);
              continue;//如果返回0的话代表那个链接断开了
          }
          printf("client %s:%d say:%s\n",inet_ntoa(addr.sin_addr),ntohs(addr.sin_port),buff);
          //发送数据
          memset(buff,0x00,1024);
          //用于初始化（清空）一个内存块
          //用第二个参数的值去填充第一个参数指向的内存块,
         //填充长度即为第三个参数
          scanf("%s",buff);
          //%s是表示从键盘输入一个字符串到buff，buff是地址
          send(new_sockfd,buff,strlen(buff),0);
      }
   }
 
     close(sockfd);
     return 0;
}