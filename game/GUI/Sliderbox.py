from functions import *
from settings import *


class Sliderbox:
    def __init__(self, gl, text, maxval, x, y):
        self.text = text
        self.maxval = maxval
        self.x = x
        self.y = y
        self.gl = gl
        self.event = None
        self.val = 100
        self.lastButtonClicked = False

        self.bg = gl.gui.GUI_TEXTURES["edit_bg"]
        self.slider = gl.gui.GUI_TEXTURES["slider"]

    def update(self, mp):
        pos = ((self.bg.width - self.slider.width) / self.maxval) * self.val
        self.slider.x = self.x + pos

        if checkHover(self.x, self.y,
                      self.bg.width, self.bg.height,
                      mp[0], mp[1]):
            if pygame.mouse.get_pressed(3)[0]:
                self.val = round((mp[0] - self.x) * self.maxval / self.bg.width)
                pos = mp[0]
                if pos > self.x + self.bg.width - self.slider.width:
                    pos = self.x + self.bg.width - self.slider.width
                self.slider.x = pos
                self.lastButtonClicked = True
            elif self.lastButtonClicked:
                self.gl.sound.playGuiSound("click")
                self.lastButtonClicked = False

        self.bg.blit(self.x, self.gl.HEIGHT - self.y - self.bg.height)
        self.slider.blit(self.slider.x, self.gl.HEIGHT - self.y - self.bg.height)
        drawInfoLabel(self.gl, self.text, xx=self.x, yy=self.gl.HEIGHT - self.y + 15, style=[('', '')],
                      size=12)
