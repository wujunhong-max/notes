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