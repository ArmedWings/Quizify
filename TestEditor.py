


import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTimeEdit
from PySide6.QtCore import Qt, QTime

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

    def cancel_clicked(self):
        print("Отмена")
        # Дополнительные действия по желанию

    def edit_questions_clicked(self):
        print("Редактировать вопросы")
        # Дополнительные действия по желанию

    def save_clicked(self):
        print("Сохранить")
        # Дополнительные действия по желанию
