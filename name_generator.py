import random

class NameGenerator:
    def __init__(self, seed: int):
        self.rng = random.Random(seed)
        
        self.prefixes = ["Val", "Ash", "Frost", "Drak", "Eld", "Glim", "Gond", "Mor", "Sil", "Thal", "Riv", "Ock", "Dun", "Iron", "Gold", "Silver", "Shadow", "Light"]
        self.suffixes = ["enor", "mere", "veil", "moor", "oria", "wood", "dor", "garth", "ton", "burg", "fort", "keep", "peak", "run", "deep", "ford", "haven"]
        
        self.kingdom_titles = ["Kingdom of", "Empire of", "The Dominion of", "Realm of"]
        self.ruin_titles = ["Ruins of", "Fallen", "Ancient", "Lost"]
        self.dungeon_titles = ["Dungeons of", "Crypt of", "Lair of", "Depths of", "Caves of"]
        
    def generate_base_name(self) -> str:
        prefix = self.rng.choice(self.prefixes)
        suffix = self.rng.choice(self.suffixes)
        return prefix + suffix

    def generate_name(self, location_type: str) -> str:
        base_name = self.generate_base_name()
        
        if location_type == "Kingdom":
            if self.rng.random() > 0.5:
                return f"{self.rng.choice(self.kingdom_titles)} {base_name}"
            return base_name
        elif location_type == "Ruin":
            if self.rng.random() > 0.5:
                return f"{self.rng.choice(self.ruin_titles)} {base_name}"
            return f"{base_name} Ruins"
        elif location_type == "Dungeon":
            if self.rng.random() > 0.5:
                return f"{self.rng.choice(self.dungeon_titles)} {base_name}"
            return f"{base_name} Dungeon"
        elif location_type == "Village":
            return base_name
        elif location_type == "Castle":
            return f"{base_name} Castle"
        
        return base_name
