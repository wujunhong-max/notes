import sys
from 设置伙伴关系 import *
from PyQt5.QtWidgets import QApplication, QMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = Ui_MainWindow()
    # 向主窗口中添加控件
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())


