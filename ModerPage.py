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

        self.plus_icon = QLabel(self)
        plus_icon_path = "icons/plus.svg"  # Путь к файлу SVG
        plus_icon_pixmap = self.load_and_render_svg(plus_icon_path, self.gradient_color1, self.gradient_color2)
        plus_icon_pixmap = plus_icon_pixmap.scaled(QSize(80, 80), Qt.KeepAspectRatio)
        self.plus_icon.setPixmap(plus_icon_pixmap)
        self.plus_icon.mousePressEvent = self.plus_icon_clicked

        # Создаем вертикальный макет для второго фрейма и добавляем отступ
        layout_frame2 = QVBoxLayout()
        layout_frame2.addSpacing(100)
        layout_frame2.addWidget(frame2)

        # Добавляем фреймы в главный макет
        main_layout.addWidget(frame1)
        main_layout.addLayout(layout_frame2)

        # Растягиваем фреймы по горизонтали
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 1)

        self.logout_icon = QLabel(self)
        logout_icon_path = "icons/logout.svg"  # Путь к файлу SVG
        logout_icon_pixmap = self.load_and_render_svg(logout_icon_path, self.gradient_color1, self.gradient_color2)
        logout_icon_pixmap = logout_icon_pixmap.scaled(QSize(50, 50), Qt.KeepAspectRatio)
        self.logout_icon.setPixmap(logout_icon_pixmap)
        self.logout_icon.mousePressEvent = self.logout_icon_clicked

        logout_size = logout_icon_pixmap.size()
        plus_size = plus_icon_pixmap.size()
        self.logout_icon.setFixedSize(logout_size)
        self.plus_icon.setFixedSize(plus_size)

        self.adjust_label_position()
        self.resizeEvent = self.on_resize

    def logout_icon_clicked(self, event):
        reply = QMessageBox.question(None, 'Выход',
                                     'Вы уверены, что хотите выйти из аккаунта?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            while self.main_window.main_layout.count():
                item = self.main_window.main_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            from Auth import Auth
            auth_page = Auth(main_window=self.main_window, gradient_color1="#6942D6", gradient_color2="#29B2D5")
            self.main_window.main_layout.removeWidget(self)
            self.main_window.main_layout.addWidget(auth_page)

    def plus_icon_clicked(self, event):
        reply = QMessageBox.question(None, 'Новый тест',
                                     'Создать новый тест?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            while self.main_window.main_layout.count():
                item = self.main_window.main_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            from TestEditor import TestEditor
            testeditor_page = TestEditor(main_window=self.main_window)
            self.main_window.main_layout.removeWidget(self)
            self.main_window.main_layout.addWidget(testeditor_page)

    def load_and_render_svg(self, filename, gradient_color1, gradient_color2):
        image = QImage(filename)
        if image.isNull():
            print("Ошибка загрузки файла")
            return QPixmap()

        pixmap = QPixmap(image.size())
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.drawImage(0, 0, image)

        gradient = QLinearGradient(0, 0, pixmap.width(), pixmap.height())
        gradient.setColorAt(0, gradient_color1)
        gradient.setColorAt(1, gradient_color2)
        brush = QBrush(gradient)
        painter.setBrush(brush)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.drawRect(pixmap.rect())
        painter.end()

        return pixmap
    def on_resize(self, event):
        self.adjust_label_position()
    def adjust_label_position(self):
        x = (self.width() - self.width()//4 - self.plus_icon.width()//2)
        x_right = (self.width() - self.logout_icon.width())
        self.logout_icon.move(x_right, 50 - self.logout_icon.height()//2)
        self.plus_icon.move(x, 50 - self.plus_icon.height()//2)


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