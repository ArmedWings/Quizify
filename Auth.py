from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QApplication, QHBoxLayout, QSizePolicy, QSpacerItem, QLineEdit, QFileDialog, QMessageBox
from PySide6.QtGui import QPainter, QLinearGradient, QBrush, QPen, QImage, QPixmap
from PySide6.QtCore import QSize, Qt
import os
import sqlite3
import hashlib
from functools import partial

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

        self.back_icon = QLabel(self)
        back_icon_path = "icons/back.svg"  # Путь к файлу SVG
        back_icon_pixmap = self.load_and_render_svg(back_icon_path, self.gradient_color1, self.gradient_color2)
        back_icon_pixmap = back_icon_pixmap.scaled(QSize(50, 50), Qt.KeepAspectRatio)
        self.back_icon.setPixmap(back_icon_pixmap)
        #self.back_icon.mousePressEvent = self.back_icon_clicked


        # Создаем иконку "Настройки" и заполняем ее
        self.settings_icon = QLabel(self)
        settings_icon_path = "icons/settings.svg"  # Путь к файлу SVG
        settings_icon_pixmap = self.load_and_render_svg(settings_icon_path, self.gradient_color1, self.gradient_color2)
        settings_icon_pixmap = settings_icon_pixmap.scaled(QSize(50, 50), Qt.KeepAspectRatio)
        self.settings_icon.setPixmap(settings_icon_pixmap)
        #self.settings_icon.mousePressEvent = self.settings_icon_clicked

        image_size = back_icon_pixmap.size()
        self.back_icon.setFixedSize(image_size)
        self.settings_icon.setFixedSize(image_size)


        # Создаем фрейм
        self.frame = GradientBorderFrame(self.gradient_color1, self.gradient_color2, self)
        self.frame.setMinimumSize(500, 100)
        self.frame.setMaximumWidth(700)  # Ограничиваем ширину фрейма до 900 пикселей

        # Добавляем фрейм в макет
        layout.addWidget(self.frame)

        frame_layout = QVBoxLayout(self.frame)
        frame_layout.setContentsMargins(40, 40, 40, 40)
        frame_layout.setAlignment(Qt.AlignCenter)  # Выравниваем содержимое по центру

        self.common_label = QLabel("Добро пожаловать!", self)
        self.common_label.setStyleSheet("font-size: 24px; color: white;")
        self.adjust_label_position()

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

    def fill_frame_firstoffline(self, *args):
        # Здесь вы можете добавить необходимые элементы во фрейм
        # Например, кнопки или другие виджеты
        self.common_label.setText("Добро пожаловать!")
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

    def fill_frame_login(self):
        # Очистить содержимое фрейма
        self.clear_frame()

        # Изменить главный лэйбл
        self.common_label.setText("Вход")
        self.adjust_label_position()

        # Получаем текущий макет фрейма
        frame_layout = self.frame.layout()

        # Создаем лэйблы и текстовые поля вручную
        label_login = QLabel("Логин:", self.frame)
        self.line_edit_login = QLineEdit(self.frame)
        label_password = QLabel("Пароль:", self.frame)
        self.line_edit_password = QLineEdit(self.frame)
        self.line_edit_password.setEchoMode(QLineEdit.Password)

        # Увеличиваем высоту полей ввода
        self.line_edit_login.setFixedHeight(40)
        self.line_edit_password.setFixedHeight(40)

        # Увеличиваем размер порядковых лэйблов
        label_login.setStyleSheet("font-size: 16px;")
        label_password.setStyleSheet("font-size: 16px;")

        # Добавляем элементы в существующий макет
        frame_layout.addWidget(label_login)
        frame_layout.addWidget(self.line_edit_login)
        frame_layout.addWidget(label_password)
        frame_layout.addWidget(self.line_edit_password)

        spacer_label = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)
        frame_layout.addItem(spacer_label)

        # Создаем кнопку "Подтвердить"
        button_confirm = QPushButton("Подтвердить", self.frame)
        button_confirm.setStyleSheet("font-size: 18px;")
        frame_layout.addWidget(button_confirm)

        # Помещаем кнопку по центру
        frame_layout.setAlignment(Qt.AlignCenter)
        button_confirm.clicked.connect(self.handle_login_confirm_click)
        self.back_icon.mousePressEvent = self.fill_frame_welcome

    def handle_login_confirm_click(self):
        # Получаем текст из полей ввода
        login = self.line_edit_login.text()


        # Получаем путь из файла config.txt
        config_path = ""
        with open("config.txt", "r") as f:
            for line in f:
                if line.startswith("catalog="):
                    config_path = line.strip().split("=")[1]
                    break

        if not config_path:
            QMessageBox.critical(self, "Ошибка", "Не удалось найти путь к базе данных")
            return

        # Подключаемся к базе данных
        db_path = os.path.join(config_path, "users.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Поиск пользователя в базе данных
        cursor.execute('''SELECT * FROM users WHERE LOWER(login)=LOWER(?)''', (login.lower(),))
        user_data = cursor.fetchone()

        if user_data is None:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Ошибка")
            msg_box.setText("Пользователь с таким логином не найден")
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.exec_()
            return

        salt = "saltingmypc"
        password = self.line_edit_password.text()
        password_bytes = password.encode()
        salt_bytes = salt.encode()
        salted_password = password_bytes + salt_bytes
        hashed_password = hashlib.md5(salted_password)
        password = hashed_password.hexdigest()
        print(password, user_data[3])


        if user_data[3] != password:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Ошибка")
            msg_box.setText("Неверный пароль")
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.exec_()
        else:
            print("Вход выполнен успешно")
            # Дополнительные действия при успешном входе, например, переход на другую страницу или отображение основного окна приложения

        # Закрываем соединение с базой данных
        conn.close()
    def fill_frame_reg(self):
        # Очистить содержимое фрейма
        self.clear_frame()

        # Изменить главный лэйбл
        self.common_label.setText("Регистрация")
        self.adjust_label_position()

        # Получаем текущий макет фрейма
        frame_layout = self.frame.layout()

        # Создаем лэйблы и текстовые поля вручную
        label1 = QLabel("Как к вам обращаться?", self.frame)
        self.line_edit1 = QLineEdit(self.frame)
        label2 = QLabel("Придумайте логин:", self.frame)
        self.line_edit2 = QLineEdit(self.frame)
        label3 = QLabel("Придумайте пароль:", self.frame)
        self.line_edit3 = QLineEdit(self.frame)
        label4 = QLabel("Повтор пароля:", self.frame)
        self.line_edit4 = QLineEdit(self.frame)

        # Увеличиваем высоту полей ввода
        self.line_edit1.setFixedHeight(40)
        self.line_edit2.setFixedHeight(40)
        self.line_edit3.setFixedHeight(40)
        self.line_edit4.setFixedHeight(40)
        self.line_edit3.setEchoMode(QLineEdit.Password)
        self.line_edit4.setEchoMode(QLineEdit.Password)

        # Увеличиваем размер порядковых лэйблов
        label1.setStyleSheet("font-size: 16px;")
        label2.setStyleSheet("font-size: 16px;")
        label3.setStyleSheet("font-size: 16px;")
        label4.setStyleSheet("font-size: 16px;")

        # Добавляем элементы в существующий макет
        frame_layout.addWidget(label1)
        frame_layout.addWidget(self.line_edit1)
        frame_layout.addWidget(label2)
        frame_layout.addWidget(self.line_edit2)
        frame_layout.addWidget(label3)
        frame_layout.addWidget(self.line_edit3)
        frame_layout.addWidget(label4)
        frame_layout.addWidget(self.line_edit4)

        spacer_label = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)
        frame_layout.addItem(spacer_label)

        # Создаем кнопку "Подтвердить"
        button_confirm = QPushButton("Подтвердить", self.frame)
        button_confirm.setStyleSheet("font-size: 18px;")
        frame_layout.addWidget(button_confirm)

        # Помещаем кнопку по центру
        frame_layout.setAlignment(Qt.AlignCenter)
        button_confirm.clicked.connect(self.handle_reg_confirm_click)
        self.back_icon.mousePressEvent = self.fill_frame_welcome

    def handle_reg_confirm_click(self):
        # Проверка заполнения всех полей и соответствия паролей
        line_edits = [self.line_edit1, self.line_edit2, self.line_edit3, self.line_edit4]
        labels = ["Имя", "Логин", "Пароль", "Повтор пароля"]
        for line_edit, label in zip(line_edits, labels):
            text = line_edit.text()
            if not text:
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Предупреждение")
                msg_box.setText(f"Необходимо заполнить поле: {label}!")
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.exec_()
                return

        if self.line_edit3.text() != self.line_edit4.text():
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Предупреждение")
            msg_box.setText("Пароли не совпадают!")
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

        # Проверка существования пользователя в базе данных
        login = self.line_edit2.text()
        config_file_path = "config.txt"
        with open(config_file_path, "r") as file:
            lines = file.readlines()
            if len(lines) >= 2:
                folder_path = lines[1].strip().split("=")[1]
            else:
                # Вывести сообщение об ошибке, если в файле нет необходимой информации
                print("Ошибка: В файле config.txt отсутствует необходимая информация о пути к базе данных.")
                return  # Вернуться, чтобы избежать дальнейшей обработки

        # Создание пути к базе данных из пути, прочитанного из файла config.txt
        db_path = os.path.join(folder_path, "users.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM users WHERE LOWER(login)=LOWER(?)''', (login,))
        if cursor.fetchone() is not None:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Предупреждение")
            msg_box.setText("Пользователь с таким логином уже существует!")
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.exec_()
            return

        # Если все проверки пройдены успешно, выводим сообщение об успешной регистрации
        print("Все данные заполнены корректно.")
        full_name = self.line_edit1.text()
        login = self.line_edit2.text()
        password = self.line_edit3.text()
        salt = "saltingmypc"
        password_bytes = password.encode()
        salt_bytes = salt.encode()
        salted_password = password_bytes + salt_bytes
        hashed_password = hashlib.md5(salted_password)
        password = hashed_password.hexdigest()

        # Вставка данных в базу данных SQLite
        cursor.execute('''INSERT INTO users (full_name, login, password) VALUES (?, ?, ?)''',
                       (full_name, login, password))

        # Сохранение изменений и закрытие соединения
        conn.commit()
        conn.close()

        # Выводим сообщение об успешной регистрации
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Успех")
        msg_box.setText("Вы успешно зарегистрированы!")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec_()

        # Очищаем фрейм и отображаем экран приветствия
        self.clear_frame()
        self.fill_frame_welcome()

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
        self.back_icon.mousePressEvent = self.fill_frame_firstoffline

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

        full_name = "MODER"
        login = self.line_edit1.text()

        salt = "saltingmypc"
        password = self.line_edit2.text()
        password_bytes = password.encode()
        salt_bytes = salt.encode()
        salted_password = password_bytes + salt_bytes
        hashed_password = hashlib.md5(salted_password)
        password = hashed_password.hexdigest()

        # Создание базы данных SQLite
        db_path = os.path.join(self.folder_path, "users.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Создание таблицы и вставка данных
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                    id INTEGER PRIMARY KEY,
                                    full_name TEXT,
                                    login TEXT,
                                    password TEXT
                                )''')

        data_tuple = (full_name, login, password)
        cursor.execute('''INSERT INTO users (full_name, login, password) VALUES (?, ?, ?)''', data_tuple)

        # Сохранение изменений и закрытие соединения
        conn.commit()
        conn.close()
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Успех")
        msg_box.setText("Аккаунт модератора зарегистрирован!")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec_()
        self.fill_frame_welcome()

    def fill_frame_welcome(self, *args):
        self.clear_frame()

        self.common_label.setText("Добро пожаловать!")
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
        button_login.clicked.connect(self.handle_welcome_login_click)
        button_register.clicked.connect(self.handle_welcome_register_click)
        self.back_icon.mousePressEvent = self.confirm_exit

    def handle_welcome_login_click(self):
        self.fill_frame_login()
        pass

    def confirm_exit(self, event):
        reply = QMessageBox.question(None, 'Выход',
                                     'Вы уверены, что хотите выйти?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            QApplication.quit()
    def handle_welcome_register_click(self):
        self.fill_frame_reg()
        pass

    def on_resize(self, event):
        self.adjust_label_position()
    def adjust_label_position(self):
        # Перемещаем метку по центру по вертикали
        self.common_label.adjustSize()
        x = (self.width() - self.common_label.width()) // 2
        y = (self.height() - self.common_label.height()) // 20
        x_left = self.width()//30
        x_right = (self.width() - self.width()//30 - self.settings_icon.width())
        self.common_label.move(x, y)
        self.back_icon.move(x_left, y)
        self.settings_icon.move(x_right, y)

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