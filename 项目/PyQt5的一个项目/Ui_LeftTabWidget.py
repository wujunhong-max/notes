#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import randint

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class LeftTabWidget(QWidget):

    def __init__(self):
        super(LeftTabWidget, self).__init__()
        self.resize(800, 500)
        #左右布局(左边一个QListWidget + 右边QStackedWidget)
        #layout = QHBoxLayout(self, spacing=0)
        layout = QHBoxLayout(spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        # 左侧列表
        self.listWidget = QListWidget(self)
        layout.addWidget(self.listWidget)

        # 右侧层叠窗口
        self.stackedWidget = QStackedWidget(self)
        #vlayout.addWidget(self.stackedWidget)
        layout.addWidget(self.stackedWidget)
        #layout.addLayout(self.stackedWidget)
        self.setLayout(layout)
        self.initUi()

    def initUi(self):
        # 初始化界面
        # 通过QListWidget的当前item变化来切换QStackedWidget中的序号
        self.listWidget.currentRowChanged.connect(
            self.stackedWidget.setCurrentIndex)
        # 去掉边框
        self.listWidget.setFrameShape(QListWidget.NoFrame)
        # 隐藏滚动条
        self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listWidget.setViewMode(QListWidget.IconMode)

    """ 增加页面 """
    def addPage(self, item, label, listview=None, m=None):
        
        item.setSizeHint(QSize(50, 40))
        self.listWidget.addItem(item)

        label.setAlignment(Qt.AlignCenter)
        vbl = QHBoxLayout(spacing=0)
        vbl.addWidget(label)
        if listview is not None:
            vbl.addWidget(listview)
        if m is not None:
            vbl.addWidget(m)
        stack = QWidget()
        stack.setLayout(vbl)
        #stack = QWidget()
        #stack.setLayout()
        self.stackedWidget.addWidget(stack)
        
        

# 美化样式表
Stylesheet = '''
/*去掉item虚线边框*/
QListWidget, QListView, QTreeWidget, QTreeView {
    outline: 0px;
}
/*设置左侧选项的最小最大宽度,文字颜色和背景颜色*/
QListWidget {
    min-width: 50px;
    max-width: 50px;
    color: white;
    background: rgb(44, 44, 44);
}
/*被选中时的背景颜色和左边框颜色*/
QListWidget::item:selected {
    background: rgb(44, 44, 44);
    border-left: 2px solid rgb(255, 255, 255);
}
/*鼠标悬停颜色*/
HistoryPanel::item:hover {
    background: rgb(52, 52, 52);
    border-left: 2px solid rgb(255, 255, 255);
}

/*右侧的层叠窗口的背景颜色*/
QStackedWidget {
    background: rgb(255, 255, 255);
}
/*模拟的页面*/
QLabel {
    color: white;
}'''


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyleSheet(Stylesheet)
    w = LeftTabWidget()
    w.show()
    sys.exit(app.exec_())
