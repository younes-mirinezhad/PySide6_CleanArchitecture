# This Python file uses the following encoding: utf-8
from PySide6.QtQuick import QQuickPaintedItem
from PySide6.QtGui import QPainter, QImage
from PySide6.QtCore import QPoint, QMetaObject, Qt
from Libs.Common import Common
import cv2
import numpy as np

class ViewPort(QQuickPaintedItem):
    def __init__(self):
        print(Common.func_info())
        super().__init__()
        self.image = np.zeros((10,10,3), dtype=np.uint8)
    
    def setNewFrame(self, image):
        self.image = image
        QMetaObject.invokeMethod(self, "update", Qt.QueuedConnection)
    def paint(self, painter: QPainter):
        if min(self.image.shape[0], self.image.shape[1]) <= 0:
            return

        out_w = self.size().toSize().width()
        out_h = self.size().toSize().height()
        img = self.image_resize(self.image, out_w, out_h)

        height, width, channel = img.shape
        bytesPerLine = channel * width
        qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()

        x = (out_w - width) / 2.0
        y = (out_h - height) / 2.0
        startPoint = QPoint(x, y)

        painter.drawImage(startPoint, qImg)
    def image_resize(self, image, out_w, out_h):
        h, w = image.shape[:2]
        w_ratio = float(out_w) / w
        h_ratio = float(out_h) / h
        ratio = min(w_ratio, h_ratio)
        dim = (int(w*ratio), int(h*ratio))

        resized = cv2.resize(image, dim, cv2.INTER_AREA)

        return resized
