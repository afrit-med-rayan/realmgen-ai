import numpy as np
from perlin_noise import PerlinNoise
import random

class TerrainGenerator:
    def __init__(self, width: int, height: int, seed: int = None):
        self.width = width
        self.height = height
        self.seed = seed if seed is not None else random.randint(0, 999999)
        
        # We will generate elevation, moisture, and temperature
        self.noise_elev = PerlinNoise(octaves=4, seed=self.seed)
        self.noise_moist = PerlinNoise(octaves=3, seed=self.seed + 1)
        self.noise_temp = PerlinNoise(octaves=3, seed=self.seed + 2)

        self.elevation_map = np.zeros((self.height, self.width))
        self.moisture_map = np.zeros((self.height, self.width))
        self.temperature_map = np.zeros((self.height, self.width))
        self.biome_map = np.empty((self.height, self.width), dtype=object)

    def generate(self):
        # Generate the maps
        for y in range(self.height):
            for x in range(self.width):
                # Normalized coordinates
                nx = x / self.width
                ny = y / self.height
                
                self.elevation_map[y][x] = self.noise_elev([nx, ny])
                self.moisture_map[y][x] = self.noise_moist([nx, ny])
                self.temperature_map[y][x] = self.noise_temp([nx, ny])
                
        self._classify_biomes()

    def _classify_biomes(self):
        for y in range(self.height):
            for x in range(self.width):
                elev = self.elevation_map[y][x]
                moist = self.moisture_map[y][x]
                temp = self.temperature_map[y][x]
                
                self.biome_map[y][x] = self.get_biome(elev, moist, temp)

    def get_biome(self, e, m, t):
        if e < -0.15:
            return "Ocean"
        elif e > 0.35:
            return "Mountains"
        
        if t > 0.1 and m < -0.1:
            return "Desert"
        elif m > 0.2 and t > 0.0:
            return "Swamp"
        elif m > 0.05:
            return "Forest"
        elif t < -0.2:
            return "Tundra"
        else:
            return "Plains"
