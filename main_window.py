from PyQt6.QtWidgets import (
    QApplication, QLabel, QMainWindow, QGraphicsDropShadowEffect, QScrollBar, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSpinBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My First PyQt App")
        self.setGeometry(100, 100, 1280, 720)

        # Background
        self.label = QLabel(self)
        pixmap = QPixmap(r"Backgrounds\background1.jpg")  # Replace with your background image
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)
        self.label.setGeometry(0, 0, 1280, 720)  # Cover the whole window

        # Initialize the overlay images list
        self.overlay_images = self.load_images("Physique")  # Folder with body PNGs
        self.current_image_index = 0  # Start with the first image

        # PNG Overlay (Physique)
        self.overlay_label = QLabel(self)
        self.update_overlay_image(self.overlay_images[self.current_image_index])

        # Add shadow effect to the overlay
        shadow_effect = QGraphicsDropShadowEffect(self.overlay_label)
        shadow_effect.setOffset(5, 5)  # Shadow offset (horizontal, vertical)
        shadow_effect.setBlurRadius(15)  # How blurry the shadow is
        shadow_effect.setColor(Qt.GlobalColor.black)  # Shadow color
        self.overlay_label.setGraphicsEffect(shadow_effect)

        # Setup scroll bar
        self.setup_scroll_bar()

        # Mouse wheel scrolling
        self.setMouseTracking(True)

        # Add fields for exercises
        self.add_exercise_fields()

    def load_images(self, folder_path):
        image_paths = []
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.png'):
                image_paths.append(os.path.join(folder_path, file_name))
        return image_paths

    def update_overlay_image(self, image_path):
        overlay_pixmap = QPixmap(image_path)
        self.overlay_label.setPixmap(overlay_pixmap)
        self.overlay_label.setScaledContents(True)

        # Center the overlay image
        overlay_width = overlay_pixmap.width()
        overlay_height = overlay_pixmap.height()
        x_pos = (self.width() - overlay_width) // 2
        y_pos = (self.height() - overlay_height) // 2
        self.overlay_label.setGeometry(x_pos, y_pos - 10, overlay_width, overlay_height)  # Slightly lifted

    def on_scroll(self):
        value = self.scroll_bar.value()
        if value != self.current_image_index:
            self.current_image_index = value
            self.update_overlay_image(self.overlay_images[self.current_image_index])

    def eventFilter(self, obj, event):
        if obj == self.scroll_bar and event.type() == event.Type.Wheel:
            delta = event.angleDelta().y()
            if delta > 0:
                new_value = min(self.scroll_bar.value() + 1, self.scroll_bar.maximum())
            else:
                new_value = max(self.scroll_bar.value() - 1, self.scroll_bar.minimum())
            self.scroll_bar.setValue(new_value)
            return True
        return super().eventFilter(obj, event)

    def wheelEvent(self, event):
        """
        Handle mouse wheel scrolling to shuffle images.
        """
        delta = event.angleDelta().y()  # Get the scroll direction
        if delta > 0:  # Scrolling up
            new_value = min(self.scroll_bar.value() + 1, self.scroll_bar.maximum())
        else:  # Scrolling down
            new_value = max(self.scroll_bar.value() - 1, self.scroll_bar.minimum())
        
        self.scroll_bar.setValue(new_value)  # Update the scroll bar value
        self.on_scroll()  # Trigger the image update

    def resizeEvent(self, event):
        # Recenter the image and adjust the scroll bar when the window is resized
        self.update_overlay_image(self.overlay_images[self.current_image_index])

        # Adjust the scroll bar width to match the overlay image width
        overlay_width = self.overlay_label.width()
        scroll_bar_x = (self.width() - overlay_width) // 2  # Center the scroll bar
        self.scroll_bar.setGeometry(scroll_bar_x, self.height() - 50, overlay_width, 10)  # Adjust position and width
        super().resizeEvent(event)

    def setup_scroll_bar(self):
        # Scroll Bar (Wheel-based)
        self.scroll_bar = QScrollBar(Qt.Orientation.Horizontal, self)
        self.scroll_bar.setGeometry(100, 650, 1080, 15)  # Initial position (will be resized dynamically)
        self.scroll_bar.setMaximum(len(self.overlay_images) - 1)  # Set maximum based on images
        self.scroll_bar.setMinimum(0)
        self.scroll_bar.setValue(self.current_image_index)  # Set initial value
        self.scroll_bar.setPageStep(1)  # One step per image
        self.scroll_bar.setSingleStep(1)

        # Style the scroll bar to make it sleek and modern
        self.scroll_bar.setStyleSheet("""
            QScrollBar:horizontal {
                background: transparent;  /* Transparent background */
                height: 10px;  /* Reduce thickness */
                border-radius: 5px;  /* Round edges */
            }
            QScrollBar::handle:horizontal {
                background: #A0A0A0;  /* Subtle gray color for the handle */
                border-radius: 5px;  /* Round edges for the handle */
                min-width: 20px;  /* Minimum width for the handle */
            }
            QScrollBar::handle:horizontal:hover {
                background: #808080;  /* Darker gray when hovered */
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                background: none;  /* Remove arrows */
                width: 0px;
            }
        """)

        self.scroll_bar.valueChanged.connect(self.on_scroll)
        self.scroll_bar.installEventFilter(self)

    def add_exercise_fields(self):
        # Create a container widget for the fields
        self.fields_container = QWidget(self)
        self.fields_container.setGeometry(50, 50, 200, 600)  # Left side

        # Create a vertical layout for the fields
        layout = QVBoxLayout(self.fields_container)

        # Add fields for exercises
        self.add_field(layout, "Pushups")
        self.add_field(layout, "Situps")
        self.add_field(layout, "Crunches")
        self.add_field(layout, "Kilometers Ran")

        self.fields_container.setLayout(layout)

    def add_field(self, layout, title):
        # Determine font color based on background brightness
        background_color = self.label.palette().window().color()  # Get the background color
        brightness = calculate_brightness(background_color)
        font_color = "#FFFFFF" if brightness < 0.5 else "#000000"  # White for dark backgrounds, black for light backgrounds

        # Create a container widget for the field
        field_widget = QWidget()
        field_layout = QVBoxLayout(field_widget)
        field_layout.setSpacing(8)  # Add spacing between elements

        # Add a title label
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;  /* Slightly larger font size */
                font-weight: bold;
                color: {font_color};  /* Dynamic font color */
                margin-bottom: 4px;  /* Add spacing below the title */
            }}
        """)
        field_layout.addWidget(title_label)

        # Add a spin box for the number
        spin_box = QSpinBox()
        spin_box.setRange(0, 1000)  # Set range for the number
        spin_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        spin_box.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)  # Remove default up/down buttons
        spin_box.setReadOnly(True)  # Make the field non-editable
        spin_box.setFixedWidth(80)  # Adjust width for better readability
        spin_box.setFixedHeight(40)  # Adjust height for better usability
        spin_box.setStyleSheet("""
            QSpinBox {
                background: #F0F4F8;  /* Light gray background */
                border: 1px solid #D1D9E6;  /* Subtle border */
                border-radius: 6px;  /* Rounded edges */
                padding: 4px;  /* Adjust padding for better spacing */
                font-size: 14px;  /* Slightly larger font size */
                color: #333333;  /* Dark gray text */
            }
        """)
        field_layout.addWidget(spin_box, alignment=Qt.AlignmentFlag.AlignCenter)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(0)  # Remove spacing between buttons
        button_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        # Add "-" button
        minus_button = QPushButton("-")
        minus_button.setFixedWidth(40)  # Adjust width
        minus_button.setFixedHeight(40)  # Adjust height (same as width for round shape)
        minus_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #4A90E2, stop: 1 #357ABD
                );  /* Gradient background */
                border: none;  /* No border */
                border-radius: 20px;  /* Half of the width/height for round shape */
                font-size: 14px;  /* Larger font size */
                font-weight: bold;
                color: #FFFFFF;  /* White text */
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #5BA9F2, stop: 1 #468ACD
                );  /* Lighter gradient on hover */
            }
            QPushButton:pressed {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #357ABD, stop: 1 #2C5AA0
                );  /* Darker gradient when pressed */
            }
        """)
        button_layout.addWidget(minus_button)

        # Add "+" button
        plus_button = QPushButton("+")
        plus_button.setFixedWidth(40)  # Adjust width
        plus_button.setFixedHeight(40)  # Adjust height (same as width for round shape)
        plus_button.setStyleSheet(minus_button.styleSheet())  # Use the same style as the "-" button
        button_layout.addWidget(plus_button)

        # Add shadow effect to buttons
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(10)
        shadow_effect.setOffset(2, 2)  # Subtle shadow offset
        plus_button.setGraphicsEffect(shadow_effect)
        minus_button.setGraphicsEffect(shadow_effect)

        # Connect buttons to increment and decrement the spin box
        plus_button.clicked.connect(lambda: spin_box.setValue(spin_box.value() + 1))
        minus_button.clicked.connect(lambda: spin_box.setValue(spin_box.value() - 1))

        # Add the button layout to the field layout
        field_layout.addLayout(button_layout)
        layout.addWidget(field_widget)

def calculate_brightness(color):
    """
    Calculate the brightness of a color.
    :param color: A QColor object.
    :return: A float representing brightness (0 = dark, 1 = bright).
    """
    return (color.red() * 0.299 + color.green() * 0.587 + color.blue() * 0.114) / 255

# Start the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
