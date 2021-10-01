from RtspClient import *
from serialport import *
from UI_Dockwidget import *
from Ui_LeftTabWidget import *
from form.LeftPageitem import *
from form.QLabel1 import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,  QHBoxLayout, QVBoxLayout


class main(QMainWindow):
    def __init__(self):
        super(main, self).__init__()
        self.addcontrols()

        self.setCentralWidget(self.w)  # 设置窗口中心的控件
        self.setGeometry(0, 0, 1200, 600)  # 设置主窗口大小
        self.layout = QHBoxLayout()  # 在水平的方向上排列控件 左右排列

    def addcontrols(self):
        self.w = LeftTabWidget()  # w是UI窗口类LeftTabWidget的一个对象

    # 设置页面按钮
        self.item = LeftPageitem('cv1.jpg')
        self.item2 = LeftPageitem('cv2.jpg')
        self.item3 = LeftPageitem('cv3.jpg')
    # 设置页面控件
        self.label = QLabel1()
        self.label2 = serialport()

    # 创建两个dock窗口对象
        self.dock1 = Ui_Dockwidget()
        self.dock2 = Ui_Dockwidget()
        self.dock1.setupUi1('第一个窗口')
        self.dock2.setupUi2('第二个窗口')
    # 垂直布局
        self.qvb = QVBoxLayout(spacing=0)
        self.qvb.addWidget(self.dock1)
        self.qvb.addWidget(self.dock2)
    # 将垂直布局加入窗口
        self.nm = QWidget()
        self.nm.setLayout(self.qvb)

    # 改变背景颜色
    # self.nm.setStyleSheet("background-color:gray;")
        self.w.addPage(self.item, self.label, self.nm)
        self.w.addPage(self.item2, self.label2)

        self.rtc = RtspClient()
        self.rtc.init_vedio(self.label)


if __name__ == '__main__':
    import sys
    import cgitb  # CGI处理模块,CGI:通用网关接口, 该模块提供了用于 Python 脚本的特殊异常处理程序，如果发生了未捕获的异常，将会展示格式化的输出报告
    cgitb.enable(1, None, 5, '')  # 可以控制是将报告显示在浏览器中，还是将报告记录到文件以供随后进行分析
    from PyQt5.QtWidgets import QApplication  # 该类管理图形用户界面应用程序的控制流和主要设置

    app = QApplication(sys.argv)  # 初始化窗口系统并且使用在argv中的argc个命令行参数构造一个应用程序对象，就是实例化一个应用对象
    #                                        sys.argv是一组命令行参数的列表
    app.setStyleSheet(Stylesheet)  # 窗口的外观
    m = main()
    m.show()
    sys.exit(app.exec_())


