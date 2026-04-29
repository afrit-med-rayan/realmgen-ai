import sys
import random
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, 
                               QVBoxLayout, QPushButton, QLabel, QLineEdit, QGroupBox)
from PySide6.QtCore import Qt
from terrain_generator import TerrainGenerator
from renderer import MapRenderer

class RealmGenMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RealmGen AI - Fantasy World Generator")
        self.setGeometry(100, 100, 1280, 720)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        
        # --- Left Control Panel ---
        self.control_panel = QWidget()
        self.control_panel.setFixedWidth(250)
        self.control_layout = QVBoxLayout(self.control_panel)
        self.control_layout.setAlignment(Qt.AlignTop)
        
        # Seed Group
        self.seed_group = QGroupBox("World Seed")
        self.seed_layout = QVBoxLayout(self.seed_group)
        
        self.seed_input = QLineEdit()
        self.seed_input.setPlaceholderText("Enter seed (or leave blank)")
        self.seed_layout.addWidget(self.seed_input)
        
        self.random_seed_btn = QPushButton("Random Seed")
        self.random_seed_btn.clicked.connect(self.generate_random_seed)
        self.seed_layout.addWidget(self.random_seed_btn)
        
        self.control_layout.addWidget(self.seed_group)
        
        # Action Group
        self.action_group = QGroupBox("Generation")
        self.action_layout = QVBoxLayout(self.action_group)
        
        self.generate_btn = QPushButton("Generate World")
        self.generate_btn.clicked.connect(self.generate_world)
        self.action_layout.addWidget(self.generate_btn)
        
        self.control_layout.addWidget(self.action_group)
        
        # Status Label
        self.status_label = QLabel("Ready.")
        self.control_layout.addWidget(self.status_label)
        
        # --- Right Map Viewer ---
        self.map_renderer = MapRenderer()
        
        self.main_layout.addWidget(self.control_panel)
        self.main_layout.addWidget(self.map_renderer)

    def generate_random_seed(self):
        self.seed_input.setText(str(random.randint(0, 999999)))

    def generate_world(self):
        seed_text = self.seed_input.text()
        if seed_text.isdigit():
            seed = int(seed_text)
        else:
            seed = random.randint(0, 999999)
            self.seed_input.setText(str(seed))
            
        self.status_label.setText("Generating terrain...")
        QApplication.processEvents() # Force UI update
        
        # Map resolution
        width, height = 512, 512
        
        self.terrain = TerrainGenerator(width, height, seed)
        self.terrain.generate()
        
        self.status_label.setText("Drawing map...")
        QApplication.processEvents()
        
        self.map_renderer.draw_map(self.terrain)
        self.status_label.setText("Generation complete!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RealmGenMainWindow()
    window.show()
    sys.exit(app.exec())
