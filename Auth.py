from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QApplication, QHBoxLayout, QSizePolicy, QSpacerItem, QLineEdit
from PySide6.QtGui import QPainter, QLinearGradient, QBrush, QPen
from PySide6.QtCore import QSize, Qt
import os

class Auth(QWidget):
    def __init__(self, main_window=None, gradient_color1=None, gradient_color2=None):
        super().__init__()
        self.main_window = main_window  # Сохраняем ссылку на MainWindow
        self.gradient_color1 = gradient_color1
        self.gradient_color2 = gradient_color2
        self.setup_ui()

    def setup_ui(self):
        # Создаем вертикальный макет для размещения фрейма
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Устанавливаем отступы макета
        layout.setAlignment(Qt.AlignCenter)  # Выравниваем содержимое по центру

        # Создаем фрейм
        self.frame = GradientBorderFrame(self.gradient_color1, self.gradient_color2, self)
        self.frame.setMinimumSize(500, 250)
        self.frame.setMaximumWidth(700)  # Ограничиваем ширину фрейма до 900 пикселей

        # Добавляем фрейм в макет
        layout.addWidget(self.frame)

        # Заполняем фрейм в зависимости от условий
        self.fill_frame()

        # Устанавливаем обработчик изменения размера окна
        self.resizeEvent = self.on_resize

    def fill_frame(self):
        # Читаем конфигурационный файл
        with open('config.txt', 'r') as file:
            lines = file.readlines()

        # Проверяем условия
        if lines[0].strip() == 'mode=1' and len(lines) == 1:
            self.fill_frame_firstoffline()

        elif lines[0].strip() == 'mode=1' and 'offline=' in lines[1]:
            db_path = lines[1].strip().split('=')[1]
            if not os.path.exists(db_path) or os.stat(db_path).st_size == 0:
                self.fill_frame_firstoffline()
            else:
                self.fill_frame_welcome()

    def fill_frame_firstoffline(self):
        # Здесь вы можете добавить необходимые элементы во фрейм
        # Например, кнопки или другие виджеты
        self.common_label = QLabel("Добро пожаловать!", self)
        self.common_label.setStyleSheet("font-size: 24px; color: white;")
        self.adjust_label_position()

        # Создаем вертикальный макет для размещения элементов внутри фрейма
        frame_layout = QVBoxLayout(self.frame)
        frame_layout.setContentsMargins(20, 20, 20, 20)
        frame_layout.setAlignment(Qt.AlignCenter)  # Выравниваем содержимое по центру

        # Создаем кнопку
        button_register = QPushButton("Зарегистрировать аккаунт модератора", self.frame)
        button_register.setStyleSheet("font-size: 18px;")
        frame_layout.addWidget(button_register)

        # Отступ
        spacer_label = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)
        frame_layout.addItem(spacer_label)

        # Лэйбл "Или"
        label_or = QLabel("Или", self.frame)
        label_or.setStyleSheet("font-size: 18px; color: white;")
        label_or.setAlignment(Qt.AlignCenter)  # Выравниваем по центру по горизонтали
        frame_layout.addWidget(label_or)

        # Отступ
        spacer_button = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)
        frame_layout.addItem(spacer_button)

        # Кнопка "Импортировать данные пользователей"
        button_import = QPushButton("Импортировать данные пользователей", self.frame)
        button_import.setStyleSheet("font-size: 18px;")
        frame_layout.addWidget(button_import)

        # Ширина кнопки = максимальная доступная по фрейму
        button_register.setFixedWidth(self.frame.width() - 30)
        button_import.setFixedWidth(self.frame.width() - 30)

        # Подключаем обработчик события нажатия на кнопку
        button_register.clicked.connect(self.handle_register_click)

    def handle_register_click(self):
        # Здесь можно выполнить дополнительные действия
        # Например, запустить функцию для заполнения фрейма другим содержимым
        self.fill_frame_moder()

    def clear_frame(self):
        # Получаем текущий макет фрейма
        frame_layout = self.frame.layout()

        # Удаляем все элементы из макета
        while frame_layout.count():
            item = frame_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                spacer = item.spacerItem()
                if spacer:
                    frame_layout.removeItem(spacer)
    def fill_frame_moder(self):
        # Очистить содержимое фрейма
        self.clear_frame()

        # Изменить главный лэйбл
        self.common_label.setText("Аккаунт модератора")
        self.adjust_label_position()

        # Получаем текущий макет фрейма
        frame_layout = self.frame.layout()

        # Создаем лэйблы и текстовые поля вручную
        label1 = QLabel("Придумайте логин:", self.frame)
        line_edit1 = QLineEdit(self.frame)
        label2 = QLabel("Придумайте пароль:", self.frame)
        line_edit2 = QLineEdit(self.frame)
        label3 = QLabel("Повтор пароля:", self.frame)
        line_edit3 = QLineEdit(self.frame)
        label4 = QLabel("Выберите папку для сохранения:", self.frame)
        line_edit4 = QLineEdit(self.frame)

        # Увеличиваем высоту полей ввода
        line_edit1.setFixedHeight(30)
        line_edit2.setFixedHeight(30)
        line_edit3.setFixedHeight(30)
        line_edit4.setFixedHeight(30)

        # Увеличиваем размер порядковых лэйблов
        label1.setStyleSheet("font-size: 14px;")
        label2.setStyleSheet("font-size: 14px;")
        label3.setStyleSheet("font-size: 14px;")
        label4.setStyleSheet("font-size: 14px;")

        # Добавляем элементы в существующий макет
        frame_layout.addWidget(label1)
        frame_layout.addWidget(line_edit1)
        frame_layout.addWidget(label2)
        frame_layout.addWidget(line_edit2)
        frame_layout.addWidget(label3)
        frame_layout.addWidget(line_edit3)
        frame_layout.addWidget(label4)
        frame_layout.addWidget(line_edit4)

        # Создаем лэйбл по середине и кнопку "Подтвердить"
        label_center = QLabel("Ограничьте прямой доступ к папке!", self.frame)
        label_center.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(label_center)

        button_confirm = QPushButton("Подтвердить", self.frame)
        button_confirm.setStyleSheet("font-size: 18px;")
        frame_layout.addWidget(button_confirm)

        # Помещаем кнопку по центру
        frame_layout.setAlignment(button_confirm, Qt.AlignCenter)

        # Ширина кнопки = максимальная доступная по фрейму
        button_confirm.setFixedWidth(self.frame.width() - 30)
    def fill_frame_welcome(self):
        pass

    def handle_button_click(self):
        # Пример обработчика события нажатия кнопки
        print("Кнопка была нажата")

    def fill_frame_reg(self):
        # Заполнение фрейма для регистрации
        pass  # здесь добавляем лейблы и кнопки

    def fill_frame_log(self):
        # Заполнение фрейма для входа
        pass  # здесь добавляем лейблы и кнопки

    def fill_frame_moderator(self):
        # Заполнение фрейма для аккаунта модератора
        pass  # здесь добавляем лейблы и кнопки

    def on_resize(self, event):
        self.adjust_label_position()
    def adjust_label_position(self):
        # Перемещаем метку по центру по вертикали
        self.common_label.adjustSize()
        x = (self.width() - self.common_label.width()) // 2
        y = (self.height() - self.common_label.height()) // 20
        self.common_label.move(x, y)


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