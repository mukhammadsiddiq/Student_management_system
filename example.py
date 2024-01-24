from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QLabel
from datetime import datetime
import sys


class CalculateAge(QWidget):
    def __init__(self):
        super().__init__()
        grid = QGridLayout()


        # Create widget

        name_label = QLabel("Name: ")
        self.name_edit_line = QLineEdit()

        date_birth = QLabel("Date of birth MM/DD/YYYY")
        self.date_line_edit = QLineEdit()

        calculate_button = QPushButton("Calculate age")
        calculate_button.clicked.connect(self.calculate_age)
        self.output_label = QLabel("")

        # add widget to  grid

        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_edit_line, 0, 1)

        grid.addWidget(date_birth, 1, 0)
        grid.addWidget(self.date_line_edit, 1, 1)

        grid.addWidget(calculate_button, 2, 0, 1, 2)
        grid.addWidget(self.output_label, 3, 0, 1, 2)

        self.setLayout(grid)

    def calculate_age(self):
        current_year = datetime.now().year
        date_birth = self.date_line_edit.text()
        year_birth = datetime.strptime(date_birth, "%m/%d/%Y").date().year
        age = current_year - year_birth
        self.output_label.setText(f"{self.name_edit_line.text()} is {age} years old")


app = QApplication(sys.argv)
calculate_Age = CalculateAge()
calculate_Age.show()
sys.exit(app.exec())





