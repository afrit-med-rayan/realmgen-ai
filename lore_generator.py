import random

class LoreGenerator:
    def __init__(self, seed: int):
        self.rng = random.Random(seed)

    def generate_lore(self, location_type, biome, danger_level):
        ruler = self._generate_ruler(location_type)
        population = self._generate_population(location_type, biome)
        history = self._generate_history(location_type, biome)
        threats = self._generate_threats(danger_level)
        
        return {
            "ruler": ruler,
            "population": population,
            "history": history,
            "threats": threats,
            "description": f"{history} Currently ruled by {ruler}, it faces threats from {threats}."
        }
        
    def _generate_ruler(self, loc_type):
        if loc_type == "Kingdom":
            titles = ["King", "Queen", "Emperor", "Empress", "High Lord"]
            return f"{self.rng.choice(titles)} of the Realm"
        elif loc_type == "Village":
            return "Elder Council"
        elif loc_type == "Castle":
            return f"{self.rng.choice(['Duke', 'Baron', 'Count', 'Lord Commander'])}"
        elif loc_type in ["Dungeon", "Ruin"]:
            return "None (Abandoned)"
        return "Unknown"
        
    def _generate_population(self, loc_type, biome):
        if loc_type == "Kingdom":
            return f"{self.rng.randint(10000, 50000)} souls"
        elif loc_type == "Village":
            return f"{self.rng.randint(50, 500)} villagers"
        elif loc_type == "Castle":
            return f"{self.rng.randint(200, 1000)} soldiers and servants"
        elif loc_type in ["Dungeon", "Ruin"]:
            return "Unknown entities"
        return "Unknown"
        
    def _generate_history(self, loc_type, biome):
        if loc_type == "Kingdom":
            return f"Founded centuries ago in the {biome}, this kingdom has stood the test of time."
        elif loc_type == "Village":
            return f"A quiet settlement established by pioneers seeking refuge in the {biome}."
        elif loc_type == "Castle":
            return f"Built as a stronghold to protect the borders of the {biome}."
        elif loc_type == "Dungeon":
            return f"A dark, labyrinthine structure beneath the {biome}, holding ancient secrets."
        elif loc_type == "Ruin":
            return f"The remnants of a forgotten civilization that once thrived in the {biome}."
        return "A place shrouded in mystery."
        
    def _generate_threats(self, danger_level):
        if danger_level == "Low":
            return self.rng.choice(["petty thieves", "wild animals", "mild weather anomalies"])
        elif danger_level == "Medium":
            return self.rng.choice(["bandit raids", "dangerous beasts", "local uprisings"])
        elif danger_level == "High":
            return self.rng.choice(["orc warbands", "undead hordes", "severe magical storms"])
        elif danger_level == "Extreme":
            return self.rng.choice(["ancient dragons", "demonic incursions", "cataclysms"])
        return "Unknown dangers"
