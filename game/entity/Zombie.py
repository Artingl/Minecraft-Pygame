from game.entity.Entity import Entity


class Zombie(Entity):
    def __init__(self, gl):
        super().__init__(gl)

        # self.model.addCube(0, 0, 0, 0.5, 0.5, 0.5, gl.panorama)
        # self.model.addCube(-0.1, -0.9, 0.0475, 0.8, 0.9, 0.38, gl.panorama)
