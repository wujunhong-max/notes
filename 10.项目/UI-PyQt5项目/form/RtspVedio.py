import cv2
import time
from PyQt5.QtGui import QImage, QPixmap


class RtspVedio:
    """视频流对象"""

    def __init__(self, url, out_label):
        """初始化方法"""
        self.url = url
        self.outLabel = out_label

    def display(self):
        """显示"""
        cap = cv2.VideoCapture(self.url)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        """帧数显示 
        fps = cap.get(cv2.CAP_PROP_FPS)
        size = (cap.get(cv2.CAP_PROP_FRAME_WIDTH),
                cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 

        print("fps: {}\nsize: {}".format(fps, size))
        """
        start_time = time.time()
        i = 0
        while cap.isOpened():
            success, frame = cap.read()
            """             
            if i < 3:
                cv2.imshow("capture", frame)
                i += 1 
                """
            if success:
                if (time.time() - start_time) > 0.1:
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    img = QImage(
                        frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)

                    self.outLabel.setPixmap(QPixmap.fromImage(img))

                    cv2.waitKey(1)
                    start_time = time.time()

