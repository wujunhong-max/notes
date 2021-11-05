import sys
from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon


class QuitApplication(QMainWindow):
    def __init__(self):
        super(QuitApplication, self).__init__()
        # 设置窗口的尺寸
        self.resize(300, 120)
        # 设置标题
        self.setWindowTitle('退出应用程序')

        # 添加Button
        self.button1 = QPushButton('退出应用程序')
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
    main = QuitApplication()
    main.show()
    sys.exit(app.exec_())