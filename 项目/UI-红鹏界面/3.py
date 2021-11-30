# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connect_me.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
#导入程序运行必须模块
import sys
#PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog,QWidget, QHBoxLayout, QLabel,QTableWidgetItem,QGridLayout
from PyQt5.QtGui import QPixmap, QImage
#导入designer工具生成的login模块
from jiemian5 import *
#from predict import *

class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.select_image.clicked.connect(self.openimage)
        self.setting.clicked.connect(self.settingshow)
        self.logoshow()
        self.textBrowser.setPlainText("序号            经度            维度            类别")
        items = {'轨条': 6, '三角': 5, '目标1':9, '目标2':6}
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        num = 0

        for key in items:
                item = QTableWidgetItem(str(key))
                self.tableWidget.setItem(0,num,item)
                num += 1
                item = QTableWidgetItem(str(items[key]))
                self.tableWidget.setItem(0,num,item)
                num += 1


    def openimage(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")

        jpg = QtGui.QPixmap(imgName).scaled(self.show_image.width(), self.show_image.height())
        self.show_image.setPixmap(jpg)
        self.show_image.setScaledContents(True)

    def settingshow(self):
        fileAddress = "F:/yolov4/img/0727.tfw"             # 文件路径
        file = open(fileAddress, 'r')                       # fileAddress为txt文件的路径
        fileContent = file.read()                      # 读取文件内容
        file.close()                                        # 关闭文件
        self.setting_show.setPlainText(fileContent)





    def logoshow(self):
        #设置布局
        #myLayout =QGridLayout()
        #设置布局没有边缘空白
        #myLayout.setContentsMargins(0,0,0,0)
        #self.setLayout(myLayout)

        #设置图片
        self.logo_1.setPixmap(QPixmap("GDUT_logo.png"))
        self.logo_1.setScaledContents(True)

        self.logo_2.setPixmap(QPixmap("HoPong_logo.png"))
        self.logo_2.setScaledContents(True)

        self.show()

        #pix = QPixmap('logo.jpg')
        #logo = QtWidgets.QLabel(self)
        #logo.setGeometry(0,250,500,210)
        #logo.setPixmap(pix)
        #logo.setScaledContents(True)   #自适应QLabel大小







if __name__ == "__main__":
    #固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    #初始化
    myWin = MyMainForm()
    # 设置窗口的标题
    myWin.setWindowTitle('无人机地面目标AI识别系统')
    #将窗口控件显示在屏幕上
    myWin.show()

    #程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())


#C:\Users\Jeff\Desktop\AIdemo\test>pyuic5 -o login.py login.ui