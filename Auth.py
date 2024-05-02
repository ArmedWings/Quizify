from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QApplication, QHBoxLayout, QSizePolicy, QSpacerItem, QLineEdit, QFileDialog, QMessageBox
from PySide6.QtGui import QPainter, QLinearGradient, QBrush, QPen
from PySide6.QtCore import QSize, Qt
import os
import sqlite3

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
        self.frame.setMinimumSize(500, 100)
        self.frame.setMaximumWidth(700)  # Ограничиваем ширину фрейма до 900 пикселей

        # Добавляем фрейм в макет
        layout.addWidget(self.frame)

        frame_layout = QVBoxLayout(self.frame)
        frame_layout.setContentsMargins(40, 40, 40, 40)
        frame_layout.setAlignment(Qt.AlignCenter)  # Выравниваем содержимое по центру

        # Заполняем фрейм в зависимости от условий
        self.fill_frame()

        # Устанавливаем обработчик изменения размера окна
        self.resizeEvent = self.on_resize

    def fill_frame(self):
        # Читаем конфигурационный файл
        with open("config.txt", "r") as f:
            lines = f.readlines()
            if len(lines) >= 2:
                second_line = lines[1].strip()  # Вторая строка файла
                if second_line.startswith("catalog="):
                    path = second_line.split("=")[1]
                    if os.path.exists(path) and os.path.isfile(os.path.join(path, "users.db")):
                        self.fill_frame_welcome()
                        return
        self.fill_frame_firstoffline()

    def fill_frame_firstoffline(self):
        # Здесь вы можете добавить необходимые элементы во фрейм
        # Например, кнопки или другие виджеты
        self.common_label = QLabel("Добро пожаловать!", self)
        self.common_label.setStyleSheet("font-size: 24px; color: white;")
        self.adjust_label_position()

        # Создаем вертикальный макет для размещения элементов внутри фрейма
        frame_layout = self.frame.layout()

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
        self.line_edit1 = QLineEdit(self.frame)
        label2 = QLabel("Придумайте пароль:", self.frame)
        self.line_edit2 = QLineEdit(self.frame)
        label3 = QLabel("Повтор пароля:", self.frame)
        self.line_edit3 = QLineEdit(self.frame)

        # Увеличиваем высоту полей ввода
        self.line_edit1.setFixedHeight(40)
        self.line_edit2.setFixedHeight(40)
        self.line_edit3.setFixedHeight(40)
        self.line_edit2.setEchoMode(QLineEdit.Password)
        self.line_edit3.setEchoMode(QLineEdit.Password)

        # Увеличиваем размер порядковых лэйблов
        label1.setStyleSheet("font-size: 16px;")
        label2.setStyleSheet("font-size: 16px;")
        label3.setStyleSheet("font-size: 16px;")

        # Добавляем элементы в существующий макет
        frame_layout.addWidget(label1)
        frame_layout.addWidget(self.line_edit1)
        frame_layout.addWidget(label2)
        frame_layout.addWidget(self.line_edit2)
        frame_layout.addWidget(label3)
        frame_layout.addWidget(self.line_edit3)

        # Создаем лэйбл по середине
        label_center = QLabel("Ограничьте прямой доступ к папке!", self.frame)
        label_center.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(label_center)

        # Создаем кнопку "Выбрать папку для сохранения"
        self.button_choose_folder = QPushButton("Выбрать папку для сохранения данных", self.frame)
        self.button_choose_folder.setStyleSheet("font-size: 18px;")
        frame_layout.addWidget(self.button_choose_folder)
        self.button_choose_folder.setFixedHeight(50)  # Изменяем высоту кнопки

        # Отступ между кнопками
        frame_layout.addSpacing(20)

        # Создаем кнопку "Подтвердить"
        button_confirm = QPushButton("Подтвердить", self.frame)
        button_confirm.setStyleSheet("font-size: 18px;")
        frame_layout.addWidget(button_confirm)

        # Помещаем кнопки по центру
        frame_layout.setAlignment(Qt.AlignCenter)
        self.button_choose_folder.clicked.connect(self.handle_choose_folder_click)
        button_confirm.clicked.connect(self.handle_confirm_click)

    def handle_choose_folder_click(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения", "/")
        if self.folder_path:
            print("Выбранная папка:", self.folder_path)
            # Изменяем текст кнопки на "Сохранить в: {ПУТЬ}"
            self.button_choose_folder.setText("Выбранная директория: " + self.folder_path)

    def handle_confirm_click(self):
        # Проверка заполнения всех полей и соответствия паролей
        line_edits = [self.line_edit1, self.line_edit2, self.line_edit3]
        labels = ["Логин", "Пароль", "Повтор пароля"]
        for line_edit, label in zip(line_edits, labels):
            text = line_edit.text()
            if not text:
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Предупреждение")
                msg_box.setText(f"Необходимо заполнить поле: {label}!")
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.exec_()
                return

        if self.line_edit2.text() != self.line_edit3.text():
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Предупреждение")
            msg_box.setText("Пароли не совпадают!")
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.exec_()
            return

        # Проверка выбора папки для сохранения
        if not hasattr(self, 'folder_path') or not self.folder_path:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Предупреждение")
            msg_box.setText("Путь сохранения не выбран!")
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.exec_()
            return

        # Проверка на наличие недопустимых символов
        valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        for line_edit in line_edits:
            text = line_edit.text()
            if not all(char in valid_chars for char in text):
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Предупреждение")
                msg_box.setText("Можно вводить только латиницу, цифры и допустимые символы!")
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.exec_()
                return

        # Если все проверки пройдены успешно, выводим сообщение об успешном сохранении
        print("Все данные заполнены корректно.")
        with open("config.txt", "r") as file:
            lines = file.readlines()
        if len(lines) >= 2:
            # Замена второй строки
            lines[1] = f"catalog={self.folder_path}\n"
        else:
            # Если не хватает строк, добавляем новую строку
            lines.append(f"catalog={self.folder_path}\n")

        # Запись изменений в файл
        with open("config.txt", "w") as file:
            file.writelines(lines)

        data1 = self.line_edit1.text()
        data2 = self.line_edit2.text()
        data3 = self.line_edit3.text()

        # Создание базы данных SQLite
        db_path = os.path.join(self.folder_path, "users.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Создание таблицы и вставка данных
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                    id INTEGER PRIMARY KEY,
                                    data1 TEXT,
                                    data2 TEXT,
                                    data3 TEXT
                                )''')

        data_tuple = (data1, data2, data3)
        cursor.execute('''INSERT INTO users (data1, data2, data3) VALUES (?, ?, ?)''', data_tuple)

        # Сохранение изменений и закрытие соединения
        conn.commit()
        conn.close()
        self.clear_frame()
        self.fill_frame_welcome()

    def fill_frame_welcome(self):
        #self.clear_frame()

        self.common_label = QLabel("Добро пожаловать!", self)
        self.common_label.setStyleSheet("font-size: 24px; color: white;")
        self.adjust_label_position()

        # Создаем вертикальный макет для размещения элементов внутри фрейма
        frame_layout = self.frame.layout()

        # Создаем кнопку
        button_login = QPushButton("Войти", self.frame)
        button_login.setStyleSheet("font-size: 18px;")
        frame_layout.addWidget(button_login)

        spacer_label = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)
        frame_layout.addItem(spacer_label)

        # Кнопка "Импортировать данные пользователей"
        button_register = QPushButton("Зарегистрироваться", self.frame)
        button_register.setStyleSheet("font-size: 18px;")
        frame_layout.addWidget(button_register)

        # Ширина кнопки = максимальная доступная по фрейму
        button_login.setFixedWidth(400)
        button_register.setFixedWidth(400)

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