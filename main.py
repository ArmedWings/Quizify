import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFrame, \
    QSizePolicy, QSpacerItem, QGraphicsOpacityEffect, QMessageBox
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QRect, QMargins, QTimer, QSequentialAnimationGroup, QCoreApplication, Signal, QPoint
from PySide6.QtGui import QPixmap, QPainter, QBrush, QLinearGradient, QColor, QImage, QPalette, QPen, QCursor
from cryptography.fernet import Fernet

from Auth import Auth
from custom_widget import CustomWidget


class GradientBorderFrame(QFrame):
    def __init__(self, gradient_color1, gradient_color2, parent=None):
        super().__init__(parent)
        self.gradient_color1 = gradient_color1
        self.gradient_color2 = gradient_color2
        self.setMinimumSize(200, 250)
        self.group_size = QSize(280, self.minimumHeight())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient(self.rect().topLeft(), self.rect().topRight())
        gradient.setColorAt(0, self.gradient_color1)
        gradient.setColorAt(1, self.gradient_color2)

        pen = QPen(QBrush(gradient), 4)  # Ширина обводки здесь 4 пикселя, можно изменить
        painter.setPen(pen)
        painter.drawRoundedRect(self.rect(), 20, 20)  # 20 - радиус скругления углов, можно изменить

        # Остальной код без изменений

    def calculate_group_size(self):
        total_height = 0
        max_width = 0

        # Обходим дочерние виджеты
        for i in range(self.layout().count()):
            child = self.layout().itemAt(i).widget()
            if child is not None:
                total_height += child.height()
                max_width = max(max_width, child.width())

        # Добавляем к высоте промежуты между элементами
        total_height += (self.layout().count() - 1) * 21  # Предполагаемый интервал в 30 пикселей

        return QSize(max_width, total_height)

    def enterEvent(self, event):
        self.anim = QPropertyAnimation(self, b"size")
        self.anim.setDuration(200)
        self.anim.setStartValue(self.size())
        self.anim.setEndValue(self.calculate_group_size() * 1.1)  # Увеличиваем размер на 10%
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.start()

    def leaveEvent(self, event):
        self.anim = QPropertyAnimation(self, b"size")
        self.anim.setDuration(200)
        self.anim.setStartValue(self.size())
        self.anim.setEndValue(self.calculate_group_size())  # Возвращаемся к исходному размеру
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.start()


