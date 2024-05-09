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
        self.question_layout.addStretch()
    def db_preset(self):
        folder_path = Funcs.get_path()
        pass
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
        #if self.questions_array[2][4][0] == '':
            #print('Пусто')

        pass
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
        pass

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
