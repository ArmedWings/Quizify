

import os
import sqlite3  # Для работы с SQLite
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTimeEdit, QMessageBox
from PySide6.QtCore import Qt, QTime

class TestEditor(QWidget):
    def __init__(self, main_window=None, name=None):
        super().__init__()
        self.main_window = main_window
        self.name = name

        # Новый вертикальный компоновщик для всех элементов
        vertical_layout = QVBoxLayout(self)
        vertical_layout.setAlignment(Qt.Alignment.AlignTop)  # Выравнивание по верхнему краю
        vertical_layout.setSpacing(10)  # Отступы между элементами
        vertical_layout.setContentsMargins(10, 10, 10, 10)  # Отступы от краев окна

        vertical_layout.addSpacing(50)

        # Лэйбл "Редактирование теста"
        label_editing = QLabel("Редактирование теста", self)
        label_editing.setAlignment(Qt.Alignment.AlignCenter)  # Выравнивание по центру
        label_editing.setStyleSheet("font-size: 16pt;")  # Применение стиля CSS для изменения размера шрифта
        vertical_layout.addWidget(label_editing)

        vertical_layout.addSpacing(50)

        # Горизонтальные компоновщики для каждой пары лейбл-поле ввода

        # Название теста
        label_test_name = QLabel("Название теста:", self)
        label_test_name.setStyleSheet("font-size: 12pt;")  # Применение стиля CSS для изменения размера шрифта
        self.test_name_edit = QLineEdit(self)
        vertical_layout.addWidget(label_test_name)
        vertical_layout.addWidget(self.test_name_edit)

        # Горизонтальный компоновщик для "Количество попыток" и "Время на прохождение теста"

        # Вертикальный компоновщик для "Количество попыток"
        labels_layout = QHBoxLayout()
        label_attempts = QLabel("Количество попыток:", self)
        label_attempts.setStyleSheet("font-size: 12pt;")  # Применение стиля CSS для изменения размера шрифта
        label_time = QLabel("Время на прохождение теста (чч:мм:сс):", self)
        label_time.setStyleSheet("font-size: 12pt;")  # Применение стиля CSS для изменения размера шрифта
        labels_layout.addWidget(label_attempts)
        labels_layout.addStretch(1)
        labels_layout.addWidget(label_time)
        label_attempts.setAlignment(Qt.Alignment.AlignLeft)
        label_time.setAlignment(Qt.Alignment.AlignRight)

        # Вертикальный компоновщик для "Время на прохождение теста"
        pickers_layout = QHBoxLayout()
        self.time_edit = QTimeEdit(self)
        self.time_edit.setDisplayFormat("HH:mm:ss")  # Устанавливаем формат отображения времени
        self.time_edit.setTime(QTime(0, 0, 0))  # Устанавливаем начальное время 00:00:00
        self.attempts_edit = QLineEdit(self)
        self.attempts_edit.setInputMask("99")
        self.attempts_edit.setFixedWidth(30)  # Фиксированная ширина для поля ввода
        self.time_edit.setFixedWidth(100)  # Фиксированная ширина для поля ввода
        pickers_layout.addWidget(self.attempts_edit)
        pickers_layout.addStretch(1)
        pickers_layout.addWidget(self.time_edit)
        self.time_edit.setAlignment(Qt.Alignment.AlignRight)
        self.attempts_edit.setAlignment(Qt.Alignment.AlignLeft)

        vertical_layout.addLayout(labels_layout)
        vertical_layout.addLayout(pickers_layout)

        # Кнопки
        buttons_layout = QHBoxLayout()
        cancel_button = QPushButton("Отмена", self)
        cancel_button.setFixedSize(150, 50)  # Установка фиксированного размера кнопки
        cancel_button.setStyleSheet("font-size: 12pt; border-radius: 25px")  # Применение стиля CSS для изменения размера шрифта
        cancel_button.clicked.connect(self.cancel_clicked)
        edit_questions_button = QPushButton("Редактировать вопросы", self)
        edit_questions_button.setFixedSize(200, 50)  # Установка фиксированного размера кнопки
        edit_questions_button.setStyleSheet("font-size: 12pt; border-radius: 25px")  # Применение стиля CSS для изменения размера шрифта
        edit_questions_button.clicked.connect(self.edit_questions_clicked)
        save_button = QPushButton("Сохранить", self)
        save_button.setFixedSize(150, 50)  # Установка фиксированного размера кнопки
        save_button.setStyleSheet("font-size: 12pt; border-radius: 25px")  # Применение стиля CSS для изменения размера шрифта
        save_button.clicked.connect(self.save_clicked)
        buttons_layout.addWidget(cancel_button)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(edit_questions_button)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(save_button)
        buttons_layout.setAlignment(Qt.Alignment.AlignCenter)  # Выравнивание по центру

        # Устанавливаем горизонтальный компоновщик с кнопками внизу окна
        vertical_layout.addStretch(1)
        vertical_layout.addLayout(buttons_layout)
        if self.name is not None:
            self.populate_fields_from_database()

    def populate_fields_from_database(self):
        # Чтение пути к папке с базой данных из файла конфигурации
        config_path = "config.txt"
        folder_path = ""
        try:
            with open(config_path, "r") as config_file:
                for line in config_file:
                    if line.startswith("catalog="):
                        folder_path = line.split("catalog=")[1].strip()
                        break
        except FileNotFoundError:
            print("Файл конфигурации не найден")
            return

        # Создание пути к файлу базы данных
        db_path = os.path.join(folder_path, "tests.db")

        # Подключение к базе данных
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Выборка данных из базы данных
        cursor.execute("SELECT name, attempts, time FROM tests WHERE name = ?", (self.name,))
        test_data = cursor.fetchone()

        if test_data:
            # Заполнение полей данными из базы данных
            self.test_name_edit.setText(test_data[0])
            self.attempts_edit.setText(str(test_data[1]))
            time = QTime.fromString(test_data[2], "HH:mm:ss")
            self.time_edit.setTime(time)

        # Закрытие соединения с базой данных
        conn.close()

    def cancel_clicked(self):
        print("Отмена")

        # Проверка совпадения данных с базой
        if self.check_for_changes():
            # Если есть изменения, спросить пользователя, хочет ли он сохранить их
            reply = QMessageBox.question(None, 'Выход',
                                         'Есть несохраненные изменения. Выйти без сохранения?',
                                         QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)

            if reply == QMessageBox.Yes:
                while self.main_window.main_layout.count():
                    item = self.main_window.main_layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()
                from ModerPage import ModerPage
                moder_page = ModerPage(main_window=self.main_window, gradient_color1="#6942D6",
                                       gradient_color2="#29B2D5")
                self.main_window.main_layout.removeWidget(self)
                self.main_window.main_layout.addWidget(moder_page)
        else:
            # Если изменений нет, просто закрыть окно и вернуться на другую страницу
            while self.main_window.main_layout.count():
                item = self.main_window.main_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            from ModerPage import ModerPage
            moder_page = ModerPage(main_window=self.main_window, gradient_color1="#6942D6", gradient_color2="#29B2D5")
            self.main_window.main_layout.removeWidget(self)
            self.main_window.main_layout.addWidget(moder_page)

    def edit_questions_clicked(self):
        print("Редактировать вопросы")
        if self.check_for_changes():
            # Если есть изменения, спросить пользователя, хочет ли он сохранить их
            reply = QMessageBox.question(None, 'Сохранение',
                                         'Сохранить изменения?',
                                         QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.save_clicked()
                while self.main_window.main_layout.count():
                    item = self.main_window.main_layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()
                from QuestionEditor import QuestionEditor
                question_page = QuestionEditor(main_window=self.main_window)
                self.main_window.main_layout.removeWidget(self)
                self.main_window.main_layout.addWidget(question_page)
        else:
            # Если изменений нет, просто закрыть окно и вернуться на другую страницу
            while self.main_window.main_layout.count():
                item = self.main_window.main_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            from QuestionEditor import QuestionEditor
            question_page = QuestionEditor(main_window=self.main_window, gradient_color1="#6942D6", gradient_color2="#29B2D5")
            self.main_window.main_layout.removeWidget(self)
            self.main_window.main_layout.addWidget(question_page)

    def save_clicked(self):
        print("Сохранить")
        # Чтение пути к папке с базой данных из файла конфигурации
        config_path = "config.txt"
        folder_path = ""
        try:
            with open(config_path, "r") as config_file:
                for line in config_file:
                    if line.startswith("catalog="):
                        folder_path = line.split("catalog=")[1].strip()
                        break
        except FileNotFoundError:
            print("Файл конфигурации не найден")
            return
        print(folder_path)
        # Создание пути к файлу базы данных
        db_path = os.path.join(folder_path, "tests.db")

        # Подключение к базе данных
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Создание таблицы, если она не существует
        cursor.execute('''CREATE TABLE IF NOT EXISTS tests (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                attempts INTEGER,
                                time TEXT,
                                amount INT,
                                visible TEXT
                            )''')

        # Получение данных из полей ввода
        name = self.test_name_edit.text()
        attempts = self.attempts_edit.text()
        time = self.time_edit.time().toString("HH:mm:ss")
        amount = -1
        visible = "False"  # Устанавливаем значение "False" для новой записи

        # Проверка, создавать новую запись или редактировать существующую
        if self.name is None:
            # Создание новой записи
            cursor.execute("INSERT INTO tests (name, attempts, time, amount, visible) VALUES (?, ?, ?, ?, ?)",
                           (name, attempts, time, amount, visible))
        else:
            # Редактирование существующей записи
            cursor.execute("UPDATE tests SET name=?, attempts=?, time=?, amount=?, visible=? WHERE name=?",
                           (name, attempts, time, amount, visible, self.name))
        self.name=name
        conn.commit()
        conn.close()

        print("Данные успешно сохранены в базу данных")

    def check_for_changes(self):
        # Получение данных из полей ввода
        name = self.test_name_edit.text()
        attempts = self.attempts_edit.text()
        time = self.time_edit.time().toString("HH:mm:ss")

        # Чтение пути к папке с базой данных из файла конфигурации
        config_path = "config.txt"
        folder_path = ""
        try:
            with open(config_path, "r") as config_file:
                for line in config_file:
                    if line.startswith("catalog="):
                        folder_path = line.split("catalog=")[1].strip()
                        break
        except FileNotFoundError:
            print("Файл конфигурации не найден")
            return False

        # Создание пути к файлу базы данных
        db_path = os.path.join(folder_path, "tests.db")

        # Подключение к базе данных
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Получение данных из базы данных
        cursor.execute("SELECT * FROM tests WHERE name=?", (self.name,))
        result = cursor.fetchone()

        conn.close()

        # Проверка совпадения данных
        if result is None:
            # Запись не найдена в базе данных
            return False
        else:
            # Сравнение данных из базы данных с данными из полей ввода
            if name == result[1] and attempts == str(result[2]) and time == result[3]:
                # Данные совпадают
                return False
            else:
                # Данные не совпадают
                return True
