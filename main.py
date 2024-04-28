import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
import sqlite3


class DatabaseManager:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                               (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
        self.connection.commit()

    def add_user(self, name, age):
        self.cursor.execute('''INSERT INTO users (name, age) VALUES (?, ?)''', (name, age))
        self.connection.commit()

    def search_users_by_name(self, name):
        self.cursor.execute('''SELECT * FROM users WHERE name LIKE ?''', ('%' + name + '%',))
        return self.cursor.fetchall()

    def get_all_users(self):
        self.cursor.execute('''SELECT * FROM users''')
        return self.cursor.fetchall()


class UserInputApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Input")
        self.db_manager = DatabaseManager("user_data.db")
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Name input
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit()
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # Age input
        age_layout = QHBoxLayout()
        age_layout.addWidget(QLabel("Age:"))
        self.age_input = QLineEdit()
        age_layout.addWidget(self.age_input)
        layout.addLayout(age_layout)

        # Submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.save_user_data)
        layout.addWidget(self.submit_button)

        # Search input
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search by Name:"))
        self.search_input = QLineEdit()
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Search button
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_user_data)
        layout.addWidget(self.search_button)

        # Show all button
        self.show_all_button = QPushButton("Show All")
        self.show_all_button.clicked.connect(self.show_all_users)
        layout.addWidget(self.show_all_button)

    def save_user_data(self):
        name = self.name_input.text()
        age = self.age_input.text()
        if name and age:
            try:
                age = int(age)
                self.db_manager.add_user(name, age)
                QMessageBox.information(self, "Success", "User data saved successfully!")
                self.name_input.clear()
                self.age_input.clear()
            except ValueError:
                QMessageBox.warning(self, "Error", "Age must be a number.")
        else:
            QMessageBox.warning(self, "Error", "Please enter both name and age.")

    def search_user_data(self):
        name = self.search_input.text()
        if name:
            users = self.db_manager.search_users_by_name(name)
            if users:
                QMessageBox.information(self, "Search Results", f"Found users:\n{users}")
            else:
                QMessageBox.warning(self, "Search Results", "No users found with that name.")
        else:
            QMessageBox.warning(self, "Error", "Please enter a name to search.")

    def show_all_users(self):
        users = self.db_manager.get_all_users()
        if users:
            QMessageBox.information(self, "All Users", f"All users:\n{users}")
        else:
            QMessageBox.warning(self, "All Users", "No users in the database.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UserInputApp()
    window.show()
    sys.exit(app.exec())