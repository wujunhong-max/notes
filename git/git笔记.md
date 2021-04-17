# 一、安装git


在windows上使用git，在git官网上下载安装包，然后安装。
安装完成后，在开始菜单里找到“Git”->“Git Bash”，蹦出一个类似命令行窗口的东西，就说明Git安装成功！

在命令行输入：

```bash
$ git config --global user.name "Your Name"
$ git config --global user.email "email@example.com"
```
注意git config命令的`--global`参数，用这个参数表示你这台机器上所有的Git仓库都会使用这个配置，当然也可以对某个仓库指定不同的用户名和Email地址。

# 二、创建版本库
1.创建一个版本库非常简单，首先，选择一个合适的地方，创建一个空目录

```bash
$ mkdir learngit	//新建文件夹learngit
$ cd learngit		//进入该文件夹
$ pwd				//显示当前目录
/Users/michael/learngit
```

2.初始化一个Git仓库，使用`git init`命令

<font color=#999AAA >测试如下：此时会多了一个`.git`目录，这个目录是Git来跟踪管理版本库的。没事不要乱动。
如果你没有看到`.git`目录，那是因为这个目录默认是隐藏的，用`ls -ah`命令就可以看见。

3.添加文件到Git仓库，分两步：

```bash
a.使用命令git add <file>，注意，可反复多次使用，添加多个文件；
b.使用命令git commit -m "备注"
```
`commit`可以一次提交很多文件，所以你可以多次`add`不同的文件
# 三、修改和删除文件
## 1. 通过命令观察修改
1.可以通过`git status`命令掌握工作区的状态
2.如果`git status`告诉你有文件被修改过，用`git diff`可以查看修改内容

![图片](https://img-blog.csdnimg.cn/2021022315335313.png)
<font color=#999AAA >测试如下：我修改了git_learn.txt文件，使用git status命令可以看到红色字体modified标出了修改的文件
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210223153731463.png)
输入了`git diff`命令，通过观察红色字体和绿色字体得出我添加了3个0

3.然后重新提交

```bash
git add git_learn.txt
```

<font color=#999AAA >输入`git status`查看下，`git status`告诉我们，将要被提交的修改包括readme.txt,我们就可以放心提交了
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210223154230516.png)

```bash
git commit -m "add 000"
```
<font color=#999AAA >再输入`git status`查看仓库的状态，Git告诉我们当前没有需要提交的修改，而且，工作目录是干净（working tree clean）的
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210223154610530.png)
## 2. 版本回退
1.每次`commit`相当于一次存档，一旦你把文件改乱了，或者误删了文件，还可以从最近的一个`commit`恢复，然后继续工作
2.用`git log`可以查看提交历史，以便确定要回退到哪个版本
3.Git允许我们在版本的历史之间穿梭，使用命令`git reset --hard commit_id`。
 HEAD指向的版本就是当前版本，上一个版本就是`HEAD^`，上上一个版本就是`HEAD^^`，当然往上100个版本写`100个^`比较容易数不过来，所以写成`HEAD~100`
4.如果我们要重返未来，用`git reflog`查看命令历史，以便确定要回到未来的哪个版本

<font color=#999AAA >测试如下：
可以看到我上传了2次
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210223160800774.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NjgxOTI0OQ==,size_16,color_FFFFFF,t_70)
如果嫌输出信息太多，看得眼花缭乱的，可以试试加上--pretty=oneline参数：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210223161047863.png)
现在将版本后退到上一个版本`第一次上次`，并查看下内容

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210223161653688.png)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210223161716993.png)
<font color=#999AAA >让我们用`git log`查看下此时版本库的状态
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210223162023441.png)对比上一次，可以看出最新的那个版本`add 000`已经看不到了。但是我们只要往上找到之前最新版本的`commit id`，就可以返回。版本号没必要写全，前几位就可以了，Git会自动去找。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210223162528554.png)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210223162544385.png)
如果我们回退版本，关闭了电脑，第二天早上就后悔了，想恢复到新版本怎么办？找不到新版本的commit id怎么办？
不用担心，Git提供了一个命令`git reflog`用来记录你的每一次命令：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210223163206253.png)
这样我们就找到新版本的`commit id`了

