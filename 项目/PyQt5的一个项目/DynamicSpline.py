from PyQt5.QtChart import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


#  DynamicSpline--动态样条，折线图
class DynamicSpline(QChart):

    def __init__(self):
        super().__init__()  # 可以直接使用 super().xxx 代替 super(Class, self).xxx
        self.m_step = 0
        self.m_x = 5
        self.m_y = 1

        # 初始化图像
        self.series = QSplineSeries(self)  # QSplineSeries()是折线类，根据自己需求选用，下载数据曲线
        green_pen = QPen(Qt.red)  # 折线的颜色
        green_pen.setWidth(3)  # 折线的粗细
        self.series.setPen(green_pen)
        self.axisX = QValueAxis()  # 声明并初始化X轴，Y轴
        self.axisY = QValueAxis()
        self.series.append(self.m_x, self.m_y)  # append--附加

        self.addSeries(self.series)  # 添加曲线
        self.addAxis(self.axisX, Qt.AlignBottom)  # 添加坐标轴X，Y
        self.addAxis(self.axisY, Qt.AlignLeft)
        self.series.attachAxis(self.axisX)  # 把曲线关联到坐标轴
        self.series.attachAxis(self.axisY)
        self.axisX.setTickCount(5)  # 设置X坐标轴上的格点
        self.axisX.setRange(0, 10)  # 设置X，Y范围
        self.axisY.setRange(-5, 10)

        self.timer = QTimer(self)  # 初始化一个定时器
        self.timer.setInterval(1000)  # setInterval--设置时间间隔
        self.timer.timeout.connect(self.handleTimeout)  # 将定时器超时信号与槽函数handleTimeout()连接 handleTimeout--处理超时
        self.timer.start()

    def handleTimeout(self):
        x = self.plotArea().width() / self.axisX.tickCount()
        y = (self.axisX.max() - self.axisX.min()) / self.axisX.tickCount()
        self.m_x += y
        # 在PyQt5.11.3及以上版本中，QRandomGenerator.global()被重命名为global_()
        self.m_y = QRandomGenerator.global_().bounded(5) - 2.5
        self.series.append(self.m_x, self.m_y)
        self.scroll(x, 0)
        if self.m_x >= 100:
            self.timer.stop()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    # 创建一个主窗口
    window = QMainWindow()
    window.resize(1200, 600)  # 设置窗口尺寸，长宽
    window.move(300, 300)  # 移动窗口(显示时在哪),长高

    # 创建一个对象
    chart = DynamicSpline()
    # chart.setTitle("Dynamic spline chart")
    chart.legend().hide()
    chart.setAnimationOptions(QChart.AllAnimations)

    view = QChartView(chart)
    view.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
    # view.setGeometry(0,0,600,400)
    view.setMinimumSize(QtCore.QSize(800, 350))
    view.setMaximumSize(QtCore.QSize(800, 350))

    window.setCentralWidget(view)  # 设置窗口中心部件

    # 显示窗口
    window.show()
    # 进入程序主循环，并通过exit函数确保主循环安全结束
    sys.exit(app.exec_())