from PyQt5 import QtCore
from form.RtspVedio import *


class MyThread(QtCore.QThread):  # 线程类 QtCore.QThread

    def __init__(self, url, out_label, parent=None):
        super(MyThread, self).__init__(parent)
        self.gui_text = None
        self.url = url
        self.outLabel = out_label

    def do_work(self):
        RtspVedio(self.url, self.outLabel).display()  # 视频播放函数

    def run(self):
        self.do_work()