import sys
import random
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel

class RealmGenMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RealmGen AI - Fantasy World Generator")
        self.setGeometry(100, 100, 1280, 720)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        self.label = QLabel("Welcome to RealmGen AI", self)
        self.layout.addWidget(self.label)
        
        # We will add the map renderer and controls here later

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RealmGenMainWindow()
    window.show()
    sys.exit(app.exec())
