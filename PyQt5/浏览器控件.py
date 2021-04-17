import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


# QWebEngineView控件使用load（）函数加载一个Web页面，实际上就是使用HTTP Get方法加载web页面，
# 这个控件可以加载本地的web页面，也可以加载外部的WEb页面
class MainWindow(QMainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()
    self.setWindowTitle('加载外部网页的例子')
    self.setGeometry(5, 30, 1355, 730)
    self.browser = QWebEngineView()     # 浏览器控件所用的类
    # 加载外部的web界面
    # load（QUrl url) 加载指定的URL(网址)并显示
    # setHtml(QString&html) 将网页视图的内容设置为指定的HTML内容
    self.browser.load(QUrl('https://www.jb51.net'))
    self.setCentralWidget(self.browser)     # 设置在窗口正中


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exit(app.exec_())