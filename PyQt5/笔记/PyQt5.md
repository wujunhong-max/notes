## Qt designer设置信号与槽

在Qt designer中

想让**方格框默认勾选**，在方格的属性**checked**那里勾选

在属性**enabled**那里取消勾选，就不可用了

设置信号与槽

关闭窗口：clicked--close()

显示/隐藏： toggled(bool)-setVisible(bool)

可用/不可用: toggled(bool)-setEnable(bool)



<img src="C:\Users\20902\Desktop\image\image1.png" alt="image1" style="zoom:80%;" />



##   Qt designer设置伙伴关系

伙伴关系，设置后能按热键，

在姓名后加(&a),在年龄后加(&b),在职业后加(&c)

按alt+a就转到第一行的输入

按alt+b就转到第二行的输入

按alt+c就转到第三行的输入





![image2](C:\Users\吴俊宏\Desktop\image\image2.png)

## 为控件添加提示信息

用到的代码如下：

```python
QToolTip.setFont(QFont('宋体', 12))       	# 设置字体，12是字体号
self.setToolTip('今天是<b>星期五</b>')       	 # 设置窗体的提示信息,其中‘星期五’被加粗了

 # 添加Button并且添加提示信息
self.button1 = QPushButton('退出应用程序')
self.button1.setToolTip('这是一个按钮，Are you ok?')

```

示意图如下：

<img src="C:\Users\吴俊宏\Desktop\image\gif1.gif" alt="gif1" style="zoom:80%;" />

完整代码：

```python
# 当鼠标移动到控件上时，显示控件的提示信息
import sys
from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QApplication, QWidget, QPushButton, QToolButton, QToolTip
from PyQt5.QtGui import QIcon, QFont


class TooltipForm(QMainWindow):
    def __init__(self):
        super(TooltipForm, self).__init__()
        self.initUI()

    def initUI(self):
        # 设置字体，12是字体号
        QToolTip.setFont(QFont('宋体', 12))   
        # 设置窗体的提示信息,其中‘星期五’被加粗了
        self.setToolTip('今天是<b>星期五</b>')      
        

        # 设置窗口的尺寸
        self.resize(500, 500)
        # 设置标题
        self.setWindowTitle('设置控件提示信息')

        # 添加Button
        self.button1 = QPushButton('退出应用程序')
        self.button1.setToolTip('这是一个按钮，Are you ok?')
        # 将信号与槽关联
       	self.button1.clicked.connect(self.onClick_Button)

        layout = QHBoxLayout()
        layout.addWidget(self.button1)

        mainFrame = QWidget()
        mainFrame.setLayout(layout)
        
	   # 设置窗体中心的控件
        self.setCentralWidget(mainFrame)    

    # 按钮单击事件的方法（自定义的槽)
    def onClick_Button(self):
        sender = self.sender()
        print(sender.text() + '按钮被按下')
        app = QApplication.instance()   # 返回应用程序对象
        # 退出应用程序
        app.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setWindowIcon(QIcon('./image/5198/0.ico'))
    main = TooltipForm()
    main.show()
    sys.exit(app.exec_())
```

## QLabel控件的基本用法

### QLabel通常用到的一些函数

setAlignment():设置文本的对齐方式

居中对齐：setAlignment(Qt.AlignCenter)

右对齐：setAlignment(Qt.AlignRight)

setIndent():设置文本缩进

.text():获取文本内容

.setBuddy():设置伙伴关系

setText():设置文本内容

selectedText(): 返回所选择的字符

setWordWrap():设置是否允许换行

### Qlabel常用的信号（事件）

1.当鼠标滑过QLabel控件时触发：linkHovered

2.当鼠标单击QLabel控件时触发：linkActivated

### 两种信号与槽绑定所用的格式

```python
# 滑过的信号
控件名称.linkHovered.connect(self.槽函数名称)
#单击的信号
控件名称.linkActivated.connect(self.槽函数名称)
```

示意图如下：



完整的代码如下：![gif2](C:\Users\吴俊宏\Desktop\image\gif2.gif)

