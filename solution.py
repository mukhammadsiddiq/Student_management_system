from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QLabel, QComboBox
import sys


class CalculateSpeed(QWidget):
    def __init__(self):
        super().__init__()
        grid = QGridLayout()

        # Create widget

        distance_label = QLabel("Distance")
        self.distance_line = QLineEdit()

        time_label = QLabel("Time(hours):")
        self.time_line = QLineEdit()

        self.combo = QComboBox()
        self.combo.addItems(['Metric (km)', 'Metric (Miles)'])

        calculate_button = QPushButton("Calculate")
        calculate_button.clicked.connect(self.calculate)
        self.output_label = QLabel("")

        grid.addWidget(distance_label, 0, 0)
        grid.addWidget(self.distance_line, 0, 1)
        grid.addWidget(self.combo, 0, 3)
        grid.addWidget(time_label, 1, 0)
        grid.addWidget(self.time_line, 1, 1)
        grid.addWidget(calculate_button, 2, 1)
        grid.addWidget(self.output_label, 3, 0, 1, 2)

        self.setLayout(grid)

    def calculate(self):
        distance_line = self.distance_line.text()
        time_line = self.time_line.text()
        if self.combo.currentText() == "Metric (km)":
            average_speed_km = int(distance_line) / int(time_line)
            self.output_label.setText(f"Average speed: {average_speed_km}km")
        if self.combo.currentText() == "Metric (miles)":
            average_speed_miles = int(distance_line) / int(time_line)
            self.output_label.setText(f"Average speed: {average_speed_miles} miles")


app = QApplication(sys.argv)
calculate = CalculateSpeed()
calculate.show()
sys.exit(app.exec())


