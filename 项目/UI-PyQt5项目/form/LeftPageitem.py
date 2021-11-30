from PyQt5.QtGui import *
from UI_Dockwidget import *


# 在主页面的左侧的页面项
class LeftPageitem(QListWidgetItem):

    def __init__(self, pic_filename):  # pic是图片的文件名
        self.pic_filename = pic_filename

        super(LeftPageitem, self).__init__()
        self.run(self)

    def run(self, pic_filename):
        self.setIcon(QIcon(self.pic_filename))  # 插入左侧按钮图片