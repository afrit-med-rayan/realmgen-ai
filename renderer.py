from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsRectItem, QGraphicsTextItem
from PySide6.QtGui import QPainter, QImage, QColor, QPixmap, QPen, QBrush, QFont
from PySide6.QtCore import Qt, Signal

BIOME_COLORS = {
    "Ocean": QColor("#1A3A5A"),     # Deep sea blue
    "Mountains": QColor("#5A5255"), # Rugged grey-brown
    "Desert": QColor("#D4B872"),    # Sandy gold
    "Swamp": QColor("#3D4C3A"),     # Murky green
    "Forest": QColor("#2D4A22"),    # Deep woodland green
    "Tundra": QColor("#D1D5D8"),    # Frosty white/grey
    "Plains": QColor("#7A9648")     # Vibrant grass green
}

class MapRenderer(QGraphicsView):
    location_clicked = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        # Pixel art style: no antialiasing
        self.location_items = []
        
    def filter_locations(self, search_text, visible_types):
        search_text = search_text.lower()
        for item in self.location_items:
            loc = getattr(item, "location_data", None)
            if loc:
                matches_search = search_text in loc['name'].lower() if search_text else True
                matches_type = loc['type'] in visible_types
                item.setVisible(matches_search and matches_type)
        
    def draw_map(self, terrain_generator, region_generator=None):
        self.scene.clear()
        self.location_items.clear()
        
        width = terrain_generator.width
        height = terrain_generator.height
        
        image = QImage(width, height, QImage.Format_RGB32)
        
        for y in range(height):
            for x in range(width):
                biome = terrain_generator.biome_map[y][x]
                elev = terrain_generator.elevation_map[y][x]
                base_color = BIOME_COLORS.get(biome, QColor("#000000"))
                
                h, s, l, a = base_color.getHslF()
                
                # Quantize elevation for pixel art "banding" effect
                elev_quantized = round(elev * 10) / 10.0
                
                if biome == "Ocean":
                    l = max(0.05, l + elev_quantized * 0.4)
                elif biome == "Mountains":
                    l = min(0.95, l + (elev_quantized - 0.3) * 1.2)
                else:
                    l = max(0.1, min(0.9, l + (elev_quantized * 0.15)))
                
                color = QColor.fromHslF(h, s, l, a)
                image.setPixelColor(x, y, color)
                
        pixmap = QPixmap.fromImage(image)
        self.map_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.map_item)
        self.scene.setSceneRect(0, 0, width, height)
        
        if region_generator:
            self._draw_locations(region_generator.locations)

    def _draw_locations(self, locations):
        for loc in locations:
            x, y = int(loc['x']), int(loc['y'])
            loc_type = loc['type']
            name = loc['name']
            
            size = 6
            color = QColor("#FFFFFF")
            pen_color = QColor("#000000")
            pen_width = 1
            
            if loc_type == "Kingdom":
                size = 14
                color = QColor("#FFD700") # Gold
                pen_width = 2
            elif loc_type == "Village":
                size = 8
                color = QColor("#D2B48C") # Tan
                pen_color = QColor("#3E2723")
            elif loc_type == "Castle":
                size = 12
                color = QColor("#9E9E9E") # Silver/Grey
                pen_width = 2
            elif loc_type == "Dungeon":
                size = 10
                color = QColor("#E53935") # Red
                pen_color = QColor("#4A148C")
                pen_width = 2
            elif loc_type == "Ruin":
                size = 8
                color = QColor("#795548") # Brown
                pen_color = QColor("#212121")
                
            # Pixel art style uses sharp rectangles
            rect = QGraphicsRectItem(x - size//2, y - size//2, size, size)
            rect.setBrush(QBrush(color))
            pen = QPen(pen_color)
            pen.setWidth(pen_width)
            # Square corners for pen
            pen.setJoinStyle(Qt.MiterJoin)
            rect.setPen(pen)
            rect.setToolTip(f"{name} ({loc_type})")
            rect.location_data = loc
            
            self.scene.addItem(rect)
            self.location_items.append(rect)
            
            if loc_type == "Kingdom":
                # Pixel art font styling (using a basic clear font)
                font = QFont("Courier New", 9, QFont.Bold)
                font.setStyleHint(QFont.Monospace)
                
                # Sharp 1px shadow offset
                shadow = QGraphicsTextItem(name)
                shadow.setDefaultTextColor(QColor(0, 0, 0, 255))
                shadow.setFont(font)
                shadow.setPos(x - shadow.boundingRect().width()/2 + 1, y + size//2 + 1)
                shadow.location_data = loc
                self.scene.addItem(shadow)
                self.location_items.append(shadow)
                
                text = QGraphicsTextItem(name)
                text.location_data = loc
                text.setDefaultTextColor(QColor("#FFFFFF"))
                text.setFont(font)
                text.setPos(x - text.boundingRect().width()/2, y + size//2)
                self.scene.addItem(text)
                self.location_items.append(text)

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

