import sqlite3
import random

from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QBrush, QLinearGradient, QPainter, QImage, QPixmap
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QTimeEdit, QMessageBox, QComboBox, QRadioButton, QCheckBox, QDateEdit, QScrollArea, QSizePolicy, QPlainTextEdit
from PySide6.QtCore import Qt, QTime, QDate, QSize

import Funcs


class TestPassing(QWidget):
    def __init__(self, main_window=None, gradient_color1=None, gradient_color2=None, name=None, user_id=None):
        super().__init__()
        self.main_window = main_window
        self.gradient_color1 = gradient_color1
        self.gradient_color2 = gradient_color2
        self.name = name
        self.user_id = user_id

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.Alignment.AlignTop)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        # Главный лэйбл
        self.label_editing = QLabel("Вопрос №1", self)
        self.label_editing.setAlignment(Qt.Alignment.AlignCenter)
        self.label_editing.setStyleSheet("font-size: 18pt;")
        self.main_layout.addWidget(self.label_editing)
        self.main_layout.addSpacing(20)

        self.label_question = QLabel("")
        self.label_question.setStyleSheet("font-size: 18pt;")
        self.main_layout.addWidget(self.label_question)

        self.main_layout.addSpacing(20)

        self.label_choose = QLabel("Выберите вариант:", self)
        self.label_choose.setStyleSheet("font-size: 12pt;")
        self.main_layout.addWidget(self.label_choose)
        # Лэйбл и поле ввода для вопроса
        #self.main_layout.addWidget(self.test_name_edit)

        # Вертикальный компоновщик для настроек ответа
        self.answer_settings_layout = QVBoxLayout()
        self.main_layout.addLayout(self.answer_settings_layout)

        # Вертикальный компоновщик для вопросов
        self.question_widget = QWidget()
        self.question_layout = QVBoxLayout(self.question_widget)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Делаем содержимое листающимся
        scroll_area.viewport().setStyleSheet("background: #1C1B1B; border: none;")
        scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Устанавливаем виджет с вопросами в QScrollArea
        scroll_area.setWidget(self.question_widget)

        # Добавляем QScrollArea в основной лейаут вашего окна
        self.main_layout.addWidget(scroll_area)

        #Получение вопросника
        self.get_array()
        #Запись предварительных (пустых) результатов в новую запись
        self.db_preset()
        #Подготовка вспомогательного массива
        self.page_init()

        #Объявление и подгрузка первой страницы
        self.question_number = 0
        self.total_getscore = 0
        self.question_load()
        #UI
        self.create_buttons()

    def page_init(self):
        print(self.questions_array)
        for i in range(len(self.questions_array)):
            first, second, third, fourth, fifth, *rest = self.questions_array[i]  # Разбиваем элементы на отдельные переменные
            fourth_elements = tuple(fourth.split(';')) if isinstance(fourth,
                                                                   str) else fourth  # Разбиваем третий элемент, если он строка
            fifth_elements = tuple(fifth.split(';')) if isinstance(fifth,
                                                                     str) else fifth  # Разбиваем четвертый элемент, если он строка
            self.questions_array[i] = (first, second, third, fourth_elements, fifth_elements, *rest)  # Обновляем элементы внутреннего списка
        #random.shuffle(self.questions_array)

    def question_load(self):
        self.clear_question_controls()
        self.label_editing.setText("Вопрос №" + str(self.question_number + 1))
        self.label_question.setText(self.questions_array[self.question_number][2])
        if self.questions_array[self.question_number][5] < 2:
            for option in self.questions_array[self.question_number][3]:
                option_layout = QHBoxLayout()
                new_option = QLabel(option)
                new_option.setStyleSheet("font-size: 14pt")
                if self.questions_array[self.question_number][5] == 0:
                    new_radio = QRadioButton()
                    option_layout.addWidget(new_radio)
                elif self.questions_array[self.question_number][5] == 1:
                    new_check = QCheckBox()
                    option_layout.addWidget(new_check)
                option_layout.addWidget(new_option)
                option_layout.addStretch()
                self.question_layout.addLayout(option_layout)
        elif self.questions_array[self.question_number][5] == 2:
            option_layout = QHBoxLayout()
            new_lineedit = QLineEdit()
            self.apply_custom_style(new_lineedit)
            option_layout.addWidget(new_lineedit)
            option_layout.addStretch()
            self.question_layout.addLayout(option_layout)
        else:
            option_layout = QHBoxLayout()
            new_dateedit = QDateEdit()
            new_dateedit.setStyleSheet("background: #2C2C2C; color: white")
            new_dateedit.setCalendarPopup(True)
            new_dateedit.setDate(QDate.currentDate())
            new_dateedit.setDisplayFormat("dd.MM.yyyy")
            new_dateedit.setFixedSize(150, 30)
            option_layout.addWidget(new_dateedit)
            option_layout.addStretch()
            self.question_layout.addLayout(option_layout)
        self.question_layout.addStretch()
    def db_preset(self):
        folder_path = Funcs.get_path()
        try:
            conn = sqlite3.connect(folder_path)
            cursor = conn.cursor()

            cursor.execute('''
                        CREATE TABLE IF NOT EXISTS passes (
                            id INTEGER PRIMARY KEY,
                            user_id INTEGER,
                            test_name TEXT,
                            questions_amount INTEGER,
                            score TEXT,
                            FOREIGN KEY(user_id) REFERENCES users(id)
                        )
                    ''')
            cursor.execute('''
                        CREATE TABLE IF NOT EXISTS answers (
                            id INTEGER PRIMARY KEY,
                            user_id INTEGER,
                            pass_id INTEGER,
                            test_name TEXT,
                            question TEXT,
                            options TEXT,
                            getanswer TEXT,
                            rightanswer TEXT,
                            type INTEGER,
                            getscore INTEGER,
                            maxscore INTEGER,
                            FOREIGN KEY(user_id) REFERENCES users(id),
                            FOREIGN KEY(pass_id) REFERENCES passes(id)
                        )
                    ''')
            #записываем предварительные данные
            cursor.execute('''
                INSERT INTO passes (user_id, test_name, questions_amount) 
                VALUES (?, ?, ?)
            ''', (self.user_id, self.name, len(self.questions_array)))
            self.pass_id = cursor.lastrowid


            for question in self.questions_array:
                if question[5] == 1:
                    maxscore = question[6] * len(question[4].split(';'))
                else:
                    maxscore = question[6]
                cursor.execute('''
                    INSERT INTO answers (user_id, pass_id, test_name, question, options, rightanswer, type, getscore, maxscore) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (self.user_id, self.pass_id, self.name, question[2], question[3], question[4], question[5], 0, maxscore))
            conn.commit()
            cursor.execute('''
                SELECT SUM(maxscore) FROM answers 
                WHERE user_id = ? AND pass_id = ?
            ''', (self.user_id, self.pass_id))

            # Получение результата запроса
            self.total_max_score = cursor.fetchone()[0]

            cursor.execute('''
                UPDATE passes 
                SET score = ? 
                WHERE id = ?
            ''', ("0/"+str(self.total_max_score), self.pass_id))
            conn.commit()

            conn.close()

        except sqlite3.Error as e:
            print("Ошибка SQLite:", e)

    def get_array(self):
        try:
            # Подключение к базе данных
            folder_path = Funcs.get_path()
            conn = sqlite3.connect(folder_path)
            cursor = conn.cursor()

            # Получение test_id из таблицы tests по имени теста
            cursor.execute("SELECT id FROM tests WHERE name=?", (self.name,))
            test_id = cursor.fetchone()

            if test_id:
                test_id = test_id[0]
                # Выбор всех записей из таблицы questions с соответствующим test_id
                cursor.execute("SELECT * FROM questions WHERE test_id=?", (test_id,))
                questions_data = cursor.fetchall()

                # Преобразование данных в квадратный массив
                self.questions_array = []
                for row in questions_data:
                    self.questions_array.append(row)  # Добавление строки в массив
                conn.close()
                # Теперь у вас есть квадратный массив questions_array с информацией о вопросах


            else:
                print("Тест с именем '{}' не найден.".format(self.name))
                conn.close()

        except sqlite3.Error as e:
            print("Ошибка SQLite:", e)


    def create_buttons(self):
        buttons_layout = QHBoxLayout()
        prev_button = QPushButton("Предыдущий вопрос", self)
        prev_button.setFixedSize(200, 50)
        prev_button.setStyleSheet("font-size: 12pt; border-radius: 25px")
        prev_button.clicked.connect(self.prev_button_handler)
        end_button = QPushButton("Завершить тестирование", self)
        end_button.setFixedSize(220, 50)
        end_button.setStyleSheet("font-size: 12pt; border-radius: 25px; border: 2px solid red;")
        end_button.clicked.connect(self.end_button_handler)
        next_button = QPushButton("Следующий вопрос", self)
        next_button.setFixedSize(200, 50)
        next_button.setStyleSheet("font-size: 12pt; border-radius: 25px")
        next_button.clicked.connect(self.next_button_handler)

        set_answer = QPushButton("Ответить", self)
        set_answer.setFixedSize(150, 50)
        set_answer.setStyleSheet("font-size: 12pt; border-radius: 25px;")
        set_answer.clicked.connect(self.answer_button_handler)
        self.main_layout.addWidget(set_answer,alignment=Qt.AlignmentFlag.AlignCenter)

        buttons_layout.addWidget(prev_button)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(end_button)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(next_button)
        self.main_layout.addLayout(buttons_layout)

    def answer_button_handler(self):
        folder_path = Funcs.get_path()

        #ПОДСЧЕТ БАЛЛОВ ЗА КОНКРЕТНЫЙ ВОПРОС
        getscore = 0
        answer_type_index = self.questions_array[self.question_number][5]
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
                        if isinstance(line_edit, QtWidgets.QLabel):
                            answer_index1.append(line_edit.text())
                elif answer_type_index == 1:  # Если индекс = 1
                    radio_button = vbox_layout.itemAt(0).widget()  # Первый элемент в компоновщике
                    if isinstance(radio_button,
                                  QtWidgets.QCheckBox) and radio_button.isChecked():  # Проверка на QRadioButton и чекнутость
                        # Получаем текст из QLineEdit, следующего за радио-баттоном
                        line_edit = vbox_layout.itemAt(1).widget()  # Второй элемент в компоновщике
                        if isinstance(line_edit, QtWidgets.QLabel):
                            answer_index1.append(line_edit.text())  # Добавляем значение в массив
                elif answer_type_index == 2:  # Если индекс = 2
                    line_edit = vbox_layout.itemAt(0).widget()  # Первый элемент в компоновщике
                    if isinstance(line_edit, QtWidgets.QLineEdit):
                        answer_index1.append(line_edit.text())  # Добавляем значение в массив
                elif answer_type_index == 3:  # Если индекс = 3
                    date_edit = vbox_layout.itemAt(0).widget()  # Первый элемент в компоновщике
                    if isinstance(date_edit, QtWidgets.QDateEdit):
                        answer_index1.append(date_edit.date().toString("dd.MM.yyyy"))
        print(answer_index1)
        getanswer = ";".join(answer_index1)
        #Рассчет полученных баллов за ответ
        for answer in answer_index1:
            if answer in self.questions_array[self.question_number][4]:
                getscore += self.questions_array[self.question_number][6]
            else:
                #За ошибочный ответ в мультивыборе (лишний) вычитается в два раза больше баллов
                getscore -= self.questions_array[self.question_number][6]*2
        if getscore < 0:
            getscore = 0
        #ЗАПИСЬ
        try:
            conn = sqlite3.connect(folder_path)
            cursor = conn.cursor()

            # Получаем id записи в таблице answers для указанного порядкового номера вопроса
            cursor.execute('''
                SELECT id 
                FROM answers 
                WHERE user_id=? AND pass_id=? 
                LIMIT 1 OFFSET ?
            ''', (self.user_id, self.pass_id, self.question_number))

            answer_id = cursor.fetchone()[0]

            # Обновляем данные в таблице answers
            cursor.execute('''
                UPDATE answers 
                SET getanswer=?, getscore=? 
                WHERE id=?
            ''', (getanswer, getscore, answer_id))

            # Сохраняем изменения в базе данных
            conn.commit()

            cursor.execute('''
                            SELECT SUM(getscore) FROM answers 
                            WHERE user_id = ? AND pass_id = ?
                        ''', (self.user_id, self.pass_id))

            # Получение результата запроса
            self.total_getscore = cursor.fetchone()[0]

            cursor.execute('''
                            UPDATE passes 
                            SET score = ? 
                            WHERE id = ?
                        ''', (str(self.total_getscore)+"/" + str(self.total_max_score), self.pass_id))
            conn.commit()

        except sqlite3.Error as e:
            print("Ошибка SQLite:", e)
        finally:
            conn.close()
    def prev_button_handler(self):
        if self.question_number > 0:
            self.question_number -= 1
        else:
            self.question_number = len(self.questions_array)-1
        self.question_load()
    def next_button_handler(self):
        if self.question_number < len(self.questions_array)-1:
            self.question_number += 1
        else:
            self.question_number = 0
        self.question_load()
    def end_button_handler(self):
        reply = QMessageBox.question(None, 'Завершить тестирование',
                                     'Вы уверены, что хотите завершить тестирование? Вы не сможете продолжить',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            while self.main_window.main_layout.count():
                item = self.main_window.main_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            score_scaled = Funcs.score_scaled(self.total_getscore, self.total_max_score)
            QMessageBox.information(None, "Результат",
                                    f"Вы завершили тестирование с результатом:\n"
                                    f"Получено баллов: {self.total_getscore}\n"
                                    f"Максимум баллов: {self.total_max_score}\n"
                                    f"Оценка по пятибалльной шкале: {score_scaled}",
                                    QMessageBox.Ok)
            from ModerPage import ModerPage
            moder_page = ModerPage(main_window=self.main_window, gradient_color1="#6942D6", gradient_color2="#29B2D5", id=self.user_id)
            self.main_window.main_layout.removeWidget(self)
            self.main_window.main_layout.addWidget(moder_page)

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
    def apply_custom_style(self, widget):
        widget.setStyleSheet(
                    '''
                QLineEdit {
                        background-color: #2C2C2C; /* темно-серый цвет поля ввода */
                        border: 1px solid #7E7E7E; /* цвет рамки */
                        color: white; /* белый цвет текста */
                        selection-background-color: #0078D7; /* цвет выделенного текста */
                        font-size: 20px;
                    }
                    QLineEdit:focus {
                        border: 2px solid #0078D7; /* цвет рамки при фокусе */
                    }
                ''')