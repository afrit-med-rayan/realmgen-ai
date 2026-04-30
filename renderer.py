from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsEllipseItem, QGraphicsTextItem
from PySide6.QtGui import QPainter, QImage, QColor, QPixmap, QPen, QBrush, QFont
from PySide6.QtCore import Qt, Signal

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
    location_clicked = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        
    def draw_map(self, terrain_generator, region_generator=None):
        self.scene.clear()
        
        width = terrain_generator.width
        height = terrain_generator.height
        
        image = QImage(width, height, QImage.Format_RGB32)
        
        for y in range(height):
            for x in range(width):
                biome = terrain_generator.biome_map[y][x]
                color = BIOME_COLORS.get(biome, QColor("#000000"))
                image.setPixelColor(x, y, color)
                
        pixmap = QPixmap.fromImage(image)
        self.map_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.map_item)
        self.scene.setSceneRect(0, 0, width, height)
        
        if region_generator:
            self._draw_locations(region_generator.locations)

    def _draw_locations(self, locations):
        for loc in locations:
            x, y = loc['x'], loc['y']
            loc_type = loc['type']
            name = loc['name']
            
            size = 6
            color = QColor("#FFFFFF")
            if loc_type == "Kingdom":
                size = 12
                color = QColor("#FFD700")
            elif loc_type == "Village":
                size = 6
                color = QColor("#8D6E63")
            elif loc_type == "Castle":
                size = 10
                color = QColor("#E0E0E0")
            elif loc_type == "Dungeon":
                size = 8
                color = QColor("#E53935")
            elif loc_type == "Ruin":
                size = 7
                color = QColor("#9E9E9E")
                
            ellipse = QGraphicsEllipseItem(x - size/2, y - size/2, size, size)
            ellipse.setBrush(QBrush(color))
            ellipse.setPen(QPen(Qt.black))
            ellipse.setToolTip(f"{name} ({loc_type})")
            ellipse.location_data = loc
            
            self.scene.addItem(ellipse)
            
            # Draw text label for Kingdoms
            if loc_type == "Kingdom":
                text = QGraphicsTextItem(name)
                text.location_data = loc
                text.setDefaultTextColor(Qt.black)
                font = QFont("Arial", 8, QFont.Bold)
                text.setFont(font)
                text.setPos(x - text.boundingRect().width()/2, y + size/2)
                self.scene.addItem(text)

    def wheelEvent(self, event):
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor
        
        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor
            
        self.scale(zoom_factor, zoom_factor)

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        if hasattr(item, "location_data"):
            self.location_clicked.emit(item.location_data)
        super().mousePressEvent(event)

