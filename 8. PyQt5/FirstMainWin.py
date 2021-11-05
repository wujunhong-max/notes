import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon  # 添加图标


# 写一个主窗口
class main(QMainWindow):
    def __init__(self):
        super(main, self).__init__()
        # 设置主窗口的标题
        self.setWindowTitle('第一个主窗口应用')
        # 设置主窗口的尺寸(用这个可以让窗口居中）
        self.resize(400, 300)
        # 设置窗口图标（与下面的效果一样）
        # self.setWindowIcon(QIcon('./image/5198/0.ico'))
        self.status = self.statusBar()  # 添加状态栏
        self.status.showMessage('只存在5秒的消息', 5000)  # 5000毫秒


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 设置图标
    app.setWindowIcon(QIcon('./image/5198/0.ico'))
    main1 = main()

    main1.show()
    sys.exit(app.exec_())
