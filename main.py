from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QLabel, QMainWindow
from datetime import datetime
from PyQt6.QtGui import QAction
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        add_action_student = QAction("Add Student", self)
        file_menu_item.addAction(add_action_student)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())



