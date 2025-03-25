from PyQt6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt

class NumberFieldButtonPair(QWidget):
    def __init__(self, parent, position):
        super().__init__(parent)
        self.setGeometry(*position, 300, 200)  # Set position dynamically

        self.left_value = QLineEdit(self)
        self.left_value.setText("0")  # Default value
        self.left_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_value.setFixedWidth(100)
        self.left_value.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 180);
                border-radius: 10px;
                font-size: 20px;
                padding: 5px;
            }
        """)

        self.step_size_left = QLineEdit(self)
        self.step_size_left.setText("1")
        self.step_size_left.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.step_size_left.setFixedWidth(50)
        self.step_size_left.setStyleSheet("""
            QLineEdit {
                background-color: rgba(200, 200, 200, 180);
                border-radius: 5px;
                font-size: 16px;
                padding: 5px;
            }
        """)

        # Buttons for the left side
        self.left_increase_btn = QPushButton("+", self)
        self.left_decrease_btn = QPushButton("-", self)
        self.left_increase_btn.setFixedWidth(30)
        self.left_decrease_btn.setFixedWidth(30)

        # Buttons functionality
        self.left_increase_btn.clicked.connect(self.increase_value)
        self.left_decrease_btn.clicked.connect(self.decrease_value)

        # Layout for buttons and fields
        left_layout = QHBoxLayout(self)
        left_layout.addWidget(self.left_increase_btn)
        left_layout.addWidget(self.step_size_left)
        left_layout.addWidget(self.left_decrease_btn)
        self.setLayout(left_layout)

    def increase_value(self):
        current_value = int(self.left_value.text())
        self.left_value.setText(str(current_value + 1))

    def decrease_value(self):
        current_value = int(self.left_value.text())
        self.left_value.setText(str(current_value - 1))
