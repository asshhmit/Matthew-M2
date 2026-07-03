import sys
import subprocess
from datetime import datetime
import numpy as np
import sounddevice as sd
import cv2  # Required for webcam feed
import requests
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QColor, QPalette, QPainter, QPolygon, QImage, QPixmap, QPen, QFont, QPainterPath
from PyQt6.QtCore import Qt, QTimer, QPoint, QRect
from pathlib import Path



StartupSound = Path(__file__).parent / "startup_sound.py"
subprocess.Popen([sys.executable, str(StartupSound)])
SpeechAi = Path(__file__).parent / "speech_ai.py"
subprocess.Popen([sys.executable, str(SpeechAi)])

# ================= APP ====================
app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Matthew AI")
window.resize(1400, 800)

palette = QPalette()
palette.setColor(QPalette.ColorRole.Window, QColor(10, 10, 10))
window.setPalette(palette)


# ================= TIME BOX ====================
time_box = QLabel(window)
time_box.setGeometry(1160, 30, 250, 80)
time_box.setStyleSheet("""
    background-color: rgba(0,255,255,20);
    border: 1px solid rgba(0,255,255,120);
    border-radius: 20px;
""")


# ================= CLOCK ====================
clock = QLabel(window)
clock.setGeometry(1180, 40, 150, 60)
clock.setStyleSheet("""
    font-size:40px;
    color:cyan;
    font-family:Arial;
    font-weight:bold;
    background:transparent;
""")


# ================= AM PM ====================
label = QLabel(window)
label.setGeometry(1290, 38, 120, 70)
label.setStyleSheet("""
    color: cyan;
    font-size: 50px;
    font-family: Arial;
    font-weight: bold;
    background: transparent;
""")


def update_clock():
    now = datetime.now()
    clock.setText(now.strftime("%I:%M"))
    label.setText(now.strftime("%p"))


timer = QTimer()
timer.timeout.connect(update_clock)
timer.start(1000)
update_clock()


# ================= DIAL ====================
from rotating_dial import RotatingDial
dial = RotatingDial()
dial.setFixedSize(1500, 700)
window.setCentralWidget(dial)


