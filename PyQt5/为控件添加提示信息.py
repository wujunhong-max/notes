# 当鼠标移动到控件上时，显示控件的提示信息
import sys
from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QApplication, QWidget, QPushButton, QToolButton, QToolTip
from PyQt5.QtGui import QIcon, QFont


class TooltipForm(QMainWindow):
    def __init__(self):
        super(TooltipForm, self).__init__()
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('宋体', 12))       # 设置字体，12是字体号
        self.setToolTip('今天是<b>星期五</b>')       # 设置窗体的提示信息,其中‘星期五’被加粗了

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

        self.setCentralWidget(mainFrame)    # 设置窗体中心的控件

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