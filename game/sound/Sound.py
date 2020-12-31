from random import randint

import pygame


class Sound:
    def __init__(self):
        print("Init Sound class...")
        self.BLOCKS_SOUND = {}
        self.SOUNDS = {}
        self.MUSIC = []
        self.music_already_playing = False

    def initMusic(self):
        musicNum = randint(0, len(self.MUSIC) - 1)
        pygame.mixer.music.load(self.MUSIC[musicNum])
        for i in range(len(self.MUSIC)):
            if i == musicNum:
                continue
            pygame.mixer.music.queue(self.MUSIC[i])

    def playSound(self, name, volume):
        channel = self.SOUNDS[name].play()
        channel.set_volume(volume)

    def playMusic(self):
        if self.music_already_playing:
            return
        if randint(0, 5000) == 746:
            self.music_already_playing = True
            pygame.mixer.music.play(0, 0.1)
            pygame.mixer.music.set_volume(0.1)
