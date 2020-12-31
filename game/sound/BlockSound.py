from random import randint


class BlockSound:
    def __init__(self, gl):
        self.gl = gl

    def playBoomSound(self):
        self.gl.sound.SOUNDS["boom"].play()

    def playBlockSound(self, blockName):
        blName = "stone"

        if blockName == "grass" or blockName == "tnt" or blockName.startswith("leaves"):
            blName = "grass"
        if blockName == "stone" or blockName == "bedrock":
            blName = "stone"
        if blockName == "dirt" or blockName == "gravel":
            blName = "gravel"
        if blockName == "sand":
            blName = "sand"
        if blockName.startswith("log"):
            blName = "wood"

        bl = len(self.gl.sound.BLOCKS_SOUND["dig"][blName])
        chnl = self.gl.sound.BLOCKS_SOUND["dig"][blName][randint(0, bl - 1)].play()
        chnl.set_volume(0.3)