class GroupWidget(QWidget):
    clicked = Signal(int)

    def __init__(self, index, icon_path, gradient_color1, gradient_color2, label_text, description_texts, parent=None):
        super().__init__(parent)
        self.setMinimumSize(200, 250)

        layout = QVBoxLayout(self)

        width_widget = QWidget()
        width_widget.setFixedSize(250, 1)
        layout.addWidget(width_widget)

        # hex_color = gradient_color1

        # Преобразование HEX в RGB
        # rgb_color = tuple(int(hex_color[i:i + 2], 16) for i in (1, 3, 5))

        self.outer_frame = GradientBorderFrame(gradient_color1, gradient_color2, self)
        self.outer_frame.setCursor(QCursor(Qt.PointingHandCursor))
        self.outer_frame.mousePressEvent = lambda event: self.handle_mouse_press_event(event, index)
        self.outer_frame.setStyleSheet(
            "QWidget {"
            f"  background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba({gradient_color2.red()}, {gradient_color2.green()}, {gradient_color2.blue()}, 0.05), stop:1 rgba({gradient_color1.red()}, {gradient_color1.green()}, {gradient_color1.blue()}, 0.05));"
            "   border-radius: 17px;"
            "}"
            "QWidget:hover {"
            f"   background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba({gradient_color2.red()}, {gradient_color2.green()}, {gradient_color2.blue()}, 0.4), stop:1 rgba({gradient_color1.red()}, {gradient_color1.green()}, {gradient_color1.blue()}, 0.4));"  # Градиент с прозрачным начальным цветом и прозрачностью в конечном цвете
            "   border-radius: 17px;"
            "}"

        )
        self.outer_frame.setWindowOpacity(0.1)
        self.outer_frame.setFixedWidth(280)

        layout.addWidget(self.outer_frame, alignment=Qt.AlignCenter)

        layout_outer_frame = QVBoxLayout(self.outer_frame)
        spacer_item = QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout_outer_frame.addItem(spacer_item)

        icon_widget = QLabel()
        icon_widget.setAlignment(Qt.AlignCenter)
        icon_pixmap = self.load_and_render_svg(icon_path, gradient_color1, gradient_color2)
        icon_pixmap = icon_pixmap.scaled(QSize(150, 150), Qt.KeepAspectRatio)
        icon_widget.setPixmap(icon_pixmap)
        layout_outer_frame.addWidget(icon_widget, alignment=Qt.AlignCenter)

        spacer_item = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout_outer_frame.addItem(spacer_item)

        # Create a horizontal layout for the line and its margins
        line_layout = QHBoxLayout()
        line_layout.addSpacerItem(QSpacerItem(30, 1, QSizePolicy.Fixed, QSizePolicy.Fixed))  # Add left margin
        gradient_line = QFrame()
        gradient_line.setFixedWidth(2)
        gradient_line.setFixedHeight(50)  # Set fixed width to 250 pixels
        gradient_line.setFrameShape(QFrame.HLine)
        gradient_line.setStyleSheet(
            "border: 0px; background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {}, stop:1 {}); border-radius: 1px;".format(
                gradient_color1.name(), gradient_color2.name()))
        line_layout.addWidget(gradient_line, alignment=Qt.AlignCenter)
        line_layout.addSpacerItem(QSpacerItem(30, 1, QSizePolicy.Fixed, QSizePolicy.Fixed))  # Add right margin
        layout_outer_frame.addLayout(line_layout)  # Add the line layout to the outer frame layout

        spacer_item = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout_outer_frame.addItem(spacer_item)

        name = QLabel(label_text)
        name.setAlignment(Qt.AlignCenter)
        name.setStyleSheet("font-size: 16pt; background: transparent;")
        layout_outer_frame.addWidget(name, alignment=Qt.AlignCenter)

        spacer_item = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout_outer_frame.addItem(spacer_item)

        for text, color in description_texts:
            label = QLabel(text)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: {}; border: 0px; background: transparent; font-size: 10pt;".format(color))
            layout_outer_frame.addWidget(label, alignment=Qt.AlignCenter)

        icon_widget.setStyleSheet("""
                    QLabel {
                        border: 0px;
                        background: transparent;
                    }
                """)

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

    def handle_mouse_press_event(self, event, index):
        # Получение координат курсора мыши относительно внешнего фрейма
        cursor_pos = event.position()

        # Проверка, находится ли курсор в пределах внешнего фрейма
        if self.outer_frame.rect().contains(cursor_pos.toPoint()):
            # Ваш код для обработки события нажатия на внешний фрейм
            print(f"Нажатие на внешний фрейм {index}")
            if index < 3:
                try:
                    with open("config.txt", "r") as file:
                        lines = file.readlines()
                except FileNotFoundError:
                    # Если файл не найден, создаем его и записываем в него значение mode=index
                    with open("config.txt", "w") as file:
                        file.write(f"mode={index}\n")
                    self.clicked.emit(index)
                else:
                    lines[0] = f"mode={index}\n"

                    with open("config.txt", "w") as file:
                        file.writelines(lines)

                    self.clicked.emit(index)
            else:
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Внимание")
                msg_box.setText("На данный момент недоступно")
                msg_box.exec()



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Группы кнопок")
        self.setMinimumSize(1000, 600)
        self.key = self.load_or_generate_key()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Устанавливаем стили
        self.setStyleSheet("""
                    QMainWindow {
                        background-color: #1C1B1B; /* черно-серый цвет фона */
                    }
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
                    QPushButton {
                        background-color: #191919; /* серый цвет кнопок */
                        color: white; /* белый цвет текста на кнопках */
                        border-radius: 15px; /* скругление углов кнопок */
                        padding: 10px; /* отступ вокруг текста кнопок */
                        border: 1px solid #7E7E7E;
                    }
                    QPushButton:hover {
                        background-color: #111111; /* изменение цвета при наведении на кнопку */
                    }
                    QLabel {
                        color: white; /* устанавливаем белый цвет текста на иконках */
                    }
                """)

        # Изменяем на горизонтальный компоновщик
        self.main_layout = QHBoxLayout(central_widget)
        mode = self.get_config_mode()
        if mode == 1:
            self.ismainfocus = False
            self.auth_widget = Auth(main_window=self, gradient_color1="#D660F2", gradient_color2="#5A42D6")
            self.main_layout.addWidget(self.auth_widget)
        else:
            self.setup_interface()
        # Вызываем функцию для настройки интерфейса


    def get_config_mode(self):
        config_filename = "config.txt"
        try:
            with open(config_filename, 'r') as config_file:
                first_line = config_file.readline().strip()
                if first_line.startswith("mode="):
                    mode_value = first_line.split("=")[1]
                    try:
                        mode_number = int(mode_value)
                        print("Правда: mode =", mode_number)
                        return mode_number
                    except ValueError:
                        pass
        except FileNotFoundError:
            pass
        print("Неправда")
        return None

    def setup_interface(self):
        self.ismainfocus = True

        # Создаем горизонтальный компоновщик для групп кнопок
        horizontal_layout = QHBoxLayout()

        # Группа 1
        self.group1_widget = GroupWidget(1, "icons/pc.svg", QColor("#D660F2"), QColor("#5A42D6"), "Оффлайн",
                                    [
                                        ("✅ Использование без интернета", "#D3D3D3"),
                                        ("✅ Простая настройка", "#D3D3D3"),
                                        ("⚠️ Локальный доступ", "#D3D3D3"),
                                        ("❌ Низкая безопасность БД", "#D3D3D3"),
                                    ])

        horizontal_layout.addWidget(self.group1_widget)

        # Группа 2
        self.group2_widget = GroupWidget( 2,"icons/network.svg", QColor("#6942D6"), QColor("#29B2D5"), "Децентрализованный",
                                    [
                                        ("✅ Доступ с любого компьютера", "#D3D3D3"),
                                        ("✅ Высокая безопасность БД", "#D3D3D3"),
                                        ("⚠️ Требуется доступ к сети", "#D3D3D3"),
                                        ("❌ Требуется открытая MySQL БД", "#D3D3D3")
                                    ])

        horizontal_layout.addWidget(self.group2_widget)

        # Группа 3
        self.group3_widget = GroupWidget(3,"icons/internet.svg", QColor("#2667C9"), QColor("#46C1F8"), "Централизованный",
                                    [
                                        ("✅ Простая настройка", "#D3D3D3"),
                                        ("✅ Доступ с любого компьютера", "#D3D3D3"),
                                        ("✅ Крайне высокая безопасность БД", "#D3D3D3"),
                                        ("⚠️ Требуется доступ к сети", "#D3D3D3")
                                    ])

        horizontal_layout.addWidget(self.group3_widget)

        self.group1_widget.clicked.connect(lambda: self.clear_layout(1))
        self.group2_widget.clicked.connect(lambda: self.clear_layout(2))
        self.group3_widget.clicked.connect(lambda: self.clear_layout(3))

        self.main_layout.addLayout(horizontal_layout)

        # Создаем лэйбл
        self.common_label = QLabel("Выберите режим", self)
        self.common_label.setStyleSheet("font-size: 24px; color: white;")

        # Перемещаем лэйбл по центру над группами кнопок
        self.adjust_label_position()

        self.common_label.show()
    def clear_layout(self, group):
        # Создаем список виджетов для удаления
        widgets_to_remove = [self.group3_widget, self.group2_widget, self.group1_widget]

        # Удаляем все виджеты из списка
        for widget in widgets_to_remove:
            widget.deleteLater()
        self.common_label.deleteLater()

        self.ismainfocus = False
        #ПЕРЕХОД НА ДРУГУЮ СТРАНИЦУ
        if group == 1:

            self.auth_widget = Auth(main_window=self, gradient_color1="#D660F2", gradient_color2="#5A42D6")
            self.main_layout.addWidget(self.auth_widget)
        elif group == 2:
            self.auth_widget = Auth(main_window=self, gradient_color1="#6942D6", gradient_color2="#29B2D5")
            self.main_layout.addWidget(self.auth_widget)
            #self.custom_widget = CustomWidget(self)
            #self.main_layout.addWidget(self.custom_widget)

    def resizeEvent(self, event):
        # Пересчитываем положение метки при изменении размера окна
        if self.ismainfocus==True:
            self.adjust_label_position()

    def adjust_label_position(self):
        # Перемещаем метку по центру по вертикали
        self.common_label.adjustSize()
        x = (self.width() - self.common_label.width()) // 2
        y = (self.height() - self.common_label.height()) // 20
        self.common_label.move(x, y)

    def set_mode_and_save(self, mode):
        # Устанавливаем режим
        self.mode = mode
        # Сохраняем режим и зашифровываем его
        self.save_and_encrypt_mode()

    def save_and_encrypt_mode(self):
        encrypted_mode = self.encrypt_data(str(self.mode))
        with open("mode.txt", "wb") as file:
            file.write(encrypted_mode)
        decrypted_mode = self.decrypt_data(encrypted_mode)
        print("Дешифрованный режим из mode.txt:", decrypted_mode)


    def load_or_generate_key(self):
        try:
            with open("key.txt", "rb") as file:
                return file.read()
        except FileNotFoundError:
            key = Fernet.generate_key()
            with open("key.txt", "wb") as file:
                file.write(key)
            return key

    def encrypt_data(self, data):
        cipher_suite = Fernet(self.key)
        encrypted_data = cipher_suite.encrypt(data.encode())
        return encrypted_data

    def decrypt_data(self, encrypted_data):
        cipher_suite = Fernet(self.key)
        decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
        return decrypted_data





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())