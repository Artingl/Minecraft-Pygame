import os
import pyglet


class OBJLoader:
    def __int__(self):
        self.models = {}

    def loadModels(self):
        print("Loading OBJ models...")
        # for i in os.listdir("models/"):
        #    print(pyglet.resource.model("models/" + i))
        #    self.models[i.split(".")[0]] = obj_reader.get_mesh("Monkey")
