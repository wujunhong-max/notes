//实现最简单的http服务端程序
//返回hello world
//http是应用协议，在传输层使用的是tcp协议,所以我们的程序本质上是tcp服务器
//我们http指定监听10000端口，所以在请求访问的时候也要手动指定否则默认80端口
#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<string.h>
#include<errno.h>
#include<sys/socket.h>
#include<netinet/in.h>

int main(int argc,char* argv[])
{
    int sockfd = socket(AF_INET,SOCK_STREAM,IPPROTO_TCP);
    if(sockfd < 0)
    {
        perror("socket error\n");
        return -1;
    }
    struct sockaddr_in lst_addr;
    lst_addr.sin_family = AF_INET;
    lst_addr.sin_port = htons(9998);
    lst_addr.sin_addr.s_addr = inet_addr("192.168.186.128");
    socklen_t len = sizeof(struct sockaddr_in);
    int ret = bind(sockfd,(struct sockaddr*)&lst_addr,len);
    if(ret<0)
    {
        perror("bind error\n");
        return -1;
    }
    if(listen(sockfd,5)<0)
    {
        perror("listen error\n");
        return -1;
    }
    while(1)
    {
        struct sockaddr_in cli_addr;
        int newfd = accept(sockfd,(struct sockaddr*)&cli_addr,&len);、
        if(newfd < 0)
        {
            perror("accept error\n");
            continue;
        }
        char buff[1024] = {0};
        int ret = recv(newfd,buff,1023,0);
        if(ret>0)
        {
            printf("req:%s\n",buff); //这里我们打印的是浏览器HTTP的请求头部
        }
        //返回的http头部信息要包括
        //首行  HTTP/1.1 200 OK
        //头信息
        // 空行
        // 正行
        char *rsp = "<h1>hello world</h1>";
        memset(buff,0x00,1024);
        
        sprintf(buff,"%s\r\n%s%d\r\n%s\r\n\r\n%s%","HTTP/1.1 200 OK","Content-Length:",strlen(rsp),"Content-Type:text/html:charset=UTF-8",rsp);
        // 这里我们返回的是简单的字符串hello world          // %s \r\n   第一行输入了HTTP/1.1 200 OK
        // %s %d \r\n 这里第二行输出了Content-Length：strlen(rsp) 这里我们是向通过这个关键字告诉浏览器我们这次发送的数据是多少
        // %s \r\n 这一行输出了Content-Type:text/html:Charset = UTF-8 是告诉浏览器我们的文件格式和编码格式
        // \r\n 这一行是HTTP头部和正文之间的空行
        // %s 这里才是我们最终传输的数据
        // 这一部分的内容才真正算是我们的HTTP协议的部分，这里是我们用HTTP协议和浏览器交流的部分。
        printf("%s",buff);
        send(newfd,buff,strlen(buff),0);
        close(newfd);
    }
}