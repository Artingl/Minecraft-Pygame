import math

from OpenGL.GL import *

from game.blocks.BlockEvent import *
from functions import roundPos
from settings import *


class Player:
    def __init__(self, x=0, y=0, z=0, rotation=[0, 0], gl=None):
        print("Init Player class...")

        self.position, self.rotation = [x, y, z], rotation
        self.speed = 0.03
        self.gl = gl
        self.gravity = 3.8
        self.jSpeed = (4 * self.gravity) ** .5
        self.tVel = 50
        self.dy = 0
        self.shift = 0
        self.cameraShake = [0, False]
        self.canShake = True
        self.acceleration = 0
        self.lastShiftPos = self.position
        self.cameraType = 1
        self.hp = -1
        self.bInAir = False
        self.inventory = None

        self.lastPlayerPosOnGround = []
        self.playerFallY = 0

    def setCameraShake(self):
        if not self.canShake or self.shift > 0:
            return

        if not self.cameraShake[1]:
            self.cameraShake[0] -= 0.007
            if self.cameraShake[0] < -0.1:
                self.cameraShake[1] = True
        else:
            self.cameraShake[0] += 0.007
            if self.cameraShake[0] > 0.1:
                self.cameraShake[1] = False

    def setShift(self, b):
        if b:
            if self.shift < 0.3:
                self.shift += 0.05
        else:
            if self.shift > 0:
                self.shift -= 0.05

    def updatePosition(self):
        rdx, rdy = pygame.mouse.get_pos()
        rdx, rdy = rdx - WIDTH // 2, rdy - HEIGHT // 2
        rdx /= 8
        rdy /= 8
        self.rotation[0] += rdy
        self.rotation[1] += rdx
        if self.rotation[0] > 90:
            self.rotation[0] = 90
        elif self.rotation[0] < -90:
            self.rotation[0] = -90

        DX, DY, DZ = 0, 0, 0

        rotY = self.rotation[1] / 180 * math.pi
        dx, dz = (self.speed + self.acceleration) * math.sin(rotY), \
                 (self.speed + self.acceleration) * math.cos(rotY)

        key = pygame.key.get_pressed()
        if key[pygame.K_LCTRL]:
            self.acceleration = 0.02
        if key[pygame.K_w]:
            DX += dx
            DZ -= dz
            self.setCameraShake()
        else:
            self.acceleration = 0
        if key[pygame.K_s]:
            DX -= dx
            DZ += dz
            self.setCameraShake()
            self.acceleration = 0
        if key[pygame.K_a]:
            DX -= dz
            DZ -= dx
            self.setCameraShake()
            self.acceleration = 0
        if key[pygame.K_d]:
            DX += dz
            DZ += dx
            self.setCameraShake()
            self.acceleration = 0
        if key[pygame.K_SPACE]:
            self.jump()
        if key[pygame.K_LSHIFT]:
            self.setShift(True)
            self.acceleration = -0.01
        else:
            self.setShift(False)
            if self.acceleration == -0.01:
                self.acceleration = 0

        dt = self.speed

        self.position = [self.position[0] + DX, self.position[1] + DY, self.position[2] + DZ]

        if dt < 0.2:
            dt /= 10
            DX /= 10
            DY /= 10
            DZ /= 10
            for i in range(10):
                self.move(dt, DX, DY, DZ)

        glPushMatrix()
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glTranslatef(-self.position[0],
                     -self.position[1] + self.shift + self.cameraShake[0],
                     -self.position[2])

    def jump(self):
        if not self.dy:
            self.dy = self.jSpeed * 0.9

    def move(self, dt, dx, dy, dz):
        self.dy -= dt * self.gravity
        self.dy = max(self.dy, -self.tVel)
        dy += self.dy * dt

        if self.dy > 9.8:
            self.dy = 9.8

        x, y, z = self.position
        col = self.collide((x + dx, y + dy, z + dz))
        col2 = roundPos((col[0], col[1] - 2, col[2]))
        self.canShake = self.position[1] == col[1]
        if self.position[0] != col[0] or self.position[2] != col[2]:
            if col2 in self.gl.cubes.cubes and self.shift <= 0:
                self.gl.blockSound.playStepSound(self.gl.cubes.cubes[col2].name)
        # Dynamic FOV
        # if self.position[0] != col[0] or self.position[2] != col[2]:
        #    if self.gl.fov < FOV + 20:
        #        self.gl.fov += 0.2
        #    else:
        #        self.gl.fov = FOV + 20
        # else:
        #    if self.gl.fov > FOV:
        #        self.gl.fov -= 0.2
        #    else:
        #        self.gl.fov = FOV
        #
        if not self.bInAir:
            for i in range(1, 6):
                col2 = roundPos((col[0], col[1] - i, col[2]))
                if col2 not in self.gl.cubes.cubes:
                    self.bInAir = True
                    if self.playerFallY < col2[1]:
                        self.playerFallY = round(col[1] - self.lastPlayerPosOnGround[1])
                else:
                    self.bInAir = False
                    break
        else:
            self.lastPlayerPosOnGround = col

        if self.bInAir and col2 in self.gl.cubes.cubes:
            hp = self.hp
            if 3 < self.playerFallY:
                # self.gl.sound.playSound("oof", 0.8)
                hp -= 1
                if self.playerFallY < 6:
                    hp -= 3
                elif self.playerFallY < 10:
                    hp -= 5
                elif self.playerFallY < 17:
                    hp -= 8
                elif self.playerFallY < 25:
                    hp -= 11
                else:
                    hp = 0
                self.gl.blockSound.damageByBlock(self.gl.cubes.cubes[col2].name, hp)
            self.hp = hp
            if self.hp <= 0:
                # Player dead
                self.hp = 20

            self.bInAir = False
            self.gl.particles.addParticle((col[0], col[1] - 1, col[2]),
                                          self.gl.cubes.cubes[col2],
                                          direction="down",
                                          count=10)
        self.position = col

    def mouseEvent(self, button):
        blockByVec = self.gl.cubes.hitTest(self.position, self.get_sight_vector())

        if button == 1 and blockByVec[0]:
            if blockByVec[0] in self.gl.cubes.cubes:
                if self.inventory.inventory[self.inventory.activeInventory][0] == \
                        self.gl.cubes.cubes[blockByVec[0]].name:
                    self.inventory.inventory[self.inventory.activeInventory][1] += 1
                elif self.inventory.inventory[self.inventory.activeInventory][1] == 0:
                    self.inventory.inventory[self.inventory.activeInventory][1] += 1
                    self.inventory.inventory[self.inventory.activeInventory][0] = \
                        self.gl.cubes.cubes[blockByVec[0]].name
            self.gl.blockSound.playBlockSound(self.gl.cubes.cubes[blockByVec[0]].name)
            self.gl.particles.addParticle(self.gl.cubes.cubes[blockByVec[0]].p, self.gl.cubes.cubes[blockByVec[0]],
                                          direction="down")
            self.gl.cubes.remove(blockByVec[0])
        if button == 2 and blockByVec[0]:
            self.inventory.inventory[self.inventory.activeInventory] = [self.gl.cubes.cubes[blockByVec[0]].name, 64]
            self.gl.gui.showText(self.inventory.inventory[self.inventory.activeInventory][0])
        if button == 3:
            if blockByVec[0] and self.shift <= 0:
                if blockByVec[0] in self.gl.cubes.cubes:
                    if canOpenBlock(self, self.gl.cubes.cubes[blockByVec[0]], self.gl):
                        openBlockInventory(self, self.gl.cubes.cubes[blockByVec[0]], self.gl)
                        return
            if blockByVec[1] and self.shift <= 0:
                if blockByVec[1] in self.gl.cubes.cubes:
                    if canOpenBlock(self, self.gl.cubes.cubes[blockByVec[1]], self.gl):
                        openBlockInventory(self, self.gl.cubes.cubes[blockByVec[1]], self.gl)
                        return
            if blockByVec[1]:
                playerPos = tuple(roundPos((self.position[0], self.position[1] - 1, self.position[2])))
                playerPos2 = tuple(roundPos((self.position[0], self.position[1], self.position[2])))
                blockByVec = blockByVec[1][0], blockByVec[1][1], blockByVec[1][2]
                if self.inventory.inventory[self.inventory.activeInventory][0] and \
                        self.inventory.inventory[self.inventory.activeInventory][1] and blockByVec != playerPos and \
                        blockByVec != playerPos2:
                    self.gl.cubes.add(blockByVec, self.inventory.inventory[self.inventory.activeInventory][0], now=True)
                    self.gl.blockSound.playBlockSound(self.gl.cubes.cubes[blockByVec].name)
                    self.inventory.inventory[self.inventory.activeInventory][1] -= 1

    def collide(self, pos):
        if pos[1] < -80:
            self.dy = 0
            return self.gl.startPlayerPos

        p = list(pos)
        np = roundPos(pos)
        for face in ((-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)):
            for i in (0, 1, 2):
                if not face[i]:
                    continue
                d = (p[i] - np[i]) * face[i]
                pad = 0 if i == 1 and face[i] < 0 else 0.25
                if d < pad:
                    continue
                for dy in (0, 1):
                    op = list(np)
                    op[1] -= dy
                    op[i] += face[i]
                    if tuple(op) in self.gl.cubes.collidable:
                        p[i] -= (d - pad) * face[i]
                        if face[1]:
                            self.dy = 0
                        break
        return tuple(p)

    def get_sight_vector(self):
        rotX, rotY = -self.rotation[0] / 180 * math.pi, self.rotation[1] / 180 * math.pi
        dx, dz = math.sin(rotY), -math.cos(rotY)
        dy, m = math.sin(rotX), math.cos(rotX)
        return dx * m, dy, dz * m

    def x(self):
        return self.position[0]

    def y(self):
        return self.position[1]

    def z(self):
        return self.position[2]

    def update(self):
        self.updatePosition()
