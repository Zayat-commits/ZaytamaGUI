import sys
from subprocess import call

# Call preprocess.py before running main application
call([sys.executable, 'preprocess.py'])

import sys
import os
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QGraphicsDropShadowEffect, QScrollBar
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

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

        # Scroll Bar (Wheel-based)
        self.scroll_bar = QScrollBar(Qt.Orientation.Horizontal, self)
        self.scroll_bar.setGeometry(100, 650, 1080, 30)  # Adjust position under the image
        self.scroll_bar.setMaximum(len(self.overlay_images) - 1)  # Set maximum based on images
        self.scroll_bar.setMinimum(0)
        self.scroll_bar.setValue(self.current_image_index)  # Set initial value
        self.scroll_bar.setPageStep(1)  # One step per image
        self.scroll_bar.setSingleStep(1)
        self.scroll_bar.setStyleSheet("QScrollBar {height: 15px;} QScrollBar::handle:horizontal {background: lightblue;}")

        self.scroll_bar.valueChanged.connect(self.on_scroll)

        # Mouse wheel scrolling
        self.setMouseTracking(True)
        self.scroll_bar.installEventFilter(self)

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

    def resizeEvent(self, event):
        # Recenter the image and the scroll bar when the window is resized
        self.update_overlay_image(self.overlay_images[self.current_image_index])
        self.scroll_bar.setGeometry(100, self.height() - 70, 1080, 30)  # Scroll bar adjustment
        super().resizeEvent(event)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
