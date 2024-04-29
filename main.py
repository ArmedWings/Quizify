import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSizePolicy, QSpacerItem
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QPainter, QBrush, QLinearGradient, QColor, QImage, QPalette

class GroupWidget(QWidget):
    # Код GroupWidget остается без изменений

    def __init__(self, icon_path, gradient_color1, gradient_color2, button_text, description_texts, parent=None):
        super().__init__(parent)
        self.setMinimumSize(200, 250)

        layout = QVBoxLayout(self)
        outer_frame = QFrame(self)
        outer_frame.setStyleSheet("""
            QFrame {
                border: 2px solid #555555;
                border-radius: 20px;
            }
        """)

        layout.addWidget(outer_frame, alignment=Qt.AlignCenter)

        layout_outer_frame = QVBoxLayout(outer_frame)
        spacer_item = QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Expanding) #НАД ИКОНКОЙ
        layout_outer_frame.addItem(spacer_item)

        icon_widget = QLabel()
        icon_widget.setAlignment(Qt.AlignCenter)
        icon_pixmap = self.load_and_render_svg(icon_path, gradient_color1, gradient_color2)
        icon_pixmap = icon_pixmap.scaled(QSize(150, 150), Qt.KeepAspectRatio)
        icon_widget.setPixmap(icon_pixmap)
        layout_outer_frame.addWidget(icon_widget, alignment=Qt.AlignCenter)

        # Добавление отступа
        spacer_item = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding) #ПОД ИКОНКОЙ
        layout_outer_frame.addItem(spacer_item)

        button = QPushButton(button_text)
        button.setFixedSize(230, 50)
        layout_outer_frame.addWidget(button, alignment=Qt.AlignCenter)

        spacer_item = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding) #ПОД КНОПКОЙ
        layout_outer_frame.addItem(spacer_item)

        for text, color in description_texts:
            description_label = QLabel(text)
            description_label.setAlignment(Qt.AlignCenter)
            description_label.setStyleSheet("color: {}; border: 0px;".format(color))
            layout_outer_frame.addWidget(description_label, alignment=Qt.AlignCenter)

        icon_widget.setStyleSheet("""
                    QLabel {
                        border: 0px;
                    }
                """)

        button.setStyleSheet("""
                    QPushButton {
                        background-color: #191919;
                        color: white;
                        border-radius: 5px;
                        padding: 10px;
                        border: 1px solid #7E7E7E;
                    }
                """)

        # Добавление отступа
        spacer_item = QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Expanding) #ПОД ТЕКСТОМ
        layout_outer_frame.addItem(spacer_item)




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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Группы кнопок")
        self.setMinimumSize(1000, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.setStyleSheet("""
                    QMainWindow {
                        background-color: #1C1B1B; /* черно-серый цвет фона */
                    }
                    QPushButton {
                        background-color: #191919; /* серый цвет кнопок */
                        color: white; /* белый цвет текста на кнопках */
                        border-radius: 5px; /* скругление углов кнопок */
                        padding: 10px; /* отступ вокруг текста кнопок */
                        border: 1px solid #7E7E7E;
                    }
                    QPushButton:hover {
                        background-color: #111111; /* изменение цвета при наведении на кнопку */
                    }
                    QLabel {
                        color: white; /* устанавливаем белый цвет текста на иконках */
                    }
                """)

        main_layout = QHBoxLayout(central_widget)

        # Группа 1
        group1_widget = GroupWidget("icons/pc.svg", QColor("#D660F2"), QColor("#5A42D6"), "Кнопка 1",
                                    [
                                        ("- Использование без интернета", "#46F557"),
                                        ("- Простая настройка", "#46F557"),
                                        ("- Низкая безопасность базы данных", "#C9180A"),
                                        ("- Доступ только на локальном компьютере", "#C9180A")
                                    ])
        main_layout.addWidget(group1_widget)

        # Группа 2
        group2_widget = GroupWidget("icons/network.svg", QColor("#6942D6"), QColor("#29B2D5"), "Кнопка 2",
                                    [
                                        ("- Доступ с любого компьютера", "#46F557"),
                                        ("- Высокая безопасность БД", "#BADB34"),
                                        ("- Требуется интернет", "#BADB34"),
                                        ("- Требуется открытая MySQL БД", "#C9180A")
                                    ])
        main_layout.addWidget(group2_widget)

        # Группа 3
        group3_widget = GroupWidget("icons/internet.svg", QColor("#2667C9"), QColor("#46C1F8"), "Кнопка 3",
                                    [
                                        ("- Простая настройка", "#46F557"),
                                        ("- Доступ с любого компьютера", "#46F557"),
                                        ("- Крайне высокая безопасность БД", "#46F557"),
                                        ("- Требуется доступ в интернет", "#BADB34")
                                    ])
        main_layout.addWidget(group3_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
