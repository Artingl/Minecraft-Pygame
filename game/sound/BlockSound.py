from random import randint


class BlockSound:
    def __init__(self, gl):
        self.gl = gl
        self.cntr = 0

    def getBlockSound(self, blockName):
        blName = "grass"

        if blockName == "grass" or blockName == "tnt" or blockName.startswith("leaves"):
            blName = "grass"
        if blockName == "stone" or blockName == "bedrock" or blockName == "brick" or blockName.endswith("ore"):
            blName = "stone"
        if blockName == "dirt" or blockName == "gravel":
            blName = "gravel"
        if blockName == "sand":
            blName = "sand"
        if blockName.startswith("log"):
            blName = "wood"
        if blockName.endswith("wool"):
            blName = "cloth"

        return blName

    def damageByBlock(self, blockName, hp):
        sound = self.gl.sound.SOUNDS["damage"]["fallbig"][0]

        if blockName.endswith("wool"):
            sound = self.gl.sound.SOUNDS["damage"]["fallsmall"][0]
        if hp > 0:
            bl = len(self.gl.sound.SOUNDS["damage"]["hit"])
            sound = self.gl.sound.SOUNDS["damage"]["hit"][randint(0, bl - 1)]

        chnl = sound.play()
        chnl.set_volume(0.6)

    def playStepSound(self, blockName):
        self.cntr += 1
        if self.cntr % 300 != 0:
            return
        blName = self.getBlockSound(blockName)

        bl = len(self.gl.sound.BLOCKS_SOUND["step"][blName])
        chnl = self.gl.sound.BLOCKS_SOUND["step"][blName][randint(0, bl - 1)].play()
        chnl.set_volume(0.3)

    def playBoomSound(self):
        bl = len(self.gl.sound.BLOCKS_SOUND["explode"])
        chnl = self.gl.sound.BLOCKS_SOUND["explode"][randint(0, bl - 1)].play()
        chnl.set_volume(0.3)

    def playBlockSound(self, blockName):
        blName = self.getBlockSound(blockName)

        bl = len(self.gl.sound.BLOCKS_SOUND["dig"][blName])
        chnl = self.gl.sound.BLOCKS_SOUND["dig"][blName][randint(0, bl - 1)].play()
        chnl.set_volume(0.3)
