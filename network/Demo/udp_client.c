//我们通过udp协议来实现一个简单的网络聊天程序
//这是客户端的实现
//过程：
//    1.创建套接字
//    2.绑定地址信息
//    3.向服务端发送数据
//    4.接受服务端发送的数据
//    5.关闭socket
 
#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<string.h>
#include<errno.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<arpa/inet.h>
 
int main()
{
    int sockfd=socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP);
    //socket函数第一个参数为地址类型，目前只支持apra类型的地址
    //第二个参数是套接字类型 如果是SOCK_DGRAM 面向数据报的套接字
    //如果是SOCK_STREAM则是面向数据流的套接字 不
    //第三个参数是用来指定具体协议，不想指定可以省略为0 默认数据报套接字为udp 数据流为tcp
    //这里我们指定了IP协议族中的UDP协议。
    if(sockfd<0)
    {
        perror("socket error\n");
        return -1;
    }
    //绑定地址信息，不过在客户端的时候我们通常不绑定
    //因为绑定的话可能会因为一些特殊情况失败，但是
    //客户端发送数据的时候使用哪个地址和端口都无所谓
    //只要数据能够发送成功就可以，所以客户端时我们一般
    //不推荐绑定端口，这样在发送数据的时候，操作系统检测
    //到socket还没有绑定地址，就会自动给他绑定一个这样
    //绑定方式不会出错。
    //
    struct sockaddr_in cli_addr;
    //sockaddr_in 是一个结构体解决了sockaddr的缺陷
    //里边有四个成员变量分别是：
    //sin_family   存储地址族
    //sin_port 16位TCP/UDP端口号
    //sin_addr 32位IP地址
    //sin_zeor[8]  我们不会使用到
    cli_addr.sin_family=AF_INET;
    cli_addr.sin_port=htons(9000);
    cli_addr.sin_addr.s_addr=inet_addr("192.168.76.130");
    socklen_t len=sizeof(struct sockaddr_in);
    while(1)
    {
        //3.发送数据
        char buff[1024]={0};
        scanf("%s",buff);
        sendto(sockfd,buff,strlen(buff),0,(struct sockaddr*)&cli_addr,len);
        //sendto 指向一指定的目的地发送数据
        //第一个参数是我们套接字操作符
        //第二个参数是要发送的数据
        //第三个参数发送的数据长度
        //第四个一般为0，如果缓冲区没有数据那么阻塞等待
        //第五个指针指向目的套接字的地址
        //第六个参数是第五个指针指向的地址长度
        //4.接受来自服务端的数据
        memset(buff,0x00,1024);//把缓冲区变成0以防刚刚的数据影响现在新接受的数据
        ssize_t r_len=recvfrom(sockfd,buff,1023,0,(struct sockaddr*)&cli_addr,&len);
        //recvfrom 是通过sock来接受数据的函数
        //参数和上边的相同不过这里第六个参数也是指针指向缓冲区的长度
        //如果成功返回的是接受的字节数，失败返回-1
         if(r_len<0)
         {
             perror("recvfrom error\n");
             return 0;
         }
         printf("server say:%s\n",buff);
    }
    close(sockfd);
    return 0;
}