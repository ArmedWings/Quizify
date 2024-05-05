import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QDateEdit
from PySide6.QtCore import Qt


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
        vertical_layout.addWidget(label_editing)

        vertical_layout.addSpacing(50)

        # Горизонтальные компоновщики для каждой пары лейбл-поле ввода

        # Название теста
        test_name_layout = QHBoxLayout()
        label_test_name = QLabel("Название теста:", self)
        self.test_name_edit = QLineEdit(self)
        test_name_layout.addWidget(label_test_name)
        test_name_layout.addWidget(self.test_name_edit)
        vertical_layout.addLayout(test_name_layout)

        # Горизонтальный компоновщик для "Количество попыток" и "Время на прохождение теста"
        input_layout = QHBoxLayout()

        # Вертикальный компоновщик для "Количество попыток"
        attempts_layout = QVBoxLayout()
        label_attempts = QLabel("Количество попыток:", self)
        self.attempts_edit = QLineEdit(self)
        attempts_layout.addWidget(label_attempts)
        attempts_layout.addWidget(self.attempts_edit)
        self.attempts_edit.setFixedWidth(100)  # Фиксированная ширина для поля ввода
        attempts_layout.setAlignment(Qt.Alignment.AlignLeft)
        input_layout.addLayout(attempts_layout)

        # Вертикальный компоновщик для "Время на прохождение теста"
        time_layout = QVBoxLayout()
        label_time = QLabel("Время на прохождение теста:", self)
        self.time_edit = QDateEdit(self)
        time_layout.addWidget(label_time)
        time_layout.addWidget(self.time_edit)
        self.time_edit.setFixedWidth(100)  # Фиксированная ширина для поля ввода
        time_layout.setAlignment(Qt.Alignment.AlignRight)
        input_layout.addLayout(time_layout)

        vertical_layout.addLayout(input_layout)

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