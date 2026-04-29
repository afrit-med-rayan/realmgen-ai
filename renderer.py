from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtGui import QPainter

class MapRenderer(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        
        # To be implemented: zoom, pan, and draw map
        
    def draw_map(self, terrain_data):
        pass
