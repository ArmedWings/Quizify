from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTimeEdit, QMessageBox, QComboBox, QRadioButton, QCheckBox, QDateEdit
from PySide6.QtCore import Qt, QTime, QDate

class QuestionEditor(QWidget):
    def __init__(self, main_window=None, name=None):
        super().__init__()
        self.main_window = main_window
        self.name = name

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.Alignment.AlignTop)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        # Главный лэйбл
        self.label_editing = QLabel("Редактирование теста", self)
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
        self.score_edit.setFixedWidth(30)
        input_layout.addWidget(self.answer_type_combo)
        input_layout.addWidget(self.score_edit)
        self.answer_settings_layout.addLayout(input_layout)

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
        choice_layout = QVBoxLayout()
        choice_label = QLabel("Варианты ответов:", self)
        choice_label.setStyleSheet("font-size: 12pt;")
        choice_layout.addWidget(choice_label)

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

        choice_layout.addLayout(choice1_layout)
        choice_layout.addLayout(choice2_layout)

        self.question_layout.addLayout(choice_layout)

    def create_multi_choice_controls(self):
        self.clear_question_controls()
        multi_choice_layout = QVBoxLayout()
        multi_choice_label = QLabel("Варианты ответов:", self)
        multi_choice_label.setStyleSheet("font-size: 12pt;")
        multi_choice_layout.addWidget(multi_choice_label)
        multi_choice_checkboxes = []
        for i in range(4):  # Пример для четырех вариантов
            checkbox_layout = QHBoxLayout()
            checkbox = QCheckBox(self)
            checkbox_edit = QLineEdit(self)
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.addWidget(checkbox_edit)
            multi_choice_layout.addLayout(checkbox_layout)
            multi_choice_checkboxes.append(checkbox)
        self.question_layout.addLayout(multi_choice_layout)

    def create_text_answer_controls(self):
        self.clear_question_controls()
        text_layout = QVBoxLayout()
        text_label = QLabel("Правильный ответ:", self)
        text_label.setStyleSheet("font-size: 12pt;")
        text_edit = QLineEdit(self)
        text_layout.addWidget(text_label)
        text_layout.addWidget(text_edit)
        self.question_layout.addLayout(text_layout)

    def create_date_controls(self):
        self.clear_question_controls()
        date_layout = QVBoxLayout()
        date_label = QLabel("Правильный ответ:", self)
        date_label.setStyleSheet("font-size: 12pt;")
        date_layout.addWidget(date_label)
        date_edit = QDateEdit(self)
        date_edit.setCalendarPopup(True)
        date_edit.setDate(QDate.currentDate())
        date_layout.addWidget(date_edit)
        self.question_layout.addLayout(date_layout)

    def create_buttons(self):
        buttons_layout = QHBoxLayout()
        cancel_button = QPushButton("Отмена", self)
        cancel_button.setFixedSize(150, 50)
        cancel_button.setStyleSheet("font-size: 12pt; border-radius: 25px")
        delete_button = QPushButton("Удалить", self)
        delete_button.setFixedSize(150, 50)
        delete_button.setStyleSheet("font-size: 12pt; border-radius: 25px; border: 2px solid red;")
        save_button = QPushButton("Записать и закрыть", self)
        save_button.setFixedSize(200, 50)
        save_button.setStyleSheet("font-size: 12pt; border-radius: 25px")
        buttons_layout.addWidget(cancel_button)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(delete_button)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(save_button)
        self.main_layout.addStretch()
        self.main_layout.addLayout(buttons_layout)