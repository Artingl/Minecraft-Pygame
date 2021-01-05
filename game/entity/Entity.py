from OpenGL.GL import *

from game.models.Model import Model


class Entity:
    def __init__(self, gl):
        self.position = [0, 0, 0]
        self.rotation = [0, 0, 0]
        self.gl = gl

        self.model = Model(gl)

    def update(self):
        self.model.drawModel(self.position, self.rotation)