## 3. 工作区和暂存区
工作区（Working Directory）：你在电脑里能看到的目录，比如我的learngit文件夹就是一个工作区
工作区有一个隐藏目录.git，这个不算工作区，而是`Git的版本库`
Git的版本库里存了很多东西，其中最重要的就是称为stage（或者叫index）的`暂存区`，还有Git为我们自动创建的==第一个分支==`master`，以及指向master的一个指针叫HEAD。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210223220404928.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NjgxOTI0OQ==,size_16,color_FFFFFF,t_70)
第一步是用git add把文件添加进去，实际上就是把文件修改添加到暂存区；

第二步是用git commit提交更改，实际上就是把暂存区的所有内容提交到当前分支；

现在我的工作区有2个文件，一个上传到分支，一个没有。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210223223038304.png)
LICENSE还从来没有被添加过，所以它的状态是`Untracked`
将该文件git add后
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210223223254286.png)
再将文件git commit 后，git status查看
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210223223529246.png)
一旦提交后，如果你又没有对工作区做任何修改，那么工作区就是“干净”的：
## 4. 管理修改
Git跟踪并管理的是修改，而非文件。
每次修改文件，如果不用git add到暂存区，那就不会加入到commit中。
git commit只会将暂存区的文件提交到分支。

比如：
第一次修改 -> `git add `-> 第二次修改 -> `git commit`
则只会提交第一次修改
提交后，用`git diff HEAD -- filename`命令可以查看工作区和版本库里面最新版本的区别;

改善：
第一次修改 -> `git add `-> 第二次修改 ->` git add` -> `git commit`

## 5. 撤销修改
场景1：当你改乱了工作区某个文件的内容，想直接丢弃工作区的修改时，用命令`git checkout -- file`
若文件添加到暂存区后，又作了修改，撤销修改就回到添加到暂存区后的状态，也用命令`git checkout -- file`

场景2：当你不但改乱了工作区某个文件的内容，还添加到了暂存区时，想丢弃修改，分两步，第一步用命令`git reset HEAD <file>`，就回到了场景1，第二步按场景1操作。

场景3：已经提交了不合适的修改到版本库时，想要撤销本次提交，参考版本回退一节，不过前提是没有推送到远程库

<font color=#999AAA >测试如下：
1.修改后没有add到暂存区
或者文件已经add到暂存区，你修改了文件，想要撤销修改（就是git add和修改文件只进行了一个）
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210223230834488.png)
2.修改后add到暂存区要撤销（既修改了又git add）
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210223231719733.png)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210223231732353.png)
3.已经提交到版本库，进行版本回退



## 6. 删除文件
命令`git rm`用于删除一个文件。如果一个文件已经被提交到版本库，那么你永远不用担心误删，但是要小心，你只能恢复文件到最新版本，你会丢失最近一次提交后你修改的内容

`git checkout`其实是用版本库里的版本替换工作区的版本，无论工作区是修改还是删除，都可以“一键还原”。
但是从来没有被添加到版本库就被删除的文件，是无法恢复的！

<font color=#999AAA >测试如下：
先创建一个新文件new.txt，并提交到版本库

```bash
$ git add new.txt
$ git commit -m "add new.txt"
[master 36ba2a9] add new.txt
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 new.txt
```
一般情况下，你通常直接在文件管理器中把没用的文件删了，或者用rm命令删了

```bash
$ rm new.txt
```
这个时候，Git知道你删除了文件，因此，工作区和版本库就不一致了，显示删除文件new.txt
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210223233101529.png)
有两种选择：
1.确认删除
那就用命令`git rm`删掉，并且`git commit`：

```bash
$ git rm new.txt
rm 'new.txt'

$ git commit -m "remove new.txt"
[master da6da6d] remove new.txt
 1 file changed, 0 insertions(+), 0 deletions(-)
 delete mode 100644 new.txt
```
2.删错了，恢复

```bash
$ git checkout -- test.txt
```
# 四、远程仓库
## 1. 添加远程库

在GitHub上创建仓库，在本地的learngit仓库下运行命令，关联远程库

```bash
$ git remote add origin git@github.com:michaelliao/learngit.git
```
远程库的名字就是`origin`
下一步，就可以把本地库的所有内容推送到远程库上：
使用命令`git push -u origin master`第一次推送master分支的所有内容；

此后，每次本地提交后，只要有必要，就可以使用命令`git push origin master`推送最新修改；

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210224003603420.png)

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210224003615514.png)

