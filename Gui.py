class Gui:
    def __init__(self):
        self.GUI_TEXTURES = {}
        self.shows = {}

    def update(self):
        for i in self.shows.values():
            i[0].blit(*i[1])

    def addGuiElement(self, image, pos):
        self.shows[image] = [self.GUI_TEXTURES[image], pos]
