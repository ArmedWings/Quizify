from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QApplication, QHBoxLayout, QSizePolicy, QSpacerItem, QLineEdit, QFileDialog, QMessageBox
from PySide6.QtGui import QPainter, QLinearGradient, QBrush, QPen, QImage, QPixmap
from PySide6.QtCore import QSize, Qt
import os
import sqlite3
class ModerPage(QWidget):
    def __init__(self, main_window=None, gradient_color1=None, gradient_color2=None):
        super().__init__()
        self.main_window = main_window
        self.gradient_color1 = gradient_color1
        self.gradient_color2 = gradient_color2
        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Создаем два фрейма
        frame1 = GradientBorderFrame(self.gradient_color1, self.gradient_color2)
        frame2 = GradientBorderFrame(self.gradient_color1, self.gradient_color2)

        # Добавляем фреймы в главный макет
        main_layout.addWidget(frame1)
        main_layout.addWidget(frame2)

        # Растягиваем фреймы по горизонтали
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 1)

class GradientBorderFrame(QFrame):
    def __init__(self, gradient_color1, gradient_color2, parent=None):
        super().__init__(parent)
        self.gradient_color1 = gradient_color1
        self.gradient_color2 = gradient_color2

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient(self.rect().topLeft(), self.rect().topRight())
        gradient.setColorAt(0, self.gradient_color1)
        gradient.setColorAt(1, self.gradient_color2)

        pen = QPen(QBrush(gradient), 4)
        painter.setPen(pen)
        painter.drawRoundedRect(self.rect(), 20, 20)