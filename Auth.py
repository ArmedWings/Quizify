from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QApplication, QHBoxLayout, QSizePolicy
from PySide6.QtGui import QPainter, QLinearGradient, QBrush, QPen
from PySide6.QtCore import QSize, Qt

class Auth(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window  # Сохраняем ссылку на MainWindow
        self.setup_ui()


    def setup_ui(self):
        # Создаем вертикальный макет для размещения фрейма и лейбла
        self.on_other_page = True
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Устанавливаем отступы макета
        layout.setAlignment(Qt.AlignCenter)  # Выравниваем содержимое по центру

        # Создаем лейбл


        # Создаем фрейм
        self.frame = GradientBorderFrame(Qt.red, Qt.blue, self)
        self.frame.setMinimumSize(500, 250)
        self.frame.setMaximumWidth(900)  # Ограничиваем ширину фрейма до 600 пикселей

        # Создаем вертикальный макет для фрейма и лейбла
        frame_layout = QVBoxLayout()
        frame_layout.addWidget(self.frame)

        # Добавляем макет с лейблом и фреймом в основной макет
        layout.addLayout(frame_layout)

        # Заполняем фрейм
        self.fill_frame()
        self.resizeEvent = self.on_resize

    def on_resize(self, event):
        self.adjust_label_position()
    def adjust_label_position(self):
        # Перемещаем метку по центру по вертикали
        self.common_label.adjustSize()
        x = (self.width() - self.common_label.width()) // 2
        y = (self.height() - self.common_label.height()) // 20
        self.common_label.move(x, y)

    def fill_frame(self):
        # Здесь вы можете добавить необходимые элементы во фрейм
        # Например, кнопки или другие виджеты
        self.common_label = QLabel("Fen[", self)
        self.common_label.setStyleSheet("font-size: 24px; color: white;")
        self.adjust_label_position()

        # Создаем вертикальный макет для размещения элементов внутри фрейма
        frame_layout = QVBoxLayout(self.frame)
        frame_layout.setContentsMargins(20, 20, 20, 20)
        frame_layout.setAlignment(Qt.AlignCenter)  # Выравниваем содержимое по центру

        # Создаем кнопку
        button = QPushButton("Нажми меня", self.frame)
        button.setStyleSheet("font-size: 18px;")
        frame_layout.addWidget(button)

        # Добавляем обработчик события нажатия кнопки
        button.clicked.connect(self.handle_button_click)

    def handle_button_click(self):
        # Пример обработчика события нажатия кнопки
        print("Кнопка была нажата")

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
        painter.drawRoundedRect(self.rect(), 20, 20)