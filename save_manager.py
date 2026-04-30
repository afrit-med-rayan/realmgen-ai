import json

class SaveManager:
    def __init__(self):
        pass
        
    def save_world(self, filepath, world_data):
        with open(filepath, 'w') as f:
            json.dump(world_data, f, indent=4)
            
    def load_world(self, filepath):
        with open(filepath, 'r') as f:
            return json.load(f)

    def export_to_png(self, filepath, map_renderer):
        # Render the graphics scene to an image
        scene = map_renderer.scene
        # Force a scene rect update to ensure everything fits
        scene_rect = scene.itemsBoundingRect()
        
        # We need PySide6 imports for this, so let's import them locally to avoid circular dependencies
        from PySide6.QtGui import QImage, QPainter
        from PySide6.QtCore import QSize
        
        image = QImage(scene_rect.size().toSize(), QImage.Format_ARGB32)
        image.fill(0) # transparent or background color
        
        painter = QPainter(image)
        scene.render(painter)
        painter.end()
        
        image.save(filepath, "PNG")
