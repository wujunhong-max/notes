//这个是UDP协议聊天程序的服务器
//1.创建socket
//2.为socket绑定地址
//3.接受数据
//4.发送数据
//5.关闭socket
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<errno.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<arpa/inet.h>

int main(int argc, char *argv[])
{
    if(argc!=3)
    {
        printf("please input: udp ip port\n");
        return -1;
    }

    int sockfd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if(sockfd<0)
    {
        perror("socket error\n");
        //将上一个函数发生错误的原因输出
        //将你输入的一些信息和errno所对应的错误一起输出。
        return -1;
    }
    struct sockaddr_in ser_addr;
    ser_addr.sin_family = AF_INET;
    ser_addr.sin_port = htons(atoi(argv[2]));
    ser_addr.sin_addr.s_addr = inet_addr(argv[1]);
    socklen_t len = sizeof(struct sockaddr_in);

    int ret = bind(sockfd, (struct sockaddr *)&ser_addr, len);
    if(ret<0)
    {
        perror("bind error\n");
        close(sockfd);
        return 0;
    }
    while(1)
    {
        char buff[1024] = {0};
        struct sockaddr_in cli_addr;
        len = sizeof(struct sockaddr_in);
        ssize_t rlen = recvfrom(sockfd, buff, 1023, 0, (struct sockaddr *)&cli_addr, &len);
        if(rlen<0)
            {
                perror("recvfrom error\n");
                close(sockfd);
                return -1;
            }
            printf("client:%s %d say:%s\n", inet_ntoa(cli_addr.sin_addr), ntohs(cli_addr.sin_port), buff);
            memset(buff, 0x00, 1024);
            scanf("%s", buff);
            sendto(sockfd, buff, strlen(buff), 0, (struct sockaddr *)&cli_addr, len);
    }
    close(sockfd);
    return -1;
}