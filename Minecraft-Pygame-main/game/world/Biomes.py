all_biomes = ["forest", "desert", "ocean", "taiga", "mountains", "big_mountains"]


def getBiomeByTemp(temp):
    if 30 > temp > 5:
        return all_biomes[0]  # Forest
    if temp > 30:
        return all_biomes[1]  # Desert
    if 5 > temp > -5:
        return all_biomes[4]  # mountains
    if 3 > temp > -3:
        return all_biomes[5]  # mountains

    return all_biomes[3]  # Taiga


class Biomes:
    def __init__(self, biome):
        self.biome = biome

    def getBiomeGrass(self):
        if self.biome == "desert":
            return "sand"
        if self.biome == "ocean":
            return "dirt"
        if self.biome == "forest" or self.biome == "taiga" or self.biome == "mountains":
            return "grass"
        if self.biome == "big_mountains":
            return "stone"

    def getBiomePlant(self):
        if self.biome == "desert":
            return "cactus"
        if self.biome == "forest" or self.biome == "taiga" or self.biome == "mountains":
            return "tree"

        return ""

    def getBiomeDirt(self):
        if self.biome == "desert":
            return "sand"
        if self.biome == "forest" or self.biome == "taiga" or self.biome == "mountains" \
                or self.biome == "big_mountains":
            return "dirt"
        if self.biome == "ocean":
            return "water"

    def getBiomeStone(self):
        if self.biome == "desert":
            return "sandstone"
        if self.biome == "forest" or self.biome == "taiga" or self.biome == "mountains":
            return "stone"
        if self.biome == "ocean":
            return "water"
        if self.biome == "big_mountains":
            return "stone"
