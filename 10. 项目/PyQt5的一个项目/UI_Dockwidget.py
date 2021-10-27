from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


# 创建两个dock窗口的类
class Ui_Dockwidget(QDockWidget):

    def __init__(self):
        super(Ui_Dockwidget, self).__init__()  # 调用父类构造函数，必须有

    def setupUi1(self, text):          # 创建右边第一个窗口

        self.text = text
        self.setWindowIconText(self.text)   # text 是窗口标题
        self.setFloating(False)             # 设置浮动
        self.setGeometry(800, 0, 600, 300)  # 设置几何
        # 下面两行是固定大小
        # self.setMinimumSize(QtCore.QSize(400, 125))
        # self.setMaximumSize(QtCore.QSize(400, 125))

    def setupUi2(self, text):           # 创建右边第二个窗口

        self.text = text
        self.setWindowIconText(self.text)   # 设置窗口标题
        self.setFloating(False)             # 设置浮动
        self.setGeometry(800, 300, 600, 300)  # 设置几何
        # 下面两行是固定大小
        # elf.setMinimumSize(QtCore.QSize(800, 250))
        # self.setMaximumSize(QtCore.QSize(800, 250))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    # 创建一个主窗口
    window = QMainWindow()
    window.resize(400, 400)  # 设置窗口尺寸，长宽
    window.move(300, 300)  # 移动窗口(显示时在哪),长高

    # 创建两个dock窗口对象
    dock1 = Ui_Dockwidget()
    dock2 = Ui_Dockwidget()
    dock1.setupUi1('第一个窗口')
    dock2.setupUi2('第二个窗口')

    # 将其加到主窗口中
    window.addDockWidget(Qt.RightDockWidgetArea, dock1)  # 添加界面
    window.addDockWidget(Qt.RightDockWidgetArea, dock2)  # 添加界面

    # 显示窗口
    window.show()
    # 进入程序主循环，并通过exit函数确保主循环安全结束
    sys.exit(app.exec_())