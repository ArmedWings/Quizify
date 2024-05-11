from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QApplication, QHBoxLayout, QSizePolicy, QSpacerItem, QLineEdit, QFileDialog, QMessageBox, QScrollArea
from PySide6.QtGui import QPainter, QLinearGradient, QBrush, QPen, QImage, QPixmap
from PySide6.QtCore import QSize, Qt

import os
import sqlite3
import Funcs
class ModerPage(QWidget):
    def __init__(self, main_window=None, gradient_color1=None, gradient_color2=None, id=None):
        super().__init__()
        self.main_window = main_window
        self.gradient_color1 = gradient_color1
        self.gradient_color2 = gradient_color2
        self.id = id
        self.setup_ui()
        if self.id == 1:
            self.setup_moder()
        else:
            self.setup_user()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Создаем два фрейма
        self.frame1 = GradientBorderFrame(self.gradient_color1, self.gradient_color2)
        self.frame2 = GradientBorderFrame(self.gradient_color1, self.gradient_color2)



        # Создаем вертикальный макет для второго фрейма и добавляем отступ
        layout_frame2 = QVBoxLayout()
        layout_frame2.addSpacing(100)
        layout_frame2.addWidget(self.frame2)



        # Добавляем фреймы в главный макет
        main_layout.addWidget(self.frame1)
        main_layout.addLayout(layout_frame2)

        # Растягиваем фреймы по горизонтали
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 1)

        self.logout_icon = QLabel(self)
        logout_icon_path = "icons/logout.svg"  # Путь к файлу SVG
        logout_icon_pixmap = self.load_and_render_svg(logout_icon_path, self.gradient_color1, self.gradient_color2)
        logout_icon_pixmap = logout_icon_pixmap.scaled(QSize(50, 50), Qt.KeepAspectRatio)
        self.logout_icon.setPixmap(logout_icon_pixmap)
        self.logout_icon.setCursor(Qt.PointingHandCursor)
        self.logout_icon.mousePressEvent = self.logout_icon_clicked

        logout_size = logout_icon_pixmap.size()

        self.logout_icon.setFixedSize(logout_size)


        self.frame1_layout = QVBoxLayout()
        self.frame1.setLayout(self.frame1_layout)
        self.frame2_layout = QVBoxLayout()
        self.frame2.setLayout(self.frame2_layout)



    def setup_moder(self):
        self.plus_icon = QLabel(self)
        plus_icon_path = "icons/plus.svg"  # Путь к файлу SVG
        plus_icon_pixmap = self.load_and_render_svg(plus_icon_path, self.gradient_color1, self.gradient_color2)
        plus_icon_pixmap = plus_icon_pixmap.scaled(QSize(80, 80), Qt.KeepAspectRatio)
        self.plus_icon.setPixmap(plus_icon_pixmap)
        self.plus_icon.mousePressEvent = self.plus_icon_clicked
        plus_size = plus_icon_pixmap.size()
        self.plus_icon.setCursor(Qt.PointingHandCursor)
        self.plus_icon.setFixedSize(plus_size)

        self.back_icon = QLabel(self)
        back_icon_path = "icons/back.svg"  # Путь к файлу SVG
        back_icon_pixmap = self.load_and_render_svg(back_icon_path, self.gradient_color1, self.gradient_color2)
        back_icon_pixmap = back_icon_pixmap.scaled(QSize(50, 50), Qt.KeepAspectRatio)
        self.back_icon.setPixmap(back_icon_pixmap)
        self.back_icon.mousePressEvent = self.back_icon_handler
        back_size = back_icon_pixmap.size()
        self.back_icon.setCursor(Qt.PointingHandCursor)
        self.back_icon.setFixedSize(back_size)


        self.fill_frame1_users()
        self.fill_frame2_tests()

        self.resizeEvent = self.on_resize
        self.adjust_label_position()

    def setup_user(self):
        self.fill_frame1_allowed_tests()
        self.fill_frame2_passed_tests(self.id)
        #self.fill_frame2_tests()

        self.resizeEvent = self.on_resize
        self.adjust_label_position()

    def back_icon_handler(self, *event):
        self.fill_frame2_tests()
        self.fill_frame1_users()
    def user_button_handler(self, id):
        self.fill_frame2_passed_tests(id)
        self.back_icon.setVisible(True)
    def pass_button_handler(self, pass_id, *event):
        if self.id == 1:
            self.fill_frame1_answers(pass_id)
    def answer_button_handler(self, data, *event):
        QMessageBox.information(None, "Детальная информация",
                                f"Вопрос: {data[1]}\n"
                                f"Полученный ответ: {data[2]}\n"
                                f"Правильный ответ: {data[3]}\n"
                                f"Получено баллов: {data[4]}\n"
                                f"Максимум баллов: {data[5]}\n"
                                "Баллы начисляются за каждое совпадение с любым правильным ответом",
                                QMessageBox.Ok)
    def fill_frame1_allowed_tests(self):
        # Очистка всего содержимого frame1_layout
        while self.frame1_layout.count():
            item = self.frame1_layout.takeAt(0)
            widget = item.widget()
            layout = item.layout()

            if widget:
                widget.deleteLater()
            elif layout:
                # Рекурсивно удаляем все виджеты из layout
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()
                layout.deleteLater()  # Удаляем layout

        self.frame1_layout.addSpacing(10)
        label_users = QLabel("Доступные тестирования", self.frame1)
        label_users.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_users.setStyleSheet("font-size: 16pt;")
        self.frame1_layout.addWidget(label_users)
        self.frame1_layout.addSpacing(10)

        h_layout = QHBoxLayout()
        label_user = QLabel("Название", self.frame1)
        label_user.setStyleSheet("font-size: 14pt;")
        h_layout.addWidget(label_user)
        h_layout.addStretch()
        label_passed_tests = QLabel("Вопросов", self.frame1)
        label_passed_tests.setStyleSheet("font-size: 14pt;")
        h_layout.addWidget(label_passed_tests)
        self.frame1_layout.addLayout(h_layout)

        folder_path = Funcs.get_path()

        conn = sqlite3.connect(folder_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tests (
                                            id INTEGER PRIMARY KEY,
                                            name TEXT,
                                            attempts INTEGER,
                                            time TEXT,
                                            amount INT,
                                            visible TEXT
                                        )''')

        # Запрос на получение данных о пользователях, кроме первого
        cursor.execute("SELECT name, amount FROM tests")
        tests = cursor.fetchall()
        tests = reversed(tests)

        # Создаем экземпляр QScrollArea
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        scroll_widget = QWidget()
        scroll_widget_layout = QVBoxLayout(scroll_widget)
        # scroll_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Создание кнопок для каждого пользователя
        for test in tests:
            test_button = DualTextButton(test[0], str(test[1]), self)
            test_button.setStyleSheet("font-size: 14pt; background-color: #191919; border: 1px solid #7E7E7E;")
            test_button.setProperty("hovered", False)  # Устанавливаем начальное значение свойства для кнопки
            test_button.enterEvent = lambda event, button=test_button: button.setStyleSheet(
                "font-size: 14pt; background-color: #111111; border: 1px solid #7E7E7E;")  # Устанавливаем стиль для наведения мыши
            test_button.leaveEvent = lambda event, button=test_button: button.setStyleSheet(
                "font-size: 14pt; background-color: #191919; border: 1px solid #7E7E7E;")  # Возвращаем стиль при уходе мыши
            test_button.clicked.connect(self.to_testpassing)  # Соединяем сигнал clicked с обработчиком
            test_button.setCursor(Qt.PointingHandCursor)
            scroll_widget_layout.addWidget(test_button)
        scroll_widget_layout.addStretch()
        # Устанавливаем виджет в QScrollArea
        scroll_area.setWidget(scroll_widget)
        # scroll_area.setStyleSheet("background: black;")

        scroll_area.viewport().setStyleSheet("background: #1C1B1B; border: none;")
        conn.close()

        # Добавляем QScrollArea в ваш текущий макет
        self.frame1_layout.addWidget(scroll_area)

    def fill_frame2_passed_tests(self, user_id):
        print(user_id)
        # Очистка всего содержимого frame1_layout
        while self.frame2_layout.count():
            item = self.frame2_layout.takeAt(0)
            widget = item.widget()
            layout = item.layout()

            if widget:
                widget.deleteLater()
            elif layout:
                # Рекурсивно удаляем все виджеты из layout
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()


        folder_path = Funcs.get_path()

        conn = sqlite3.connect(folder_path)
        cursor = conn.cursor()

        cursor.execute("SELECT full_name FROM users WHERE id = ?", (user_id,))
        user_name = cursor.fetchone()

        self.frame2_layout.addSpacing(10)
        label_user = QLabel("Пользователь: "+user_name[0][:20] + "..." if len(user_name[0]) > 20 else "Пользователь: "+user_name[0], self.frame1)
        label_user.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_user.setStyleSheet("font-size: 14pt;")
        self.frame2_layout.addWidget(label_user)

        self.frame2_layout.addSpacing(8)
        label_users = QLabel("Пройденные тестирования", self.frame1)
        label_users.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_users.setStyleSheet("font-size: 16pt;")
        self.frame2_layout.addWidget(label_users)
        self.frame2_layout.addSpacing(10)

        h_layout = QHBoxLayout()
        label_user = QLabel("Название", self.frame1)
        label_user.setStyleSheet("font-size: 14pt;")
        h_layout.addWidget(label_user)
        h_layout.addStretch()
        label_passed_tests = QLabel("Баллов", self.frame1)
        label_passed_tests.setStyleSheet("font-size: 14pt;")
        h_layout.addWidget(label_passed_tests)
        self.frame2_layout.addLayout(h_layout)

        # Запрос на получение данных о пройденных тестах юзера
        cursor.execute("SELECT test_name, score, id FROM passes WHERE user_id = ?", (user_id,))
        passes = cursor.fetchall()
        passes = reversed(passes)

        # Создаем экземпляр QScrollArea
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        scroll_widget = QWidget()
        scroll_widget_layout = QVBoxLayout(scroll_widget)
        # scroll_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Создание кнопок для каждого прохождения
        for attempt in passes:
            attempt_button = DualTextButton(attempt[0], attempt[1], self)
            Funcs.set_style_scaled(attempt_button, attempt[1])
            attempt_button.setProperty("hovered", False)  # Устанавливаем начальное значение свойства для кнопки
            attempt_button.enterEvent = lambda event, element=attempt_button, score=attempt[1]: Funcs.hovered_style_scaled(
                element, score, event)
            attempt_button.leaveEvent = lambda event, element=attempt_button, score=attempt[1]: Funcs.hovered_style_scaled(
                element, score, event)
            attempt_button.setCursor(Qt.PointingHandCursor)
            attempt_button.clicked.connect(lambda checked, id_prop=attempt[2]: self.pass_button_handler(id_prop))
            scroll_widget_layout.addWidget(attempt_button)
        scroll_widget_layout.addStretch()
        # Устанавливаем виджет в QScrollArea
        scroll_area.setWidget(scroll_widget)
        # scroll_area.setStyleSheet("background: black;")

        scroll_area.viewport().setStyleSheet("background: #1C1B1B; border: none;")
        conn.close()

        # Добавляем QScrollArea в ваш текущий макет
        self.frame2_layout.addWidget(scroll_area)
        # self.frame2_layout.addStretch()

    def fill_frame1_users(self):
        self.back_icon.setVisible(False)
        # Очистка всего содержимого frame1_layout
        while self.frame1_layout.count():
            item = self.frame1_layout.takeAt(0)
            widget = item.widget()
            layout = item.layout()

            if widget:
                widget.deleteLater()
            elif layout:
                # Рекурсивно удаляем все виджеты из layout
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()
                layout.deleteLater()  # Удаляем layout

        self.frame1_layout.addSpacing(10)
        label_users = QLabel("Пользователи", self.frame1)
        label_users.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_users.setStyleSheet("font-size: 16pt;")
        self.frame1_layout.addWidget(label_users)
        self.frame1_layout.addSpacing(10)

        h_layout = QHBoxLayout()
        label_user = QLabel("Пользователь", self.frame1)
        label_user.setStyleSheet("font-size: 14pt;")
        h_layout.addWidget(label_user)
        h_layout.addStretch()
        label_passed_tests = QLabel("Пройдено тестов", self.frame1)
        label_passed_tests.setStyleSheet("font-size: 14pt;")
        h_layout.addWidget(label_passed_tests)
        self.frame1_layout.addLayout(h_layout)

        folder_path = Funcs.get_path()

        conn = sqlite3.connect(folder_path)
        cursor = conn.cursor()

        # Запрос на получение данных о пользователях, кроме первого
        cursor.execute("SELECT full_name, passed FROM users LIMIT -1 OFFSET 1")
        users = cursor.fetchall()
        id_property = len(users)+1
        users = reversed(users)
        # Создаем экземпляр QScrollArea
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)  # Позволяет автоматически изменять размеры области прокрутки

        # Создаем виджет, который будет содержать кнопки
        scroll_widget = QWidget()
        scroll_widget_layout = QVBoxLayout(scroll_widget)

        # Создание кнопок для каждого пользователя
        for user in users:
            user_button = DualTextButton(user[0], str(user[1]), self.frame1)
            user_button.setStyleSheet("font-size: 14pt; background-color: #191919; border: 1px solid #7E7E7E;")
            user_button.setProperty("hovered", False)  # Устанавливаем начальное значение свойства для кнопки
            user_button.enterEvent = lambda event, button=user_button: button.setStyleSheet(
                "font-size: 14pt; background-color: #111111; border: 1px solid #7E7E7E;")  # Устанавливаем стиль для наведения мыши
            user_button.leaveEvent = lambda event, button=user_button: button.setStyleSheet(
                "font-size: 14pt; background-color: #191919; border: 1px solid #7E7E7E;")  # Возвращаем стиль при уходе мыши
            user_button.setCursor(Qt.PointingHandCursor)
            user_button.clicked.connect(lambda checked, id_prop=id_property: self.user_button_handler(id_prop))
            scroll_widget_layout.addWidget(user_button)
            id_property -= 1
        scroll_widget_layout.addStretch()

        # Устанавливаем виджет в QScrollArea
        scroll_area.setWidget(scroll_widget)

        scroll_area.viewport().setStyleSheet("background: #1C1B1B; border: none;")
        conn.close()

        # Добавляем QScrollArea в ваш текущий макет
        self.frame1_layout.addWidget(scroll_area)

    def fill_frame2_tests(self, *event):
        # Очистка всего содержимого frame1_layout
        while self.frame2_layout.count():
            item = self.frame2_layout.takeAt(0)
            widget = item.widget()
            layout = item.layout()

            if widget:
                widget.deleteLater()
            elif layout:
                # Рекурсивно удаляем все виджеты из layout
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()

        self.frame2_layout.addSpacing(10)
        label_users = QLabel("Тестирования", self.frame1)
        label_users.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_users.setStyleSheet("font-size: 16pt;")
        self.frame2_layout.addWidget(label_users)
        self.frame2_layout.addSpacing(10)

        h_layout = QHBoxLayout()
        label_user = QLabel("Название", self.frame1)
        label_user.setStyleSheet("font-size: 14pt;")
        h_layout.addWidget(label_user)
        h_layout.addStretch()
        label_passed_tests = QLabel("Вопросов", self.frame1)
        label_passed_tests.setStyleSheet("font-size: 14pt;")
        h_layout.addWidget(label_passed_tests)
        self.frame2_layout.addLayout(h_layout)

        folder_path = Funcs.get_path()

        conn = sqlite3.connect(folder_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tests (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT,
                                    attempts INTEGER,
                                    time TEXT,
                                    amount INT,
                                    visible TEXT
                                )''')



        # Запрос на получение данных о пользователях, кроме первого
        cursor.execute("SELECT name, amount FROM tests")
        tests = cursor.fetchall()
        tests = reversed(tests)

        # Создаем экземпляр QScrollArea
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)  # Позволяет автоматически изменять размеры области прокрутки

        # Создаем виджет, который будет содержать кнопки
        scroll_widget = QWidget()
        scroll_widget_layout = QVBoxLayout(scroll_widget)
        #scroll_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Создание кнопок для каждого пользователя
        for test in tests:
            test_button = DualTextButton(test[0], str(test[1]), self)
            test_button.setStyleSheet("font-size: 14pt; background-color: #191919; border: 1px solid #7E7E7E;")
            test_button.setProperty("hovered", False)  # Устанавливаем начальное значение свойства для кнопки
            test_button.enterEvent = lambda event, button=test_button: button.setStyleSheet(
                "font-size: 14pt; background-color: #111111; border: 1px solid #7E7E7E;")  # Устанавливаем стиль для наведения мыши
            test_button.leaveEvent = lambda event, button=test_button: button.setStyleSheet(
                "font-size: 14pt; background-color: #191919; border: 1px solid #7E7E7E;")  # Возвращаем стиль при уходе мыши
            test_button.setCursor(Qt.PointingHandCursor)
            test_button.clicked.connect(self.show_selected_test)  # Соединяем сигнал clicked с обработчиком
            scroll_widget_layout.addWidget(test_button)
        scroll_widget_layout.addStretch()
        # Устанавливаем виджет в QScrollArea
        scroll_area.setWidget(scroll_widget)
        #scroll_area.setStyleSheet("background: black;")

        scroll_area.viewport().setStyleSheet("background: #1C1B1B; border: none;")
        conn.close()

        # Добавляем QScrollArea в ваш текущий макет
        self.frame2_layout.addWidget(scroll_area)
        #self.frame2_layout.addStretch()

    def fill_frame1_answers(self, pass_id, *event):
        print(pass_id)
        # Очистка всего содержимого frame1_layout
        while self.frame1_layout.count():
            item = self.frame1_layout.takeAt(0)
            widget = item.widget()
            layout = item.layout()

            if widget:
                widget.deleteLater()
            elif layout:
                # Рекурсивно удаляем все виджеты из layout
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()
                layout.deleteLater()  # Удаляем layout


        folder_path = Funcs.get_path()

        conn = sqlite3.connect(folder_path)
        cursor = conn.cursor()

        # Запрос на получение данных о пользователях, кроме первого
        cursor.execute("SELECT test_name, question, getanswer, rightanswer, getscore, maxscore FROM answers WHERE pass_id = ?", (pass_id,))
        answers = cursor.fetchall()

        self.frame1_layout.addSpacing(10)
        label_testname = QLabel("Тест: "+answers[0][0][:20] + "..." if len(answers[0][0]) > 20 else "Тест: "+answers[0][0], self.frame1)
        label_testname.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_testname.setStyleSheet("font-size: 12pt;")
        self.frame1_layout.addWidget(label_testname)

        self.frame1_layout.addSpacing(10)
        label_users = QLabel("Полученные ответы", self.frame1)
        label_users.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_users.setStyleSheet("font-size: 16pt;")
        self.frame1_layout.addWidget(label_users)
        self.frame1_layout.addSpacing(10)

        h_layout = QHBoxLayout()
        label_user = QLabel("Вопрос", self.frame1)
        label_user.setStyleSheet("font-size: 14pt;")
        h_layout.addWidget(label_user)
        h_layout.addStretch()
        label_passed_tests = QLabel("Баллов", self.frame1)
        label_passed_tests.setStyleSheet("font-size: 14pt;")
        h_layout.addWidget(label_passed_tests)
        self.frame1_layout.addLayout(h_layout)
        # Создаем экземпляр QScrollArea
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)  # Позволяет автоматически изменять размеры области прокрутки

        # Создаем виджет, который будет содержать кнопки
        scroll_widget = QWidget()
        scroll_widget_layout = QVBoxLayout(scroll_widget)
        # Создание кнопок для каждого пользователя
        for answer in answers:
            user_button = DualTextButton(answer[1][:40] + "..." if len(answer[1]) > 40 else answer[1], str(answer[4])+"/"+str(answer[5]), self.frame1)
            Funcs.set_style_scaled(user_button, str(answer[4])+"/"+str(answer[5]))
            user_button.setProperty("hovered", False)  # Устанавливаем начальное значение свойства для кнопки
            user_button.enterEvent = lambda event, element=user_button, score=str(answer[4])+"/"+str(answer[5]): Funcs.hovered_style_scaled(
                element, score, event)
            user_button.leaveEvent = lambda event, element=user_button,score=str(answer[4])+"/"+str(answer[5]): Funcs.hovered_style_scaled(
                element, score, event)
            user_button.setCursor(Qt.PointingHandCursor)
            user_button.clicked.connect(lambda checked, data=answer: self.answer_button_handler(data))
            scroll_widget_layout.addWidget(user_button)
        scroll_widget_layout.addStretch()

        # Устанавливаем виджет в QScrollArea
        scroll_area.setWidget(scroll_widget)

        scroll_area.viewport().setStyleSheet("background: #1C1B1B; border: none;")
        conn.close()

        # Добавляем QScrollArea в ваш текущий макет
        self.frame1_layout.addWidget(scroll_area)

    def to_testpassing(self):
        sender_button = self.sender()  # Получаем отправителя сигнала
        if isinstance(sender_button, DualTextButton):  # Проверяем, является ли отправитель кнопкой DualTextButton
            left_text = sender_button.left_label.text()  # Получаем текст слева от кнопки
            reply = QMessageBox.question(None, 'Начать тест?',
                                         'Вы уверены, что хотите начать тест? Это действие отменить нельзя',
                                         QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)

            if reply == QMessageBox.Yes:
                while self.main_window.main_layout.count():
                    item = self.main_window.main_layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()
                from TestPassing import TestPassing
                testpassing_page = TestPassing(main_window=self.main_window, gradient_color1=self.gradient_color1, gradient_color2=self.gradient_color2, name=left_text, user_id=self.id)
                self.main_window.main_layout.removeWidget(self)
                self.main_window.main_layout.addWidget(testpassing_page)
    def show_selected_test(self):
        sender_button = self.sender()  # Получаем отправителя сигнала
        if isinstance(sender_button, DualTextButton):  # Проверяем, является ли отправитель кнопкой DualTextButton
            left_text = sender_button.left_label.text()  # Получаем текст слева от кнопки
            print(f"Selected test: {left_text}")
            while self.main_window.main_layout.count():
                item = self.main_window.main_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            from TestEditor import TestEditor
            testeditor_page = TestEditor(main_window=self.main_window, name=left_text)
            self.main_window.main_layout.removeWidget(self)
            self.main_window.main_layout.addWidget(testeditor_page)

    def logout_icon_clicked(self, event):
        reply = QMessageBox.question(None, 'Выход',
                                     'Вы уверены, что хотите выйти из аккаунта?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            while self.main_window.main_layout.count():
                item = self.main_window.main_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            from Auth import Auth
            auth_page = Auth(main_window=self.main_window, gradient_color1="#6942D6", gradient_color2="#29B2D5")
            self.main_window.main_layout.removeWidget(self)
            self.main_window.main_layout.addWidget(auth_page)

    def plus_icon_clicked(self, event):
        reply = QMessageBox.question(None, 'Новый тест',
                                     'Создать новый тест?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            while self.main_window.main_layout.count():
                item = self.main_window.main_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            from TestEditor import TestEditor
            testeditor_page = TestEditor(main_window=self.main_window)
            self.main_window.main_layout.removeWidget(self)
            self.main_window.main_layout.addWidget(testeditor_page)

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
    def on_resize(self, event):
        self.adjust_label_position()
    def adjust_label_position(self):
        x_right = (self.width() - self.logout_icon.width())
        self.logout_icon.move(x_right, 50 - self.logout_icon.height()//2)
        if hasattr(self, 'plus_icon') and self.plus_icon is not None:
            x = (self.width() - self.width() // 4 - self.plus_icon.width() // 2)
            self.plus_icon.move(x, 50 - self.plus_icon.height() // 2)
        if hasattr(self, 'back_icon') and self.back_icon is not None:
            x = (self.width() - self.width() // 2 + self.back_icon.width() // 2)
            self.back_icon.move(x, 50 - self.back_icon.height() // 2)


class DualTextButton(QPushButton):
    def __init__(self, left_text, right_text, parent=None):
        super().__init__(parent)

        self.left_label = QLabel(left_text)
        self.right_label = QLabel(right_text)

        layout = QHBoxLayout()
        layout.addWidget(self.left_label)
        layout.addStretch(1)
        layout.addWidget(self.right_label)
        self.left_label.setStyleSheet("border: none")
        self.right_label.setStyleSheet("border: none")

        self.setLayout(layout)


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

        pen = QPen(QBrush(gradient), 4)
        painter.setPen(pen)
        painter.drawRoundedRect(self.rect(), 20, 20)