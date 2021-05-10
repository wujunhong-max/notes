# 怎么用linux查找文件

> # find -name test.file
>
> 这样他就会查找test.file文件
>
> 也可以指定某个目录
>
> find /var -name test.file

# 查看连接树莓派的摄像头设备名

> ls /dev/video*

# 怎么查看Linux进程id

>  ps -ef | grep "***"

# 查看Linux下的ip

> ifconfig 

# 给文件赋权

输入命令【chmod 777 文件名称】，赋权文件rwx，可读可写可执行权限

# Linux中删除文件

rm  [选项] 文件名

-f, --force 强制删除。忽略不存在的文件，不提示确认
-i 在删除前需要确认
-r, -R, --recursive 递归删除目录及其内容
-v, --verbose 详细显示进行的步骤

# 给文件改名

输入命令:mv 修改前文件名 修改后文件名,按回车。

# 查看连接网线上的ip

> apr -a

## Vim的操作

按esc键进入命令行模式，输入【:wq 】保存文件退出

- i：在当前光标的前面插入字符
- a：在当前光标的后面追加字符
- u：撤销上一次操作