from PyQt5.QtCore import pyqtSlot, QIODevice, QByteArray
from PyQt5.QtSerialPort import QSerialPortInfo, QSerialPort
from PyQt5.QtWidgets import QWidget, QMessageBox
from Ui_serialport2 import *
from socket import *
from UI_Dockwidget import *


# 创建TCP套接字
# tcp tcp_socket = socket(AF_INET, SOCK_STREAM)
# 2.准备连接服务器，建立连接
# tcp serve_ip = '10.33.230.228'  # 获取本地主机名
# tcp serve_port = int(5000)  # 端口要是int类型，所有要转换


# 串口调试助手，发送按钮是发送tcp数据
class serialport(QLabel, Ui_Form):

    def __init__(self):
        super(serialport, self).__init__()

        self.setAutoFillBackground(True)  # 标签1的背景填充更改为True，否则无法显示背景

        self.setAlignment(Qt.AlignCenter)
        # 设置label的背景颜色(这里随机)
        # 这里加了一个margin边距(方便区分QStackedWidget和QLabel的颜色)
        #self.setStyleSheet('background: rgb(%d, %d, %d);margin: 50px;' % (
            #randint(0, 255), randint(0, 255), randint(0, 255)))
        #self.setText("我是页面")  # setText():设置Qlabel的文本内容
        self.setupUi(self)

        self._serial = QSerialPort(self)  # 用于连接串口的对象
        self._serial.readyRead.connect(self.onReadyRead)  # 绑定数据读取信号，绑定点击信号
        # 首先获取可用的串口列表
        self.getAvailablePorts()

        # tcp_socket.connect((serve_ip, serve_port))  # 连接服务器，建立连接,参数是元组形式

        # 信号与槽装饰器，@pyqtSlot()装饰器把函数on_buttonConnect_clicked包装为一个槽函数
    @pyqtSlot()
    def on_buttonConnect_clicked(self):  # 创建一个on_buttonConnect_clicked方法，on_发送者对象名称_发射信号名称
        # 打开或关闭串口按钮
        if self._serial.isOpen():
            # 如果串口是打开状态则关闭
            self._serial.close()
            self.textBrowser.append('串口已关闭')
            self.buttonConnect.setText('打开串口')  # 按钮的名字
            self.labelStatus.setProperty('isOn', False)
            self.labelStatus.style().polish(self.labelStatus)  # 刷新样式
            return

        # 根据配置连接串口
        name = self.comboBoxPort.currentText()
        if not name:
            QMessageBox.critical(self, '错误', '没有选择串口')
            return
        port = self._ports[name]
        #         self._serial.setPort(port)
        # 根据名字设置串口（也可以用上面的函数）
        self._serial.setPortName(port.systemLocation())
        # 设置波特率
        self._serial.setBaudRate(  # 动态获取,类似QSerialPort::Baud9600这样的吧
            getattr(QSerialPort, 'Baud' + self.comboBoxBaud.currentText()))
        # 设置校验位
        self._serial.setParity(  # QSerialPort::NoParity
            getattr(QSerialPort, self.comboBoxParity.currentText() + 'Parity'))
        # 设置数据位
        self._serial.setDataBits(  # QSerialPort::Data8
            getattr(QSerialPort, 'Data' + self.comboBoxData.currentText()))
        # 设置停止位
        self._serial.setStopBits(  # QSerialPort::Data8
            getattr(QSerialPort, self.comboBoxStop.currentText()))

        # NoFlowControl          没有流程控制
        # HardwareControl        硬件流程控制(RTS/CTS)
        # SoftwareControl        软件流程控制(XON/XOFF)
        # UnknownFlowControl     未知控制
        self._serial.setFlowControl(QSerialPort.NoFlowControl)
        # 读写方式打开串口
        ok = self._serial.open(QIODevice.ReadWrite)
        if ok:
            self.textBrowser.append('打开串口成功')
            self.buttonConnect.setText('关闭串口')
            self.labelStatus.setProperty('isOn', True)
            self.labelStatus.style().polish(self.labelStatus)  # 刷新样式
        else:
            self.textBrowser.append('打开串口失败')
            self.buttonConnect.setText('打开串口')
            self.labelStatus.setProperty('isOn', False)
            self.labelStatus.style().polish(self.labelStatus)  # 刷新样式

    @pyqtSlot()
    def on_buttonSend_clicked(self):
        # text1 = self.plainTextEdit.toPlainText()
        # if not text1:
            # return
        # if self.checkBoxHexSend.isChecked():
            # 如果勾选了hex发送
           #  text1 = text1.toHex()
        # 发送数据
        # tcp send_data = text1
        # tcp tcp_socket.send(send_data.encode("gbk"))  # 用的是send方法，不是sendto

        # 下面注释掉的部分是用来通过串口发送数据的
        # 发送消息按钮
        # text = self.plainTextEdit.toPlainText()
        if not self._serial.isOpen():
            print('串口未连接')
            return
        text = self.plainTextEdit.toPlainText()
        if not text:
            return
        text = QByteArray(text.encode('gb2312'))  # emmm windows 测试的工具貌似是这个编码
        if self.checkBoxHexSend.isChecked():
             # 如果勾选了hex发送
            text = text.toHex()
        # 发送数据
        print('发送数据:', text)
        self._serial.write(text)

    def onReadyRead(self):
        # 数据接收响应
        if self._serial.bytesAvailable():
            # 当数据可读取时
            # 这里只是简答测试少量数据,如果数据量太多了此处readAll其实并没有读完
            # 需要自行设置粘包协议
            data = self._serial.readAll()
            if self.checkBoxHexView.isChecked():
                # 如果勾选了hex显示
                data = data.toHex()
            data = data.data()
            # 解码显示（中文啥的）
            try:
                self.textBrowser.append('我收到了: ' + data.decode('gb2312'))
            except:
                # 解码失败
                self.textBrowser.append('我收到了: ' + repr(data))

    def getAvailablePorts(self):
        # 获取可用的串口
        self._ports = {}  # 用于保存串口的信息
        infos = QSerialPortInfo.availablePorts()
        infos.reverse()  # 逆序
        for info in infos:
            # 通过串口名字-->关联串口变量
            self._ports[info.portName()] = info
            self.comboBoxPort.addItem(info.portName())

    def closeEvent(self, event):
        if self._serial.isOpen():
            self._serial.close()
        super(serialport, self).closeEvent(event)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    # 创建一个主窗口
    window = QMainWindow()
    window.resize(1200, 600)  # 设置窗口尺寸，长宽
    window.move(300, 300)  # 移动窗口(显示时在哪),长高

    label = serialport()
    window.setCentralWidget(label)  # 设置窗口中心部件

    # 显示窗口
    window.show()
    # 进入程序主循环，并通过exit函数确保主循环安全结束
    sys.exit(app.exec_())