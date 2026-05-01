import sys
import random
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, 
                               QVBoxLayout, QPushButton, QLabel, QLineEdit, QGroupBox, QFileDialog, QCheckBox)
from PySide6.QtCore import Qt
from terrain_generator import TerrainGenerator
from region_generator import RegionGenerator
from renderer import MapRenderer
from save_manager import SaveManager

STYLESHEET = """
QMainWindow {
    background-color: #121016;
}
QWidget {
    color: #E2D9E8;
    font-family: 'Cambria', 'Georgia', serif;
    font-size: 14px;
}
QGroupBox {
    background-color: #1C1924;
    border: 1px solid #3A3248;
    border-radius: 8px;
    margin-top: 25px;
    padding: 15px 10px 10px 10px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top center;
    padding: 2px 15px;
    color: #D4AF37;
    font-size: 16px;
    font-weight: bold;
    letter-spacing: 1px;
}
QPushButton {
    background-color: #2B2338;
    border: 1px solid #483C5C;
    border-radius: 4px;
    padding: 10px 12px;
    color: #E2D9E8;
    font-weight: bold;
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
    margin-bottom: 4px;
}
QPushButton:hover {
    background-color: #3C3050;
    border-color: #D4AF37;
    color: #FFF;
}
QPushButton:pressed {
    background-color: #D4AF37;
    color: #121016;
}
QLineEdit {
    background-color: #0E0C12;
    border: 1px solid #3A3248;
    border-radius: 4px;
    padding: 8px;
    color: #E2D9E8;
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
    margin-bottom: 4px;
}
QLineEdit:focus {
    border: 1px solid #D4AF37;
}
QLabel {
    font-size: 14px;
    line-height: 1.5;
    padding: 2px 0;
}
QCheckBox {
    spacing: 8px;
    font-size: 14px;
    font-family: 'Segoe UI', sans-serif;
    margin-bottom: 4px;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    background-color: #0E0C12;
    border: 1px solid #3A3248;
    border-radius: 3px;
}
QCheckBox::indicator:checked {
    background-color: #D4AF37;
    border: 1px solid #D4AF37;
}
QGraphicsView {
    border: 2px solid #3A3248;
    border-radius: 8px;
    background-color: #0B0A10;
}
"""

class RealmGenMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(STYLESHEET)
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
        self.action_group = QGroupBox("Actions")
        self.action_layout = QVBoxLayout(self.action_group)
        
        self.generate_btn = QPushButton("Generate World")
        self.generate_btn.clicked.connect(self.generate_world)
        self.action_layout.addWidget(self.generate_btn)

        self.save_btn = QPushButton("Save World")
        self.save_btn.clicked.connect(self.save_world_data)
        self.action_layout.addWidget(self.save_btn)

        self.load_btn = QPushButton("Load World")
        self.load_btn.clicked.connect(self.load_world_data)
        self.action_layout.addWidget(self.load_btn)

        self.export_btn = QPushButton("Export to PNG")
        self.export_btn.clicked.connect(self.export_png)
        self.action_layout.addWidget(self.export_btn)
        
        self.control_layout.addWidget(self.action_group)
        
        # Filter Group
        self.filter_group = QGroupBox("Filters & Search")
        self.filter_layout = QVBoxLayout(self.filter_group)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name...")
        self.search_input.textChanged.connect(self.update_filters)
        self.filter_layout.addWidget(self.search_input)
        
        self.type_filters = {}
        for loc_type in ["Kingdom", "Village", "Castle", "Dungeon", "Ruin"]:
            cb = QCheckBox(loc_type)
            cb.setChecked(True)
            cb.stateChanged.connect(self.update_filters)
            self.filter_layout.addWidget(cb)
            self.type_filters[loc_type] = cb
            
        self.control_layout.addWidget(self.filter_group)
        
        # Legend Group
        self.legend_group = QGroupBox("Legend")
        self.legend_layout = QVBoxLayout(self.legend_group)
        
        legend_items = [
            ("Kingdom", "#FFD700", "Gold"),
            ("Castle", "#9E9E9E", "Silver"),
            ("Dungeon", "#E53935", "Red"),
            ("Village", "#D2B48C", "Tan"),
            ("Ruin", "#795548", "Brown")
        ]
        for name, color, color_name in legend_items:
            lbl = QLabel(f"■ {name}")
            lbl.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 15px;")
            self.legend_layout.addWidget(lbl)
            
        self.control_layout.addWidget(self.legend_group)
        
        # Detail Panel
        self.detail_group = QGroupBox("Location Details")
        self.detail_layout = QVBoxLayout(self.detail_group)
        
        self.detail_name_label = QLabel("Name: None")
        self.detail_type_label = QLabel("Type: None")
        self.detail_biome_label = QLabel("Biome: None")
        self.detail_ruler_label = QLabel("Ruler: None")
        self.detail_danger_label = QLabel("Danger: None")
        self.detail_lore_label = QLabel("Lore: None")
        self.detail_lore_label.setWordWrap(True)
        
        self.detail_layout.addWidget(self.detail_name_label)
        self.detail_layout.addWidget(self.detail_type_label)
        self.detail_layout.addWidget(self.detail_biome_label)
        self.detail_layout.addWidget(self.detail_ruler_label)
        self.detail_layout.addWidget(self.detail_danger_label)
        self.detail_layout.addWidget(self.detail_lore_label)
        
        self.control_layout.addWidget(self.detail_group)
        
        # Status Label
        self.status_label = QLabel("Ready.")
        self.control_layout.addWidget(self.status_label)
        
        # --- Right Map Viewer ---
        self.map_renderer = MapRenderer()
        self.map_renderer.location_clicked.connect(self.display_location_details)
        
        self.main_layout.addWidget(self.control_panel)
        self.main_layout.addWidget(self.map_renderer)
        self.save_manager = SaveManager()

    def display_location_details(self, loc_data):
        self.detail_name_label.setText(f"Name: {loc_data.get('name', 'Unknown')}")
        self.detail_type_label.setText(f"Type: {loc_data.get('type', 'Unknown')}")
        self.detail_biome_label.setText(f"Biome: {loc_data.get('biome', 'Unknown')}")
        
        lore = loc_data.get('lore', {})
        self.detail_ruler_label.setText(f"Ruler: {lore.get('ruler', 'Unknown')}")
        self.detail_danger_label.setText(f"Danger: {loc_data.get('danger_level', 'Unknown')}")
        self.detail_lore_label.setText(f"Lore: {lore.get('description', 'None')}")

    def save_world_data(self):
        if not hasattr(self, 'terrain') or not hasattr(self, 'regions'):
            self.status_label.setText("No world to save!")
            return
            
        filepath, _ = QFileDialog.getSaveFileName(self, "Save World", "", "JSON Files (*.json)")
        if filepath:
            world_data = {
                "seed": self.terrain.seed,
                "width": self.terrain.width,
                "height": self.terrain.height,
                "locations": self.regions.locations
            }
            self.save_manager.save_world(filepath, world_data)
            self.status_label.setText("World saved successfully.")

    def load_world_data(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Load World", "", "JSON Files (*.json)")
        if filepath:
            try:
                world_data = self.save_manager.load_world(filepath)
                seed = world_data["seed"]
                width = world_data["width"]
                height = world_data["height"]
                self.seed_input.setText(str(seed))
                
                self.terrain = TerrainGenerator(width, height, seed)
                self.terrain.generate()
                
                self.regions = RegionGenerator(self.terrain, seed)
                # Override locations with loaded locations
                self.regions.locations = world_data.get("locations", [])
                
                self.map_renderer.draw_map(self.terrain, self.regions)
                self.status_label.setText("World loaded successfully.")
            except Exception as e:
                self.status_label.setText(f"Error loading world: {e}")

    def export_png(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Export to PNG", "", "PNG Images (*.png)")
        if filepath:
            self.save_manager.export_to_png(filepath, self.map_renderer)
            self.status_label.setText("Exported successfully.")

    def update_filters(self):
        search_text = self.search_input.text()
        visible_types = [t for t, cb in self.type_filters.items() if cb.isChecked()]
        self.map_renderer.filter_locations(search_text, visible_types)

    def generate_random_seed(self):
        self.seed_input.setText(str(random.randint(0, 999999)))

    def generate_world(self):
        seed_text = self.seed_input.text()
        if seed_text.isdigit():
            seed = int(seed_text)
        else:
            seed = random.randint(0, 999999)
            self.seed_input.setText(str(seed))
            
        self.generate_btn.setEnabled(False)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        
        try:
            self.status_label.setText("Generating terrain... Please wait.")
            QApplication.processEvents() # Force UI update
            
            width, height = 512, 512
            
            self.terrain = TerrainGenerator(width, height, seed)
            self.terrain.generate()
            
            self.status_label.setText("Populating world... Please wait.")
            QApplication.processEvents()
            
            self.regions = RegionGenerator(self.terrain, seed)
            self.regions.generate_locations()
            
            self.status_label.setText("Drawing map... Please wait.")
            QApplication.processEvents()
            
            self.map_renderer.draw_map(self.terrain, self.regions)
            self.status_label.setText(f"Generation complete! {len(self.regions.locations)} locations found.")
        finally:
            QApplication.restoreOverrideCursor()
            self.generate_btn.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RealmGenMainWindow()
    window.show()
    sys.exit(app.exec())
