//这是一个通过TCP协议来实现聊天的程序
//1.创建socket
//2.为socket绑定地址
//3.向服务端发送链接请求
//4.发送数据
//5.接受数据
//6.断开连接
//
 
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<errno.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<arpa/inet.h>
#include<unistd.h>
 
int main(int argc,char *argv[])
{
    if(argc!=3)
    {
        printf("please input:tcp ip port\n");
        return -1;
    }
    int sockfd=socket(AF_INET,SOCK_STREAM,IPPROTO_TCP);
    if(sockfd<0)
    {
        perror("socket error\n");
        return -1;
    }
    //2.和UDP协议一样客户端不推荐绑定端口地址
    //3.向服务器端发送链接请求
    struct sockaddr_in cli_addr;
    cli_addr.sin_family=AF_INET;
    cli_addr.sin_port=htons(atoi(argv[2]));
    cli_addr.sin_addr.s_addr=inet_addr(argv[1]);
    //通过命令行参数来给结构体赋值
    socklen_t len=sizeof(struct sockaddr_in);
    int ret=connect(sockfd,(struct sockaddr*)&cli_addr,len);
    //connect 向服务端发送链接请求
    //第一个参数是sockfd也就是操作描述符
    //第二个参数为要连接的服务器地址
    //第三个参数为地址信息的长度
    //返回值如果成功为0，失败为-1
    if(ret<0)
    {
      perror("connect error\n");
      return -1;
    }
    while(1)
    {
        //发送数据
        char buff[1024]={0};
        scanf("%s",buff);
        send(sockfd,buff,strlen(buff),0);
        //send 函数用来给已经链接的socket发送数据
        //第一个参数为sockfd 操作符
        //第二个参数为发送的数据
        //第三个参数为发送的数据长度
        //第四个参数为执行方式0位阻塞
        //
        //接受数据
        memset(buff,0x00,1024);
        ssize_t rlen=recv(sockfd,buff,1023,0);
        //recv  函数用来接受已经链接的socket接受数据
        //第一个参数是sockfd操作符
        //第二个参数为接受数据的缓冲区
        //第三个参数为接受数据的长度
        //第四个参数0为阻塞接受
        if(rlen<=0)
        {
            perror("recv error\n");
            return -1;
        }
        printf("server say:%s",buff);
 
 
    }
    close(sockfd);
    return 0;
 
}