<font color=#999AAA >添加ssh秘钥（一次就行）：
输入命令`ssh-keygen`，然后三次回车。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210224003736297.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NjgxOTI0OQ==,size_16,color_FFFFFF,t_70)![在这里插入图片描述](https://img-blog.csdnimg.cn/20210224003843443.png)将这些内容复制粘贴到GitHub网站的settings的SSH and GPG keys的ssh keys中。

## 2. 从远程库克隆
要克隆一个仓库，首先必须知道仓库的地址，然后使用`git clone`命令克隆。

Git支持多种协议，包括`https`，但`ssh`协议速度最快

<font color=#999AAA >测试如下：

```bash
$ cd ..   		//返回上一级目录
$ ls				//查看该目录下的文件
$ mkdir pyqt		//新建文件夹
$ cd pyqt			//进入该文件夹
$ git clone git@github.com:wujunhong-max/PyQt.git
$ cd PyQt			//进入克隆的仓库
$ ls				//查看文件
$ git pull			//能将本地的代码更新至远程仓库 
					 里面最新的代码版本，能更新分支
```
git clone克隆仓库很慢，可以使用GitHub的镜像地址：即在github.com后面加cnpmjs.org这句

```bash
git clone https://github.com.cnpmjs.org/你的GitHub名字/项目名称
```

# 五、分支管理
## 1. 创建与合并分支
查看分支：`git branch`

创建分支：`git branch <name>`

切换分支：`git checkout <name>`或者`git switch <name>`

创建+切换分支：`git checkout -b <name>`或者`git switch -c <name>`

合并某分支到当前分支：`git merge <name>`

删除分支：`git branch -d <name>`

<font color=#999AAA >测试如下：
创建新分支dev，对文件进行修改，提交到dev上.

```bash
$ git checkout -b dev
Switched to a new branch 'dev'
```
<font color=#999AAA >`git checkou`t命令加上-b参数表示创建并切换，相当于以下两条命令：

```bash
$ git branch dev
$ git checkout dev
Switched to branch 'dev'
```
<font color=#999AAA >然后，用`git branch`命令查看当前分支：

```bash
$ git branch
* dev
  master
```
`git branch`命令会列出所有分支，当前分支前面会标一个*号
<font color=#999AAA >然后，我们就可以在dev分支上正常提交，比如对git_learn.txt做个修改,然后提交：

```bash
$ git add git_learn.txt 
$ git commit -m "branch test"
[dev b17d20e] branch test
 1 file changed, 1 insertion(+)
```
<font color=#999AAA >切换回master分支后，再查看一个git_learn.txt文件，刚才添加的内容不见了！因为那个提交是在dev分支上，而master分支此刻的提交点并没有变,所以我们要把dev分支的工作成果合并到master分支上

```bash
$ git merge dev
Updating d46f35e..b17d20e
Fast-forward
 readme.txt | 1 +
 1 file changed, 1 insertion(+)
```
`git merge`命令用于合并指定分支到当前分支
`Fast-forward`信息，Git告诉我们，这次合并是“快进模式”
<font color=#999AAA >合并完成后，就可以放心地删除dev分支了：

```bash
$ git branch -d dev
Deleted branch dev (was b17d20e).
```
## 2. 解决冲突
当两个分支的相同文件进行了不同的修改，Git无法自动合并分支时，就必须首先解决冲突。解决冲突后，再提交，合并完成。

解决冲突就是把Git合并失败的文件手动编辑为我们希望的内容，再提交。

用`git log --graph`命令可以看到分支合并图，然后在英文状态下按Q就可以退出
## 3. 分支管理策略
合并分支时，加上`--no-ff`参数就可以用普通模式合并，合并后的历史有分支，能看出来曾经做过合并，而fast forward合并就看不出来曾经做过合并。
<font color=#999AAA >通常，合并分支时，如果可能，Git会用Fast forward模式，但这种模式下，删除分支后，会丢掉分支信息。
如果要强制禁用Fast forward模式，Git就会在merge时生成一个新的commit，这样，从分支历史上就可以看出分支信息。
我们切换回master：

```bash
$ git switch master
Switched to branch 'master'
```
准备合并dev分支，请注意--no-ff参数，表示禁用Fast forward，因为本次合并要创建一个新的commit，所以加上-m参数，把commit描述写进去

```bash
$ git merge --no-ff -m "merge with no-ff" dev

Merge made by the 'recursive' strategy.
 readme.txt | 1 +
 1 file changed, 1 insertion(+)
```

## 4. Bug分支

## 5. Feature分支
## 6. 多人协作
## 7. Rebase
# 六、标签管理
## 1. 创建标签
## 2. 操作标签











