import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSizePolicy, QSpacerItem, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QSize, QPropertyAnimation
from PySide6.QtGui import QPixmap, QPainter, QBrush, QLinearGradient, QColor, QImage, QPalette, QPen, QCursor

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

        pen = QPen(QBrush(gradient), 4)  # Ширина обводки здесь 4 пикселя, можно изменить
        painter.setPen(pen)
        painter.drawRoundedRect(self.rect(), 20, 20)  # 20 - радиус скругления углов, можно изменить


class GroupWidget(QWidget):
    def __init__(self, icon_path, gradient_color1, gradient_color2, button_text, description_texts, parent=None):
        super().__init__(parent)
        self.setMinimumSize(200, 250)

        layout = QVBoxLayout(self)

        width_widget = QWidget()
        width_widget.setFixedSize(250, 1)
        layout.addWidget(width_widget)

        #hex_color = gradient_color1

        # Преобразование HEX в RGB
        #rgb_color = tuple(int(hex_color[i:i + 2], 16) for i in (1, 3, 5))

        outer_frame = GradientBorderFrame(gradient_color1, gradient_color2, self)
        outer_frame.setCursor(QCursor(Qt.PointingHandCursor))
        outer_frame.setStyleSheet(
            "QWidget:hover {"
            f"   background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba({gradient_color2.red()}, {gradient_color2.green()}, {gradient_color2.blue()}, 0.4), stop:1 rgba({gradient_color1.red()}, {gradient_color1.green()}, {gradient_color1.blue()}, 0.4));"  # Градиент с прозрачным начальным цветом и прозрачностью в конечном цвете
                                                                                                                                               "   border-radius: 17px;"
                                                                                                                                               "}"

        )
        outer_frame.setWindowOpacity(0.1)
        outer_frame.setFixedWidth(280)

        layout.addWidget(outer_frame, alignment=Qt.AlignCenter)

        layout_outer_frame = QVBoxLayout(outer_frame)
        spacer_item = QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout_outer_frame.addItem(spacer_item)

        icon_widget = QLabel()
        icon_widget.setAlignment(Qt.AlignCenter)
        icon_pixmap = self.load_and_render_svg(icon_path, gradient_color1, gradient_color2)
        icon_pixmap = icon_pixmap.scaled(QSize(150, 150), Qt.KeepAspectRatio)
        icon_widget.setPixmap(icon_pixmap)
        layout_outer_frame.addWidget(icon_widget, alignment=Qt.AlignCenter)

        spacer_item = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout_outer_frame.addItem(spacer_item)

        # Create a horizontal layout for the line and its margins
        line_layout = QHBoxLayout()
        line_layout.addSpacerItem(QSpacerItem(30, 1, QSizePolicy.Fixed, QSizePolicy.Fixed))  # Add left margin
        gradient_line = QFrame()
        gradient_line.setFixedWidth(2)
        gradient_line.setFixedHeight(50)# Set fixed width to 250 pixels
        gradient_line.setFrameShape(QFrame.HLine)
        gradient_line.setStyleSheet(
            "border: 0px; background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {}, stop:1 {}); border-radius: 1px;".format(
                gradient_color1.name(), gradient_color2.name()))
        line_layout.addWidget(gradient_line, alignment=Qt.AlignCenter)
        line_layout.addSpacerItem(QSpacerItem(30, 1, QSizePolicy.Fixed, QSizePolicy.Fixed))  # Add right margin
        layout_outer_frame.addLayout(line_layout)  # Add the line layout to the outer frame layout

        spacer_item = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout_outer_frame.addItem(spacer_item)

        new_label = QLabel("Новый лэйбл")
        new_label.setAlignment(Qt.AlignCenter)
        layout_outer_frame.addWidget(new_label, alignment=Qt.AlignCenter)

        spacer_item = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout_outer_frame.addItem(spacer_item)

        for text, color in description_texts:
            label = QLabel(text)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: {}; border: 0px; background: transparent;".format(color))
            layout_outer_frame.addWidget(label, alignment=Qt.AlignCenter)

        icon_widget.setStyleSheet("""
                    QLabel {
                        border: 0px;
                        background: transparent;
                    }
                """)



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
