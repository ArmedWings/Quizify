import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QColor  # Добавляем QColor для работы с цветами

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
        group1_layout.setSpacing(50)
        icon1_widget = QLabel()
        icon1_widget.setAlignment(Qt.AlignCenter)
        icon1_pixmap = QPixmap("icons/pc.svg").scaled(150, 150)  # Изменяем размер иконки на 150x150 пикселей
        icon1_pixmap = self.change_pixmap_color(icon1_pixmap, QColor("#8a2be2"))  # Изменяем цвет заливки иконки на темно-фиолетовый
        icon1_widget.setPixmap(icon1_pixmap)  # Устанавливаем изображение на QLabel
        button1_1 = QPushButton("Кнопка 1")
        button1_1.setFixedSize(250, 50)
        button1_1.clicked.connect(self.print_window_size)
        group1_layout.addWidget(icon1_widget)
        group1_layout.addWidget(button1_1)
        group1_layout.setAlignment(Qt.AlignCenter)  # Выравниваем содержимое по центру
        main_layout.addLayout(group1_layout)
        main_layout.addSpacing(30)

        # Группа 2
        group2_layout = QVBoxLayout()
        group2_layout.setSpacing(50)
        icon2_widget = QLabel()
        icon2_widget.setAlignment(Qt.AlignCenter)
        icon2_pixmap = QPixmap("icons/network.svg").scaled(150, 150)  # Изменяем размер иконки на 150x150 пикселей
        icon2_pixmap = self.change_pixmap_color(icon2_pixmap, QColor("#8a2be2"))  # Изменяем цвет заливки иконки на темно-фиолетовый
        icon2_widget.setPixmap(icon2_pixmap)  # Устанавливаем изображение на QLabel
        button2_1 = QPushButton("Кнопка 2")
        button2_1.setFixedSize(250, 50)
        group2_layout.addWidget(icon2_widget)
        group2_layout.addWidget(button2_1)
        group2_layout.setAlignment(Qt.AlignCenter)  # Выравниваем содержимое по центру
        main_layout.addLayout(group2_layout)
        main_layout.addSpacing(30)

        # Группа 3
        group3_layout = QVBoxLayout()
        group3_layout.setSpacing(50)
        icon3_widget = QLabel()
        icon3_widget.setAlignment(Qt.AlignCenter)
        icon3_pixmap = QPixmap("icons/internet.svg").scaled(150, 150)  # Изменяем размер иконки на 150x150 пикселей
        icon3_pixmap = self.change_pixmap_color(icon3_pixmap, QColor("#8a2be2"))  # Изменяем цвет заливки иконки на темно-фиолетовый
        icon3_widget.setPixmap(icon3_pixmap)  # Устанавливаем изображение на QLabel
        button3_1 = QPushButton("Кнопка 3")
        button3_1.setFixedSize(250, 50)
        group3_layout.addWidget(icon3_widget)
        group3_layout.addWidget(button3_1)
        group3_layout.setAlignment(Qt.AlignCenter)  # Выравниваем содержимое по центру
        main_layout.addLayout(group3_layout)

    def change_pixmap_color(self, pixmap, color):
        painter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        painter.end()
        return pixmap

    def print_window_size(self):
        window_size = self.size()  # Получаем размеры окна
        print(f"Текущие размеры окна: {window_size.width()}x{window_size.height()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())