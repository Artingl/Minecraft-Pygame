class Cube:
    def __init__(self, name, p, t, typ):
        self.name, self.p, self.t, self.type = name, p, t, typ
        self.shown = {'left': False, 'right': False, 'bottom': False, 'top': False, 'back': False, 'front': False}
        self.faces = {'left': None, 'right': None, 'bottom': None, 'top': None, 'back': None, 'front': None}
