from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPainter, QColor, QPen
import math


class RotatingDial(QWidget):
    def __init__(self):
        super().__init__()

        self.angle = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate)
        self.timer.start(20)

    def rotate(self):
        self.angle += 2
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.translate(self.width() / 2,
                           self.height() / 2)

        painter.rotate(self.angle)

        pen = QPen(QColor(0, 255, 255))
        pen.setWidth(4)
        painter.setPen(pen)

        radius = 120

        for i in range(40):
            a = i * 9
            x1 = radius * math.cos(math.radians(a))
            y1 = radius * math.sin(math.radians(a))

            x2 = (radius + 20) * math.cos(math.radians(a))
            y2 = (radius + 20) * math.sin(math.radians(a))

            painter.drawLine(
                int(x1), int(y1),
                int(x2), int(y2)
            )