# ================= GROQ GRAPH ====================
class GroqGraph(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(700, 250)
        self.max_limit = 60000

        try:
            import os
            if os.path.exists("groq_usage.txt"):
                try:
                    with open("groq_usage.txt", "r") as f:
                        self.used = int(f.read().strip())
                except:
                    self.used = 0
            else:
                self.used = 0
        except:
            self.used = 0

        self.history = [
            0,
            self.used * 0.10,
            self.used * 0.25,
            self.used * 0.45,
            self.used * 0.70,
            self.used
        ]

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Background
        painter.setPen(QColor(0, 255, 255, 40))
        painter.setBrush(QColor(5, 10, 20, 220))
        painter.drawRoundedRect(self.rect(), 15, 15)

        # Title
        painter.setPen(QColor("white"))
        font = painter.font()
        font.setPointSize(13)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(20, 35, "llama-3.1-8b-instant")

        # Graph Labels
        painter.setPen(QColor(220, 220, 220))
        font.setPointSize(10)
        font.setBold(False)
        painter.setFont(font)
        painter.drawText(300, 35, "Total Tokens")

        # Rate limit line
        painter.setPen(QPen(QColor(255, 0, 0), 1, Qt.PenStyle.DashLine))
        painter.drawLine(50, 65, self.width() - 30, 65)

        painter.setPen(QColor("red"))
        painter.drawText(self.width() - 90, 80, "Rate Limit")

        # Axis
        painter.setPen(QColor(150,150,150))
        painter.drawLine(50, 210, 50, 65)
        painter.drawLine(50, 210, self.width() - 30, 210)

        # Scale Labels
        painter.drawText(10, 70, "60K")
        painter.drawText(10, 140, "30K")
        painter.drawText(20, 210, "0")

        # Cyan Graph
        pen = QPen(QColor(0,255,255))
        pen.setWidth(2)
        painter.setPen(pen)

        graph_width = self.width() - 90
        graph_height = 145
        points = []

        for i, value in enumerate(self.history):
            x = 50 + (graph_width/(len(self.history)-1))*i
            y = 210 - ((value/self.max_limit) * graph_height)
            points.append((x,y))

        for i in range(len(points)-1):
            painter.drawLine(int(points[i][0]), int(points[i][1]), int(points[i+1][0]), int(points[i+1][1]))

        painter.setBrush(QColor(0,255,255))
        for x,y in points:
            painter.drawEllipse(int(x)-3, int(y)-3, 6, 6)

        # Bottom Stats
        painter.setPen(QColor("cyan"))
        painter.drawText(100, 240, f"Tokens : {self.used:,}")
        painter.drawText(350, 240, f"Limit : {self.max_limit:,}")


# ================= JARVIS BUTTON ====================
class JarvisButton(QPushButton):
    def __init__(self, text, command, parent=None):
        super().__init__(text, parent)
        self.command = command
        self.setFixedSize(180, 45)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton{
                background: transparent;
                border:none;
                color:white;
                font-size:14px;
                font-family:Arial;
                font-weight:bold;
                text-align:left;
                padding-left:35px;
                }
        """)
        self.clicked.connect(self.open_app)

    def open_app(self):
        try:
            subprocess.Popen(self.command)
        except Exception as e:
            print("Error:", e)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        points = [
            QPoint(0, 0),
            QPoint(150, 0),
            QPoint(180, 22),
            QPoint(150, 45),
            QPoint(0, 45),
            QPoint(20, 22)
        ]

        painter.setPen(QColor(0, 255, 255))
        painter.setBrush(QColor(60, 60, 60, 230))
        painter.drawPolygon(QPolygon(points))
        super().paintEvent(event)


# ================= SIDEBAR BUTTONS ====================
buttons = [
    ("This PC", "explorer.exe"),
    ("Task Mngr", "taskmgr.exe"),
    ("CMD", "cmd.exe"),
    ("Paint", "mspaint.exe"),
    ("Notepad", "notepad.exe"),
    ("Calculator", "calc.exe"),
]

y = 120
for text, command in buttons:
    btn = JarvisButton(text, command, window)
    btn.move(20, y)
    y += 55


# ==================== BATTERY INDICATOR ====================
class BatteryBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.level = 10
        self.setFixedSize(60, 300)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        box_width = 35
        box_height = 20
        spacing = 5
        x = 12

        for i in range(10):
            y = self.height() - ((i + 1) * (box_height + spacing))
            if i < self.level:
                painter.setBrush(QColor(0, 170, 255))
            else:
                painter.setBrush(QColor(40, 40, 40))

            painter.setPen(QColor(0, 255, 255))
            painter.drawRoundedRect(x, y, box_width, box_height, 3, 3)

battery = BatteryBar(window)
battery.move(20, 450)
battery.show()
battery.level = 7
battery.update()


# =============================== MID CIRCLE =============================================
class CircleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 200)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QColor("cyan"))
        painter.setBrush(QColor(0, 255, 255, 40))
        painter.drawEllipse(20, 20, 160, 160)

circle = CircleWidget()
circle.setParent(window)
circle.move(650, 250)
circle.show()


# ============================== MID CIRCLE 2 ============================================
class CircleWidget2(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 200)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QColor("cyan"))
        painter.setBrush(QColor(0, 255, 255, 40))
        painter.drawEllipse(20, 20, 160, 160)

circle2 = CircleWidget2()
circle2.setParent(window)
circle2.move(300, 150)
circle2.show()


# ================================== MIDDLE TEXT ============================================================
jarvis_text = QLabel(window)
jarvis_text.setText("MATTHEW")
jarvis_text.setStyleSheet("""
    color: cyan;
    font-size: 27px;
    font-family: Arial;
    font-weight: bold;
    background: transparent;
""")
jarvis_text.resize(155, 70)
jarvis_text.move(680, 317)


# ============================================ WAVE PATTERN =============================================================
class AudioWaveWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(400, 120)
        self.bars = np.zeros(50)

        self.stream = sd.InputStream(
            channels=1,
            callback=self.audio_callback,
            blocksize=1024
        )
        self.stream.start()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(30)

    def audio_callback(self, indata, frames, time, status):
        audio = np.abs(indata[:, 0])
        chunks = np.array_split(audio, len(self.bars))

        for i, chunk in enumerate(chunks):
            self.bars[i] = np.mean(chunk) * 1500

        self.bars = np.clip(self.bars, 5, 100)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        bar_width = 6
        spacing = 2
        x = 0

        for h in self.bars:
            height = int(h)
            y = self.height() - height

            painter.setBrush(QColor(0, 255, 255))
            painter.setPen(QColor(0, 255, 255))

            dot_size = 4
            for yy in range(y, self.height(), 6):
                painter.drawEllipse(x, yy, dot_size, dot_size)

            x += bar_width + spacing

wave = AudioWaveWidget(window)
wave.move(1050, 650)
wave.show()


# ==================================== CAMERA WIDGET ====================================
class CameraWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(320, 220)
        
        self.video_frame = QLabel(self)
        self.video_frame.setGeometry(12, 40, 296, 155)
        self.video_frame.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW if sys.platform == "win32" else cv2.CAP_ANY)
        self.camera_connected = self.capture.isOpened()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        if self.camera_connected:
            ret, frame = self.capture.read()
            if ret:
                frame = cv2.flip(frame, 1)
                frame = cv2.resize(frame, (296, 155))
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
                
                self.video_frame.setPixmap(QPixmap.fromImage(qt_image))
                self.video_frame.setStyleSheet("border-radius: 10px; background-color: transparent;")
                return
            else:
                self.camera_connected = False
        
        self.video_frame.clear()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setPen(QColor(0, 140, 200, 100))
        painter.setBrush(QColor(8, 18, 28, 240))
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 14, 14)

        painter.setPen(QColor(0, 180, 255))
        font = painter.font()
        font.setFamily("Segoe UI")
        font.setBold(True)
        font.setPointSize(10)
        painter.setFont(font)
        painter.drawText(40, 26, "Camera")

        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(16, 15, 16, 11, 2, 2)
        painter.drawEllipse(21, 17, 6, 6)

        painter.drawRoundedRect(268, 15, 14, 10, 1, 1)
        painter.drawEllipse(288, 14, 11, 11)

        if not self.camera_connected:
            painter.setPen(QColor(0, 255, 255, 30))
            painter.setBrush(QColor(5, 12, 20, 150))
            painter.drawRoundedRect(12, 40, 296, 155, 10, 10)

            painter.setPen(QColor(0, 130, 200, 180))
            painter.setBrush(QColor(0, 130, 200, 140))
            painter.drawRoundedRect(138, 90, 32, 22, 4, 4)
            
            points = [QPoint(170, 96), QPoint(182, 90), QPoint(182, 112), QPoint(170, 106)]
            painter.drawPolygon(QPolygon(points))

            painter.setPen(QColor(0, 150, 220))
            font.setPointSize(11)
            font.setBold(False)
            painter.setFont(font)
            painter.drawText(QRect(12, 122, 296, 25), Qt.AlignmentFlag.AlignCenter, "Camera Off")

            painter.setPen(QColor(0, 130, 200, 150))
            font.setPointSize(8)
            painter.setFont(font)
            painter.drawText(QRect(12, 198, 296, 20), Qt.AlignmentFlag.AlignCenter, "Camera is inactive. Click the power button to start.")

    def closeEvent(self, event):
        if self.capture.isOpened():
            self.capture.release()
        super().closeEvent(event)

camera_panel = CameraWidget(window)
camera_panel.move(1150, 400)
camera_panel.show()


# ================================ WEATHER DATA & WIDGET =============================================
def weather_stats():
    location = "Sector 30, Faridabad, Haryana, India"
    url = f"https://wttr.in/{location}?format=j1"
    try:
        response = requests.get(url)
        data = response.json()
        current = data["current_condition"][0]

        temperature = current["temp_C"]
        feels_like = current["FeelsLikeC"]
        humidity = current["humidity"]
        weather = current["weatherDesc"][0]["value"]
        wind_speed = current["windspeedKmph"]
        
        return temperature, feels_like, humidity, weather, wind_speed
    except Exception as e:
        print("Error fetching weather:", e)
        return "N/A", "N/A", "N/A", "Unknown", "N/A"

# Custom Vector Cloud Component
class NeonCloudIcon(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(90, 70)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        cyan_color = QColor("#00e5ff")
        pen = QPen(cyan_color, 3)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        path = QPainterPath()
        path.moveTo(25, 50)
        path.lineTo(65, 50)
        path.arcTo(55, 35, 20, 20, 270, 180)
        path.arcTo(30, 15, 35, 35, 0, 180)
        path.arcTo(13, 33, 22, 22, 90, 140)
        path.closeSubpath()

        glow_pen = QPen(QColor(0, 229, 255, 50), 7)
        painter.setPen(glow_pen)
        painter.drawPath(path)
        
        painter.setPen(pen)
        painter.drawPath(path)

# Unified UI Card Frame Box Component
class JarvisWeatherWidget(QWidget):
    def __init__(self, parent=None, temp="18", humidity="88", wind="22", condition="Cloudy", feel="18"):
        super().__init__(parent)
        
        self.setStyleSheet("background-color: #040c12; border-radius: 12px;")
        self.setFixedSize(420, 145)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(15)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        text_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # Vector Icon Placement
        self.icon_widget = NeonCloudIcon()
        main_layout.addWidget(self.icon_widget, alignment=Qt.AlignmentFlag.AlignVCenter)

        # Dynamic Content Fonts
        header_font = QFont("Segoe UI", 11, QFont.Weight.Bold)
        stats_font = QFont("Segoe UI", 10)
        small_font = QFont("Segoe UI", 8)

        # Data Field Integration
        self.lbl_title = QLabel(f"CURRENT WEATHER: {condition.upper()}")
        self.lbl_title.setFont(header_font)
        self.lbl_title.setStyleSheet("color: #00e5ff; background: transparent;")
        text_layout.addWidget(self.lbl_title)

        self.lbl_temp = QLabel(f"TEMP: {temp}°C")
        self.lbl_temp.setFont(stats_font)
        self.lbl_temp.setStyleSheet("color: #a0c0d0; background: transparent;")
        text_layout.addWidget(self.lbl_temp)

        self.lbl_humidity = QLabel(f"HUMIDITY: {humidity}%")
        self.lbl_humidity.setFont(stats_font)
        self.lbl_humidity.setStyleSheet("color: #a0c0d0; background: transparent;")
        text_layout.addWidget(self.lbl_humidity)

        self.lbl_wind = QLabel(f"WIND: {wind} km/h WNW")
        self.lbl_wind.setFont(stats_font)
        self.lbl_wind.setStyleSheet("color: #a0c0d0; background: transparent;")
        text_layout.addWidget(self.lbl_wind)

        # Micro-summary detail tracking layer
        self.lbl_details = QLabel(f"METRIC TRACK: FEELS LIKE {feel}°C // REGION ID: SEC-30")
        self.lbl_details.setFont(small_font)
        self.lbl_details.setStyleSheet("color: #5c7c8c; background: transparent; padding-top: 2px;")
        text_layout.addWidget(self.lbl_details)

        main_layout.addLayout(text_layout)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        border_pen = QPen(QColor(0, 229, 255, 80), 1)
        painter.setPen(border_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(1, 1, self.width() - 2, self.height() - 2, 12, 12)


# Pull API stats & Instantiate Weather Module Box
temp, feel, humidity, wthr, windSpeed = weather_stats()

weather_panel = JarvisWeatherWidget(window, temp, humidity, windSpeed, wthr, feel)
weather_panel.move(1050, 200)  # Precision Layout Allocation Coordinates
weather_panel.show()


# ==================== REMAINING UI ELEMENTS ====================
temp_txt = QLabel(window)
temp_txt.setText(f"{temp}*C")
temp_txt.setStyleSheet("""
    color: cyan;
    font-size: 50px;
    font-family: Arial;
    font-weight: bold;
""")
temp_txt.adjustSize()
temp_txt.move(347, 225)

usage_graph = GroqGraph(window)
usage_graph.move(170, 530)
usage_graph.show()

# ================= SHOW WINDOW ====================
window.show()
sys.exit(app.exec())