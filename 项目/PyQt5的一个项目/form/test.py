import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class SplitterExample(QWidget):
    def __init__(self):
        super(SplitterExample, self).__init__()
        self.initUI()

    def initUI(self):
        # 水平布局
        hbox = QHBoxLayout(self)

        self.setWindowTitle("QSplitter 例子")
        self.setGeometry(300, 300, 300, 200)
        # QFrame是基本控件的基类，QWidget是QFrame的基类
        topleft = QFrame()
        topleft.setFrameShape(QFrame.StyledPanel)
        bottom = QFrame()
        bottom.setFrameShape(QFrame.StyledPanel)
        splitter1 = QSplitter(Qt.Horizontal)
        textedit = QTextEdit()
        splitter1.addWidget(topleft)
        splitter1.addWidget(textedit)
        splitter1.setSizes([100,200])
        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)
        # 为水平布局添加控件
        hbox.addWidget(splitter2)
        # 将窗口本身设置为水平布局，总布局为水平布局
        self.setLayout(hbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = SplitterExample()
    demo.show()
    sys.exit(app.exec_())
