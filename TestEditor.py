import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTimeEdit
from PySide6.QtCore import Qt, QTime
from PySide6 import QtGui


class TestEditor(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window

        # Новый вертикальный компоновщик для всех элементов
        vertical_layout = QVBoxLayout(self)
        vertical_layout.setAlignment(Qt.Alignment.AlignTop)  # Выравнивание по верхнему краю
        vertical_layout.setSpacing(10)  # Отступы между элементами
        vertical_layout.setContentsMargins(10, 10, 10, 10)  # Отступы от краев окна

        vertical_layout.addSpacing(50)

        # Лэйбл "Редактирование теста"
        label_editing = QLabel("Редактирование теста", self)
        label_editing.setAlignment(Qt.Alignment.AlignCenter)  # Выравнивание по центру
        label_editing.setFont(QtGui.QFont("Arial", 16))  # Установка крупного шрифта
        vertical_layout.addWidget(label_editing)

        vertical_layout.addSpacing(50)

        # Горизонтальные компоновщики для каждой пары лейбл-поле ввода

        # Название теста
        label_test_name = QLabel("Название теста:", self)
        label_test_name.setFont(QtGui.QFont("Arial", 12))  # Установка крупного шрифта
        self.test_name_edit = QLineEdit(self)
        vertical_layout.addWidget(label_test_name)
        vertical_layout.addWidget(self.test_name_edit)

        # Горизонтальный компоновщик для "Количество попыток" и "Время на прохождение теста"

        # Вертикальный компоновщик для "Количество попыток"
        labels_layout = QHBoxLayout()
        label_attempts = QLabel("Количество попыток:", self)
        label_attempts.setFont(QtGui.QFont("Arial", 12))  # Установка крупного шрифта
        label_time = QLabel("Время на прохождение теста (чч:мм:сс):", self)
        label_time.setFont(QtGui.QFont("Arial", 12))  # Установка крупного шрифта
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
        edit_questions_button = QPushButton("Редактировать вопросы", self)
        save_button = QPushButton("Сохранить", self)
        buttons_layout.addWidget(cancel_button)
        buttons_layout.addWidget(edit_questions_button)
        buttons_layout.addWidget(save_button)
        buttons_layout.setAlignment(Qt.Alignment.AlignCenter)  # Выравнивание по центру

        # Устанавливаем горизонтальный компоновщик с кнопками внизу окна
        vertical_layout.addStretch(1)
        vertical_layout.addLayout(buttons_layout)