import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QPainter, QLinearGradient, QColor, QBrush, QImage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Группы кнопок")
        self.setMinimumSize(1000, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.setStyleSheet("""
                    QMainWindow {
                        background-color: #404040; /* черно-серый цвет фона */
                    }
                    QPushButton {
                        background-color: #808080; /* серый цвет кнопок */
                        color: white; /* белый цвет текста на кнопках */
                        border-radius: 5px; /* скругление углов кнопок */
                        padding: 10px; /* отступ вокруг текста кнопок */
                        border: none; /* убираем границу кнопок */
                        box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.5); /* тень от кнопок */
                    }
                    QPushButton:hover {
                        background-color: #606060; /* изменение цвета при наведении на кнопку */
                    }
                    QLabel {
                        color: white; /* устанавливаем белый цвет текста на иконках */
                    }
                """)

        main_layout = QHBoxLayout(central_widget)

        # Группа 1
        group1_layout = QVBoxLayout()
        group1_layout.setSpacing(30)
        group1_layout.setContentsMargins(0, 0, 0, 0)  # Устанавливаем отступы в 0
        icon1_widget = QLabel()
        icon1_widget.setAlignment(Qt.AlignCenter)
        icon1_pixmap = self.load_and_render_svg("icons/pc.svg", QColor("#8a2be2"))
        icon1_pixmap = icon1_pixmap.scaled(QSize(150, 150), Qt.KeepAspectRatio)  # Устанавливаем фиксированный размер
        icon1_widget.setPixmap(icon1_pixmap)
        button1_1 = QPushButton("Кнопка 1")
        button1_1.setFixedSize(150, 50)
        button1_1.clicked.connect(self.print_window_size)
        group1_layout.addWidget(icon1_widget, alignment=Qt.AlignBottom)
        group1_layout.addWidget(button1_1, alignment=Qt.AlignTop)
        main_layout.addLayout(group1_layout)

        # Группа 2
        group2_layout = QVBoxLayout()
        group2_layout.setSpacing(30)
        icon2_widget = QLabel()
        icon2_widget.setAlignment(Qt.AlignCenter)
        icon2_pixmap = self.load_and_render_svg("icons/network.svg", QColor("#8a2be2"))
        icon2_pixmap = icon2_pixmap.scaled(QSize(150, 150), Qt.KeepAspectRatio)  # Устанавливаем фиксированный размер
        icon2_widget.setPixmap(icon2_pixmap)
        button2_1 = QPushButton("Кнопка 2")
        button2_1.setFixedSize(150, 50)
        group2_layout.addWidget(icon2_widget, alignment=Qt.AlignBottom)
        group2_layout.addWidget(button2_1, alignment=Qt.AlignTop)
        main_layout.addLayout(group2_layout)

        # Группа 3
        group3_layout = QVBoxLayout()
        group3_layout.setSpacing(30)
        group3_layout.setContentsMargins(0, 0, 0, 0)  # Устанавливаем отступы в 0
        icon3_widget = QLabel()
        icon3_widget.setAlignment(Qt.AlignCenter)
        icon3_pixmap = self.load_and_render_svg("icons/internet.svg", QColor("#8a2be2"))
        icon3_pixmap = icon3_pixmap.scaled(QSize(150, 150), Qt.KeepAspectRatio)  # Устанавливаем фиксированный размер
        icon3_widget.setPixmap(icon3_pixmap)
        button3_1 = QPushButton("Кнопка 3")
        button3_1.setFixedSize(150, 50)
        group3_layout.addWidget(icon3_widget, alignment=Qt.AlignBottom)
        group3_layout.addWidget(button3_1, alignment=Qt.AlignTop)
        main_layout.addLayout(group3_layout)

    def load_and_render_svg(self, filename, gradient_color):
        image = QImage(filename)
        if image.isNull():
            print("Ошибка загрузки файла")
            return QPixmap()

        pixmap = QPixmap(image.size())
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.drawImage(0, 0, image)

        gradient = QLinearGradient(0, 0, pixmap.width(), pixmap.height())
        gradient.setColorAt(0, QColor(gradient_color))
        gradient.setColorAt(1, QColor(Qt.transparent))
        brush = QBrush(gradient)
        painter.setBrush(brush)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.drawRect(pixmap.rect())
        painter.end()

        return pixmap

    def print_window_size(self):
        window_size = self.size()
        print(f"Текущие размеры окна: {window_size.width()}x{window_size.height()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())