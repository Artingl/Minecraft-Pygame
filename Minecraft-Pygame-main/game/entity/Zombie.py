from game.entity.Entity import Entity


class Zombie(Entity):
    def __init__(self, gl):
        super().__init__(gl)

        # self.model.addCube(0, 0, 0, 0.5, 0.5, 0.5, gl.panorama)
