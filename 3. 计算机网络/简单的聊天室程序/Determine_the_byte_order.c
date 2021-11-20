//检查机器的字节序
//运行后我的机器是小端字节序
#include<stdio.h>
int main()
{
    union 
    {
        short value;
        char union_bytes[sizeof(short)];
    } test;
    test.value = 0x0102;
    if((test.union_bytes[0] == 1 )&&(test.union_bytes[1] == 2))
    {
        printf("big endian\n");
    }
    else if((test.union_bytes[0] == 2)&&( test.union_bytes[1] == 1))
    {
        printf("little endian\n");
    }
    else
    {
        printf("unknown...\n");
    }
}
