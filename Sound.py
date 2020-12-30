from random import randint


class Sound:
    def __init__(self):
        print("Init Sound class...")
        self.SOUNDS = {}
        self.MUSIC = []
        self.music_already_playing = False
        self.channel = None

    def playSound(self, name, volume):
        channel = self.SOUNDS[name].play()
        channel.set_volume(volume)

    def playMusic(self):
        if self.music_already_playing:
            return
        self.music_already_playing = True
        self.channel = self.MUSIC[randint(0, len(self.MUSIC) - 1)].play()
        self.channel.set_volume(0.1)
