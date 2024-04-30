from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout

class CustomWidget(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window  # Сохраняем ссылку на MainWindow

        # Создаем вертикальный компоновщик для кнопок слева
        left_layout = QVBoxLayout()

        # Создаем кнопки слева
        for i in range(3):
            button = QPushButton(f"Left Button {i+1}")
            button.clicked.connect(self.clear_layout)  # Подключаем кнопку к слоту go_to_main
            left_layout.addWidget(button)

        # Создаем вертикальный компоновщик для кнопок справа
        right_layout = QVBoxLayout()

        # Создаем кнопки справа
        for i in range(3):
            button = QPushButton(f"Right Button {i+1}")
            right_layout.addWidget(button)

        # Создаем горизонтальный компоновщик для размещения кнопок слева и справа
        main_layout = QHBoxLayout(self)
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

    def clear_layout(self):
        # Удаляем все дочерние элементы из макета главного окна
        while self.main_window.main_layout.count():
            item = self.main_window.main_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Вызываем метод setup_interface из MainWindow
        self.main_window.setup_interface()