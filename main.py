import sqlite3
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


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


class UserInputApp(App):
    def build(self):
        self.db_manager = DatabaseManager("user_data.db")

        layout = GridLayout(cols=2)
        layout.add_widget(Label(text='Name:'))
        self.name_input = TextInput(multiline=False)
        layout.add_widget(self.name_input)

        layout.add_widget(Label(text='Age:'))
        self.age_input = TextInput(multiline=False)
        layout.add_widget(self.age_input)

        self.submit_button = Button(text='Submit')
        self.submit_button.bind(on_press=self.save_user_data)
        layout.add_widget(self.submit_button)

        layout.add_widget(Label(text='Search by Name:'))
        self.search_input = TextInput(multiline=False)
        layout.add_widget(self.search_input)

        self.search_button = Button(text='Search')
        self.search_button.bind(on_press=self.search_user_data)
        layout.add_widget(self.search_button)

        self.show_all_button = Button(text='Show All')
        self.show_all_button.bind(on_press=self.show_all_users)
        layout.add_widget(self.show_all_button)

        return layout

    def save_user_data(self, instance):
        name = self.name_input.text
        age = self.age_input.text
        if name and age:
            try:
                age = int(age)
                self.db_manager.add_user(name, age)
                print("User data saved successfully!")
                self.name_input.text = ''
                self.age_input.text = ''
            except ValueError:
                print("Age must be a number.")
        else:
            print("Please enter both name and age.")

    def search_user_data(self, instance):
        name = self.search_input.text
        if name:
            users = self.db_manager.search_users_by_name(name)
            if users:
                print("Found users:")
                for user in users:
                    print(user)
            else:
                print("No users found with that name.")
        else:
            print("Please enter a name to search.")

    def show_all_users(self, instance):
        users = self.db_manager.get_all_users()
        if users:
            print("All users:")
            for user in users:
                print(user)
        else:
            print("No users in the database.")


if __name__ == '__main__':
    UserInputApp().run()