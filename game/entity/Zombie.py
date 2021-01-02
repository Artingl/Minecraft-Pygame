from game.entity.Entity import Entity


class Zombie(Entity):
    def __init__(self):
        super().__init__()

        self.vertices = [
            (0, 0, 0),
            (1, 0, 0),
            (1, 0, 1),
            (1, 1, 1),
            (1, 1, 0),
            (0, 1, 0),
            (0, 1, 1),
            (0, 0, 1),
            (0, 0, 0),
            (0, 1, 0),

        ]
