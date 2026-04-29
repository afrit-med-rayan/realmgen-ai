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
