from PyQt5.QtWidgets import *


# 设置第一个页面的标签控件
class QLabel1(QLabel):

    def __init__(self):
        super(QLabel1, self).__init__()

        self.setAutoFillBackground(True)  # 标签1的背景填充更改为True，否则无法显示背景
        self.setText("")  # setText():设置Qlabel的文本内容
        # 下面两行是固定大小
        # label.setMinimumSize(QtCore.QSize(800, 350))
        # label.setMaximumSize(QtCore.QSize(800, 350))
        self.setGeometry(0, 0, 600, 300)  # 从屏幕上（0，0）位置开始（即为最左上角的点），显示一个600*300的界面（宽600，高300）
        self.setScaledContents(True)
        self.setObjectName("RtspInput")