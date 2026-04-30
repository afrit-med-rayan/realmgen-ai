import random
from name_generator import NameGenerator
from lore_generator import LoreGenerator

class RegionGenerator:
    def __init__(self, terrain_data, seed: int):
        self.terrain_data = terrain_data
        self.rng = random.Random(seed)
        self.name_gen = NameGenerator(seed)
        self.lore_gen = LoreGenerator(seed)
        self.locations = []
        
    def generate_locations(self, num_attempts=1000):
        width = self.terrain_data.width
        height = self.terrain_data.height
        
        for _ in range(num_attempts):
            x = self.rng.randint(0, width - 1)
            y = self.rng.randint(0, height - 1)
            
            biome = self.terrain_data.biome_map[y][x]
            if biome == "Ocean":
                continue
                
            location_type = self._determine_location_type(biome)
            if location_type:
                name = self.name_gen.generate_name(location_type)
                danger = self._determine_danger(biome, location_type)
                
                # Check minimum distance to avoid overlapping
                if not self._is_too_close(x, y):
                    lore = self.lore_gen.generate_lore(location_type, biome, danger)
                    self.locations.append({
                        "name": name,
                        "x": x,
                        "y": y,
                        "type": location_type,
                        "biome": biome,
                        "danger_level": danger,
                        "lore": lore
                    })
                    
    def _determine_location_type(self, biome: str):
        roll = self.rng.random()
        
        if biome in ["Plains", "Forest"]:
            if roll < 0.05: return "Kingdom"
            if roll < 0.25: return "Village"
        elif biome == "Mountains":
            if roll < 0.15: return "Castle"
            if roll < 0.25: return "Dungeon"
        elif biome in ["Desert", "Tundra"]:
            if roll < 0.15: return "Ruin"
        elif biome == "Swamp":
            if roll < 0.25: return "Dungeon"
            
        return None
        
    def _determine_danger(self, biome: str, loc_type: str) -> str:
        if loc_type == "Dungeon": return "Extreme"
        if loc_type == "Ruin": return "High"
        if biome in ["Swamp", "Tundra", "Desert"]: return "High"
        if biome == "Mountains": return "High"
        if biome == "Forest": return "Medium"
        return "Low"

    def _is_too_close(self, x, y, min_dist=20):
        for loc in self.locations:
            dist = ((loc['x'] - x) ** 2 + (loc['y'] - y) ** 2) ** 0.5
            if dist < min_dist:
                return True
        return False
