# windows10里命令行的使用

## 修改hosts文件

```bash
以管理员身份进入CMD
输入命令“cd C:\Windows\System32\drivers\etc"，回车，进入hosts文件目录
输入命令“notepad hosts"，回车，用记事本打开hosts
修改并保存
```

更新DNS缓存

```bash
ipconfig /flushdns
```

