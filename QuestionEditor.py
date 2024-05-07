import sqlite3

from PySide6 import QtWidgets
from PySide6.QtGui import QBrush, QLinearGradient, QPainter, QImage, QPixmap
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTimeEdit, QMessageBox, QComboBox, QRadioButton, QCheckBox, QDateEdit
from PySide6.QtCore import Qt, QTime, QDate, QSize


class QuestionEditor(QWidget):
    def __init__(self, main_window=None, gradient_color1=None, gradient_color2=None, name=None):
        super().__init__()
        self.main_window = main_window
        self.name = name
        self.gradient_color1 = gradient_color1
        self.gradient_color2 = gradient_color2

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.Alignment.AlignTop)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        # Главный лэйбл
        self.label_editing = QLabel("Вопрос №1", self)
        self.label_editing.setAlignment(Qt.Alignment.AlignCenter)
        self.label_editing.setStyleSheet("font-size: 16pt;")
        self.main_layout.addWidget(self.label_editing)

        # Лэйбл и поле ввода для вопроса
        self.label_test_name = QLabel("Введите вопрос:", self)
        self.label_test_name.setStyleSheet("font-size: 12pt;")
        self.test_name_edit = QLineEdit(self)
        self.main_layout.addWidget(self.label_test_name)
        self.main_layout.addWidget(self.test_name_edit)

        # Вертикальный компоновщик для настроек ответа
        self.answer_settings_layout = QVBoxLayout()
        self.main_layout.addLayout(self.answer_settings_layout)

        # Вертикальный компоновщик для вопросов
        self.question_widget = QWidget()
        self.question_layout = QVBoxLayout(self.question_widget)
        self.main_layout.addWidget(self.question_widget)

        self.create_question_controls()

        # ИКОНКА
        self.plus_icon = QLabel(self)
        plus_icon_path = "icons/plus.svg"  # Путь к файлу SVG
        plus_icon_pixmap = self.load_and_render_svg(plus_icon_path, self.gradient_color1, self.gradient_color2)
        plus_icon_pixmap = plus_icon_pixmap.scaled(QSize(70, 70), Qt.KeepAspectRatio)
        self.plus_icon.setPixmap(plus_icon_pixmap)
        self.plus_icon.mousePressEvent = self.plus_icon_clicked
        self.plus_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.plus_icon)

        self.create_buttons()

        self.answer_type_combo.currentIndexChanged.connect(self.update_answer_controls)

    def create_question_controls(self):
        # Лэйблы типа ответа и баллов за верный ответ, их настройки
        labels_layout = QHBoxLayout()
        self.label_answer_type = QLabel("Тип ответа:", self)
        self.label_answer_type.setStyleSheet("font-size: 12pt;")
        self.label_score = QLabel("Баллов за верный ответ:", self)
        self.label_score.setStyleSheet("font-size: 12pt;")
        labels_layout.addWidget(self.label_answer_type)
        labels_layout.addStretch(1)
        labels_layout.addWidget(self.label_score)
        self.answer_settings_layout.addLayout(labels_layout)

        # Компоновщики выпадающего списка и поля ввода для баллов за верный ответ
        input_layout = QHBoxLayout()
        self.answer_type_combo = QComboBox(self)
        self.answer_type_combo.addItems(["Выбор варианта", "Выбор нескольких", "Произвольный ответ", "Выбор даты"])
        self.score_edit = QLineEdit(self)
        self.score_edit.setInputMask("99")
        #self.score_edit.setText("01")
        self.score_edit.setFixedWidth(30)
        input_layout.addWidget(self.answer_type_combo)
        input_layout.addStretch()
        input_layout.addWidget(self.score_edit)
        self.answer_settings_layout.addLayout(input_layout)
        self.create_choice_controls()

    def update_answer_controls(self, index):
        self.clear_question_controls()
        if index == 0:  # Выбор варианта
            self.create_choice_controls()
        elif index == 1:  # Выбор нескольких
            self.create_multi_choice_controls()
        elif index == 2:  # Произвольный ответ
            self.create_text_answer_controls()
        elif index == 3:  # Выбор даты
            self.create_date_controls()

    def clear_question_controls(self):
        while self.question_layout.count() > 0:
            item = self.question_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                nested_layout = item.layout()
                if nested_layout:
                    self.clear_layout(nested_layout)

    def clear_layout(self, layout):
        while layout.count() > 0:
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                nested_layout = item.layout()
                if nested_layout:
                    self.clear_layout(nested_layout)

    def create_choice_controls(self):
        self.clear_question_controls()
        choice_label = QLabel("Варианты ответов:", self)
        choice_label.setStyleSheet("font-size: 12pt;")
        self.question_layout.addWidget(choice_label)

        choice1_layout = QHBoxLayout()
        choice_radio1 = QRadioButton(self)
        choice_edit1 = QLineEdit(self)
        choice1_layout.addWidget(choice_radio1)
        choice1_layout.addWidget(choice_edit1)

        choice2_layout = QHBoxLayout()
        choice_radio2 = QRadioButton(self)
        choice_edit2 = QLineEdit(self)
        choice2_layout.addWidget(choice_radio2)
        choice2_layout.addWidget(choice_edit2)

        self.question_layout.addLayout(choice1_layout)
        self.question_layout.addLayout(choice2_layout)

    def plus_icon_clicked(self, event):
        # Проверяем, что количество элементов в self.question_layout не превышает 5
        if self.question_layout.count() <= 5:
            index = self.answer_type_combo.currentIndex()
            if index == 0:
                # Создаем горизонтальный компоновщик для радиокнопки и поля ввода
                new_layout = QHBoxLayout()

                # Создаем радиокнопку и поле ввода
                new_radio_button = QRadioButton(self)
                new_line_edit = QLineEdit(self)

                # Создаем метку для удаления строки
                delete_label = QLabel("❌", self)
                delete_label.setStyleSheet("color: red; font-size: 16pt;")

                # Привязываем функцию удаления строки к событию щелчка на метке
                delete_label.mousePressEvent = lambda event: self.delete_row(new_layout)

                # Добавляем радиокнопку, поле ввода и метку удаления в горизонтальный компоновщик
                new_layout.addWidget(new_radio_button)
                new_layout.addWidget(new_line_edit)
                new_layout.addWidget(delete_label)

                # Добавляем горизонтальный компоновщик в основной компоновщик
                self.question_layout.addLayout(new_layout)
            elif index == 1:
                # Создаем горизонтальный компоновщик для чекбокса, поля ввода и метки
                new_layout = QHBoxLayout()

                # Создаем чекбокс и поле ввода
                new_checkbox = QCheckBox(self)
                new_line_edit = QLineEdit(self)

                # Создаем метку для удаления строки
                delete_label = QLabel("❌", self)
                delete_label.setStyleSheet("color: red; font-size: 16pt;")

                # Привязываем функцию удаления строки к событию щелчка на метке
                delete_label.mousePressEvent = lambda event: self.delete_row(new_layout)

                # Добавляем чекбокс, поле ввода и метку удаления в горизонтальный компоновщик
                new_layout.addWidget(new_checkbox)
                new_layout.addWidget(new_line_edit)
                new_layout.addWidget(delete_label)

                # Добавляем горизонтальный компоновщик в основной компоновщик
                self.question_layout.addLayout(new_layout)
            elif index == 2:
                # Создаем горизонтальный компоновщик для поля ввода и метки
                new_layout = QHBoxLayout()

                # Создаем поле ввода
                new_line_edit = QLineEdit(self)

                # Создаем метку для удаления строки
                delete_label = QLabel("❌", self)
                delete_label.setStyleSheet("color: red; font-size: 16pt;")

                # Привязываем функцию удаления строки к событию щелчка на метке
                delete_label.mousePressEvent = lambda event: self.delete_row(new_layout)

                # Добавляем поле ввода и метку удаления в горизонтальный компоновщик
                new_layout.addWidget(new_line_edit)
                new_layout.addWidget(delete_label)

                # Добавляем горизонтальный компоновщик в основной компоновщик
                self.question_layout.addLayout(new_layout)
            elif index == 3:
                # Создаем горизонтальный компоновщик для выбора даты и метки
                new_layout = QHBoxLayout()

                # Создаем виджет выбора даты
                new_date_edit = QDateEdit(self)
                new_date_edit.setFixedSize(150, 30)
                new_date_edit.setDate(QDate.currentDate())
                new_date_edit.setCalendarPopup(True)

                # Создаем метку для удаления строки
                delete_label = QLabel("❌", self)
                delete_label.setStyleSheet("color: red; font-size: 16pt;")

                # Привязываем функцию удаления строки к событию щелчка на метке
                delete_label.mousePressEvent = lambda event: self.delete_row(new_layout)

                # Добавляем виджет выбора даты и метку удаления в горизонтальный компоновщик
                new_layout.addWidget(new_date_edit)
                new_layout.addWidget(delete_label)

                # Добавляем горизонтальный компоновщик в основной компоновщик
                self.question_layout.addLayout(new_layout)
        else:
            QMessageBox.warning(None, "Внимание", "Невозможно добавить больше вариантов!")

    def delete_row(self, layout):
        # Перебираем все элементы в компоновщике
        for i in reversed(range(layout.count())):
            # Получаем элемент из компоновщика
            item = layout.itemAt(i)
            # Если элемент существует
            if item is not None:
                # Удаляем его из компоновщика
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    layout.removeItem(item)

        # Удаляем компоновщик из основного компоновщика
        self.question_layout.removeItem(layout)

    def create_multi_choice_controls(self):
        self.clear_question_controls()
        choice_label = QLabel("Варианты ответов:", self)
        choice_label.setStyleSheet("font-size: 12pt;")
        self.question_layout.addWidget(choice_label)
        choice_checkboxes = []
        for i in range(2):  # Пример для четырех вариантов
            checkbox_layout = QHBoxLayout()
            checkbox = QCheckBox(self)
            checkbox_edit = QLineEdit(self)
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.addWidget(checkbox_edit)
            self.question_layout.addLayout(checkbox_layout)
            choice_checkboxes.append(checkbox)

    def create_text_answer_controls(self):
        self.clear_question_controls()
        text_layout = QHBoxLayout()
        text_label = QLabel("Правильный ответ:", self)
        text_label.setStyleSheet("font-size: 12pt;")
        text_edit = QLineEdit(self)
        text_layout.addWidget(text_edit)
        self.question_layout.addWidget(text_label)
        self.question_layout.addLayout(text_layout)

    def create_date_controls(self):
        self.clear_question_controls()
        date_layout = QHBoxLayout()
        date_label = QLabel("Правильный ответ:", self)
        date_label.setStyleSheet("font-size: 12pt;")
        self.question_layout.addWidget(date_label)
        date_edit = QDateEdit(self)
        date_edit.setCalendarPopup(True)
        date_edit.setDate(QDate.currentDate())
        date_edit.setFixedSize(150, 30)
        date_layout.addWidget(date_edit)
        date_layout.addStretch()
        self.question_layout.addLayout(date_layout)


    def create_buttons(self):
        buttons_layout1 = QHBoxLayout()
        prev_button = QPushButton("Предыдущий вопрос", self)
        prev_button.setFixedSize(200, 50)
        prev_button.setStyleSheet("font-size: 12pt; border-radius: 25px")
        prev_button.clicked.connect(self.prev_button_handler)
        next_button = QPushButton("Следующий вопрос", self)
        next_button.setFixedSize(200, 50)
        next_button.setStyleSheet("font-size: 12pt; border-radius: 25px")
        next_button.clicked.connect(self.next_button_handler)
        buttons_layout1.addWidget(prev_button)
        buttons_layout1.addStretch()
        buttons_layout1.addWidget(next_button)

        buttons_layout = QHBoxLayout()
        cancel_button = QPushButton("Отмена", self)
        cancel_button.setFixedSize(150, 50)
        cancel_button.setStyleSheet("font-size: 12pt; border-radius: 25px")
        cancel_button.clicked.connect(self.cancel_button_handler)
        delete_button = QPushButton("Удалить вопрос", self)
        delete_button.setFixedSize(150, 50)
        delete_button.setStyleSheet("font-size: 12pt; border-radius: 25px; border: 2px solid red;")
        delete_button.clicked.connect(self.delete_button_handler)
        save_button = QPushButton("Записать и закрыть", self)
        save_button.setFixedSize(200, 50)
        save_button.setStyleSheet("font-size: 12pt; border-radius: 25px")
        save_button.clicked.connect(self.save_button_handler)
        buttons_layout.addWidget(cancel_button)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(delete_button)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(save_button)
        self.main_layout.addStretch()
        self.main_layout.addLayout(buttons_layout1)
        self.main_layout.addLayout(buttons_layout)

    def prev_button_handler(self):
        pass
    def next_button_handler(self):
        pass

    def save_button_handler(self):
        print("SAVE")
        # Путь к файлу базы данных
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

        if self.answer_type_combo.currentIndex() != 3:  # Проверка индекса
            # Код для типа ответа "Текст"
            options = []
            # Перебор элементов в self.question_layout
            for i in range(self.question_layout.count()):
                vbox_layout = self.question_layout.itemAt(i).layout()
                if isinstance(vbox_layout, QtWidgets.QHBoxLayout):  # Проверка на QHBoxLayout
                    # Перебор элементов внутри QHBoxLayout
                    for k in range(vbox_layout.count()):
                        widget = vbox_layout.itemAt(k).widget()
                        if widget and isinstance(widget, QtWidgets.QLineEdit):  # Проверка на QLineEdit
                            options.append(widget.text())  # Добавление текста из LineEdit в список опций
            # Преобразование списка опций в строку с разделителем ";"
            options_str = ";".join(options)
        else:
            # Код для типа ответа "Дата"
            date_options = []
            # Перебор элементов в self.question_layout
            for i in range(self.question_layout.count()):
                vbox_layout = self.question_layout.itemAt(i).layout()
                if isinstance(vbox_layout, QtWidgets.QHBoxLayout):  # Проверка на QHBoxLayout
                    # Перебор элементов внутри QHBoxLayout
                    for k in range(vbox_layout.count()):
                        widget = vbox_layout.itemAt(k).widget()
                        if widget and isinstance(widget, QtWidgets.QDateEdit):  # Проверка на QDateEdit
                            date_options.append(widget.text())  # Добавление текста из QDateEdit в список опций
            # Преобразование списка опций в строку с разделителем ";"
            options_str = ";".join(date_options)
        #print(self.question_layout.count())
        print("варианты",options_str)

        answer = None
        answer_type_index = self.answer_type_combo.currentIndex()
        answer_index1 = []  # Создаем массив для хранения ответов в случае индекса 1

        # Перебор элементов в self.question_layout
        for i in range(self.question_layout.count()):
            vbox_layout = self.question_layout.itemAt(i).layout()
            if isinstance(vbox_layout, QtWidgets.QHBoxLayout):  # Проверка на QHBoxLayout
                if answer_type_index == 0:  # Если индекс = 0
                    # Получаем чекнутый радио-баттон из текущего QHBoxLayout
                    radio_button = vbox_layout.itemAt(0).widget()  # Первый элемент в компоновщике
                    if isinstance(radio_button,
                                  QtWidgets.QRadioButton) and radio_button.isChecked():  # Проверка на QRadioButton и чекнутость
                        # Получаем текст из QLineEdit, следующего за радио-баттоном
                        line_edit = vbox_layout.itemAt(1).widget()  # Второй элемент в компоновщике
                        if isinstance(line_edit, QtWidgets.QLineEdit):
                            answer = line_edit.text()
                            break  # Прерываем цикл, так как нашли ответ
                elif answer_type_index == 1:  # Если индекс = 1
                    radio_button = vbox_layout.itemAt(0).widget()  # Первый элемент в компоновщике
                    if isinstance(radio_button,
                                  QtWidgets.QCheckBox) and radio_button.isChecked():  # Проверка на QRadioButton и чекнутость
                        # Получаем текст из QLineEdit, следующего за радио-баттоном
                        line_edit = vbox_layout.itemAt(1).widget()  # Второй элемент в компоновщике
                        if isinstance(line_edit, QtWidgets.QLineEdit):
                            answer_index1.append(line_edit.text())  # Добавляем значение в массив
                else:
                    answer = options_str  # Остальные случаи сохраняем в переменной answer

        # Приравниваем переменную answer в зависимости от значения индекса
        if answer_type_index == 1:
            answer = ";".join(answer_index1)  # Объединяем массив в строку с разделителем ";"
        print("ответы",answer)
        # Создание соединения с базой данных
        conn = sqlite3.connect(folder_path)
        cursor = conn.cursor()

        # Создание таблицы 'questions', если она не существует
        cursor.execute('''CREATE TABLE IF NOT EXISTS questions
                              (id INTEGER PRIMARY KEY,
                               test_id INTEGER,
                               question TEXT,
                               options TEXT,
                               answer TEXT,
                               type INTEGER,
                               score INTEGER,
                               FOREIGN KEY(test_id) REFERENCES tests(id))''')

        # Получение ID теста по его имени
        test_name = self.name
        cursor.execute("SELECT id FROM tests WHERE name=?", (test_name,))
        row = cursor.fetchone()

        if row:
            test_id = row[0]

            # Получение значений для обновления в таблице 'questions'
            question = self.test_name_edit.text()
            #answer = "1"  # Теперь ответ просто берется из self.answer_edit
            answer_type = self.answer_type_combo.currentIndex()
            score = self.score_edit.text()

            # Вставка новых данных в таблицу 'questions'
            cursor.execute(
                "INSERT INTO questions (test_id, question, options, answer, type, score) VALUES (?, ?, ?, ?, ?, ?)",
                (test_id, question, options_str, answer, answer_type, score))

            # Применение изменений и закрытие соединения с базой данных
            conn.commit()
            conn.close()
        else:
            print("Тест с именем", test_name, "не найден.")
    def delete_button_handler(self):
        print("DELETE")
    def cancel_button_handler(self):
        print("CANCEL")
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