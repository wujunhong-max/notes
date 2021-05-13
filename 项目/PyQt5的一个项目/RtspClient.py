import os  # os--操作系统接口模块
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
# 调用本地的一个类
from form.MyThread import *


class RtspClient():
    def __init__(self):  # 创建一个__init__方法,新类构造函数
        super(RtspClient, self).__init__()  # 调用父类构造函数
        # self.setupUi(self)              # 图形界面初始化
        # self.init_vedio(label)       # Label 控件用以显示文字和图片. Label 通常被用来展示信息, 而非与用户交互

    """ 初始化视频流 """

    def init_vedio(self, label):
        print("进程pid:", os.getpid())  # 操作系统里每打开一个程序都会创建一个进程ID，即PID。

        self.mythread = MyThread(
            'rtmp://58.200.131.2:1935/livetv/gdtv', label)
        # 'rtsp://192.168.137.25/live.sdp', label)    # thread--进程
        self.mythread.start()  # 启动线程


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    # 创建一个主窗口
    window = QMainWindow()
    window.resize(1200, 600)  # 设置窗口尺寸，长宽
    window.move(300, 300)  # 移动窗口(显示时在哪),长高

    # 设置页面
    label = QLabel(window)
    label.setAutoFillBackground(True)
    label.setText("")
    label.setMinimumSize(QtCore.QSize(800, 400))
    label.setMaximumSize(QtCore.QSize(800, 400))
    label.setScaledContents(True)
    label.setObjectName("RtspInput")

    # 创建一个对象
    rtc = RtspClient()
    rtc.init_vedio(label)

    # 显示窗口
    window.show()
    # 进入程序主循环，并通过exit函数确保主循环安全结束
    sys.exit(app.exec_())