```python
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtGui import QPalette, QPixmap
from PyQt5.QtCore import Qt


class QLabelDemo(QWidget):
    def __init__(self):
        super(QLabelDemo, self).__init__()
        self.initUI()

    def initUI(self):
        # 设置4个控件
        label1 = QLabel(self)
        label2 = QLabel(self)
        label3 = QLabel(self)
        label4 = QLabel(self)

        # 设置文本显示内容和字体颜色
        label1.setText("<font color = yellow>这是一个文本标签")
        # 设置图片背景
        label1.setAutoFillBackground(True)
        # 建立画布，颜色为蓝色
        palette = QPalette()
        palette.setColor(QPalette.Window, Qt.blue)
        # 将画布添加到label中
        label1.setPalette(palette)
        # 文本居中
        label1.setAlignment(Qt.AlignCenter)

        # 第二个标签
        label2.setText("<a href='#'>欢迎使用Python GUI程序</a>")
        # 鼠标滑过
        label2.linkHovered.connect(self.linkHovered)

        # 第三个标签
        # 添加提示信息
        label3.setToolTip('这是一个图片标签')
        # 居中
        label3.setAlignment(Qt.AlignCenter)
        # 图片导入
        label3.setPixmap(QPixmap("./image/5198/cv3.jpg"))

        # 第四个标签，网站链接
        # 注意，触发事件和打开浏览器是互斥的！！！
        # 设置打开扩展链接，如果设置True,打开浏览器，如果为False，就调用槽函数
        label4.setOpenExternalLinks(True)
        label4.setText("<a href='https://www.baidu.com/'>点击这里可以打开链接（百度）")
        # 居右
        label4.setAlignment(Qt.AlignRight)
        # tip
        label4.setToolTip("这是一个超级链接")
        # 鼠标点击（和上面的打开网页是互斥的）
        label4.linkActivated.connect(self.linkClicked)

        # 垂直布局
        vbox = QVBoxLayout()
        vbox.addWidget(label1)
        vbox.addWidget(label2)
        vbox.addWidget(label3)
        vbox.addWidget(label4)

        # 设置布局
        self.setLayout(vbox)
        # 标题
        self.setWindowTitle("QLabel控件演示")

    # 两个槽函数
    def linkHovered(self):
        print("当鼠标滑过label2")

    def linkClicked(self):
        print("当鼠标单击label4")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = QLabelDemo()
    # 显示窗口
    main.show()
    # 建立循环
    sys.exit(app.exec_())
```

## QLabel与伙伴控件

```python
# 设置热键
# 创建一个标签和行输入
# 输入alt+n就能转到namelineEdit
nameLabel = QLabel('&name',self)
namelineEdit = QLineEdit(self)
# 设置伙伴控件
nameLabel.setBuddy(nameLineEdit)

# 栅格布局
mainLayout = QGridLayout(self)
mainLayout.addWidget(nameLabel, 0, 0) 	    # 表示将nameLabel添加在第一行第一列
mainLayout.addWidget(nameLineEdit, 0, 1, 1, 2)	# 表示将nameLineEdit添加在第一行第二列，占一行两列 
```

## 使用Pyinstaller打包PyQt5应用

```
pip3 install pyinstaller

pyinstaller -Fw 文件名
# -w: 不让程序显示终端
# -F：将所有的库打包成一个单独的文件
```

## 设置lineEdit里面的默认值

在Qt designer中，LineEdit的属性placeholderText里添加即可

## 限制QLineEdit控件的输入（校验器）

## 布局控件

先定义一些控件

```python
self.pushButton_get_ip = QtWidgets.QPushButton()    # 重新获取IP的按钮
self.pushButton_link = QtWidgets.QPushButton()      # 连接网络的按钮
self.pushButton_unlink = QtWidgets.QPushButton()    # 断开网络的按钮
```

定义布局

```python
self.h_box_1 = QHBoxLayout()
self.h_box_2 = QHBoxLayout()
self.h_box_3 = QHBoxLayout()
self.h_box_4 = QHBoxLayout()
self.h_box_recv = QHBoxLayout()
```

## 设置线程和在线程中利用信号来调用另一个类中的函数

```python
import sys
from PyQt5.QtCore import Qt, QThread,pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,QHBoxLayout


class Demo(QWidget):
    def __init__(self):  
        super(Demo, self).__init__()

        self.button = QPushButton('开始', self)
        self.button.clicked.connect(self.count_func)
        self.button_2 = QPushButton('停止', self)
        self.button_2.clicked.connect(self.stop_count_func)

        self.label = QLabel('0', self)
        self.label.setAlignment(Qt.AlignCenter)

        self.my_thread = MyThread()#实例化线程对象
        self.my_thread.my_signal.connect(self.set_label_func)
        #线程自定义信号连接的槽函数

        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()
        self.h_layout.addWidget(self.button)
        self.h_layout.addWidget(self.button_2)
        self.v_layout.addWidget(self.label)
        self.v_layout.addLayout(self.h_layout)
        self.setLayout(self.v_layout)


    def stop_count_func(self):
        self.my_thread.is_on = False
        self.my_thread.count = 0

    def count_func(self):
        self.my_thread.is_on = True
        self.my_thread.start()#启动线程

    def set_label_func(self, num):
        self.label.setText(num)
        #由于自定义信号时自动传递一个字符串参数，所以在这个槽函数中要接受一个参数


class MyThread(QThread):#线程类
    my_signal = pyqtSignal(str)  #自定义信号对象。参数str就代表这个信号可以传一个字符串
    def __init__(self):
        super(MyThread, self).__init__()
        self.count = 0
        self.is_on = True


    def run(self): #线程执行函数
        while self.is_on :
            print(self.count)
            self.count += 1
            self.my_signal.emit(str(self.count))  #释放自定义的信号
            #通过自定义信号把str(self.count)传递给槽函数

            self.sleep(1)  #本线程睡眠n秒【是QThread函数】


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
```



