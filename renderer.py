from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtGui import QPainter, QImage, QColor, QPixmap
from PySide6.QtCore import Qt

BIOME_COLORS = {
    "Ocean": QColor("#1E88E5"),
    "Mountains": QColor("#757575"),
    "Desert": QColor("#FFD54F"),
    "Swamp": QColor("#556B2F"),
    "Forest": QColor("#2E7D32"),
    "Tundra": QColor("#CFD8DC"),
    "Plains": QColor("#81C784")
}

class MapRenderer(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        # Enable dragging to pan
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        
        self.map_item = QGraphicsPixmapItem()
        self.scene.addItem(self.map_item)

    def draw_map(self, terrain_generator):
        width = terrain_generator.width
        height = terrain_generator.height
        
        # Create an image to draw the terrain pixel by pixel
        image = QImage(width, height, QImage.Format_RGB32)
        
        for y in range(height):
            for x in range(width):
                biome = terrain_generator.biome_map[y][x]
                color = BIOME_COLORS.get(biome, QColor("#000000"))
                image.setPixelColor(x, y, color)
                
        # Update the pixmap
        pixmap = QPixmap.fromImage(image)
        self.map_item.setPixmap(pixmap)
        
        # Adjust scene rect to match image
        self.scene.setSceneRect(0, 0, width, height)

    def wheelEvent(self, event):
        # Zoom functionality
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor
        
        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor
            
        self.scale(zoom_factor, zoom_factor)
