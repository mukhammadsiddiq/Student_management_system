from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QLabel, QMainWindow, QTableWidget, QTableWidgetItem, \
    QDialog, QVBoxLayout, QComboBox, QToolBar, QStatusBar, QMessageBox
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
        file_menu_item.addAction(add_action_student)
        add_action_student.triggered.connect(self.insert_data)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        about_action.triggered.connect(self.about)

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

        # create s atatus bar and status bar elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect s cell  click

        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Button")
        edit_button.clicked.connect(self.edit_data)

        delete_button = QPushButton("Delete Button")
        delete_button.clicked.connect(self.delete_data)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    # edit data from database

    def edit_data(self):
        dialog = EditDialog()
        dialog.exec()

    def delete_data(self):
        dialog = DeleteDialog()
        dialog.exec()

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

    # inserting data to database
    def insert_data(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """ This app was build by The student of software engineering course to manage student data,
         feel free to reuse and modify
         """
        self.setText(content)

# editing data
class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        layout = QVBoxLayout()

        # get student name from selected row
        index = main_window.table.currentRow()
        student_name = main_window.table.item(index, 1).text()

        # add student name widget
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # get id of student from the database

        self.student_id = main_window.table.item(index, 0).text()

        # add current course name
        course_name = main_window.table.item(index, 2).text()
        # add combo box widget with study courses
        self.student_project = QComboBox()
        courses = ["Software Engineering", "Math", "Astronomy", "Biology", "Physics"]

        # Add each course individually to the QComboBox
        for course in courses:
            self.student_project.addItem(course)
        self.student_project.setCurrentText(course_name)
        layout.addWidget(self.student_project)

        # add current mobile phone number
        current_number = main_window.table.item(index, 3).text()
        self.phone_number = QLineEdit(current_number)
        self.phone_number.setPlaceholderText("Phone number")
        layout.addWidget(self.phone_number)

        # add submit button

        button = QPushButton("Submit")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)  # Added the button to the layout
        self.setLayout(layout)

    def update_student(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (self.student_name.text(),
                        self.student_project.itemText(self.student_project.currentIndex()),
                        self.phone_number.text(),
                        self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        self.close()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")
        # creating a pop up for deleting student data
        layout = QGridLayout()
        confirmation = QLabel("Are you sure to delete ? ")
        yes = QPushButton("Yes")
        no = QPushButton("No")
        # small pop up window
        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)
        # connecting "yes" button to the delete method
        yes.clicked.connect(self.delete_student)
        # connecting "no" button to the delete method
        no.clicked.connect(self.cancel_delete)

    def delete_student(self):
        # getting student id and name from the cell
        index = main_window.table.currentRow()
        student_id = main_window.table.item(index, 0).text()

        # connecting database
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE from students WHERE id = ?", (student_id, ))

        connection.commit()
        cursor.close()
        connection.close()
        # loading main window to update
        main_window.load_data()

        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was deleted successfully")
        confirmation_widget.exec()

    def cancel_delete(self):
        self.close()


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
        courses = ["Software Engineering", "Math", "Astronomy", "Biology", "Physics"]

        # Add each course individually to the QComboBox
        for course in courses:
            self.student_project.addItem(course)

        layout.addWidget(self.student_project)

        # add mobile phone number

        self.phone_number = QLineEdit()
        self.phone_number.setPlaceholderText("Phone number")
        layout.addWidget(self.phone_number)

        # add submit button

        button = QPushButton("Submit")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)  # Added the button to the layout
        self.setLayout(layout)

    # function for inserting new data to database
    def add_student(self):
        name = self.student_name.text()
        course = self.student_project.currentText()
        phone = self.phone_number.text()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, phone))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        self.close()


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
        self.student_name.setPlaceholderText("Please enter full name or student ID")
        layout.addWidget(self.student_name)

        # create a button

        button = QPushButton("Search")
        button.clicked.connect(self.search_name)
        layout.addWidget(button)
        self.setLayout(layout)

    def search_name(self):
        # connecting to database and searching for the student name
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
        self.close()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
