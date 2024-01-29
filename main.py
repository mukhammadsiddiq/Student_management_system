from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QLabel, QMainWindow, QTableWidget, QTableWidgetItem, \
    QDialog, QVBoxLayout, QComboBox, QToolBar
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(500, 500)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_action_student = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_action_student.triggered.connect(self.insert_data)
        file_menu_item.addAction(add_action_student)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Course", "Name", "Module"))
        self.setCentralWidget(self.table)
        self.table.verticalHeader().setVisible(False)

        # adding toolbar and widget

        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        toolbar.addAction(add_action_student)
        toolbar.addAction(search_action)
    # loading data from database

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        print(result)
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert_data(self):
        dialog = InsertDialog()
        dialog.exec()
        
    def search(self):
        dialog = SearchDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        layout = QVBoxLayout()

        # add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # add combo box widget with study courses

        self.student_project = QComboBox()
        self.courses = ["Software Engineering", "Math", "Astronomy", "Biology", "Pysics"]
        self.student_project.addItem(self.courses)
        layout.addWidget(self.student_project)

        # add mobile phone number

        self.phone_number = QLineEdit()
        self.phone_number.setPlaceholderText("Phone number")
        layout.addWidget(self.phone_number)

        # add submit button

        button = QPushButton("Submit")
        button.clicked.connect(self.add_student)
        self.setLayout(layout)

    # function for inserting new data to database
    def add_student(self):
        name = self.student_name.text()
        course = self.student_project.itemText(self.student_project.currentIndex())
        phone = self.phone_number.text()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, phone))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        # set window title
        self.setWindowTitle("Search")
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        # create a layout and input label

        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("name")
        layout.addWidget(self.student_name)

        # create a button

        button = QPushButton("Search")
        button.clicked.connect(self.search_name)
        layout.addWidget(button)
        self.setLayout(layout)

    def search_name(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        row = list(result)
        print(row)
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            main_window.table.item(item.row(), 1).setSelected(True)
        cursor.close()
        connection.close()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())



