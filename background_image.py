from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel

class BackgroundImage:
    def __init__(self, parent):
        self.parent = parent
        self.label = QLabel(self.parent)
        self.label.setGeometry(0, 0, 1280, 720)

    def set_background_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)
