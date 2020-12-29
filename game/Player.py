import math

import pygame
from OpenGL.GL import *

from blocks.Inventory import Inventory
from blocks.blockInventory import *
from functions import roundPos
from settings import *


class Player:
    def __init__(self, x=0, y=0, z=0, rotation=[0, 0], gl=None):
        self.position, self.rotation = [x, y, z], rotation
        self.speed = 0.02
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

        self.inventory = Inventory(gl)

    def setCameraShake(self):
        if not self.canShake or self.shift != 0:
            return

        if not self.cameraShake[1]:
            self.cameraShake[0] -= 0.007
            if self.cameraShake[0] < -0.1:
                self.cameraShake[1] = True
        else:
            self.cameraShake[0] += 0.007
            if self.cameraShake[0] > 0.1:
                self.cameraShake[1] = False

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
        dx, dz = (self.speed + self.acceleration) * math.sin(rotY),\
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
            self.shift = 0.3
            self.acceleration = -0.01
        else:
            self.shift = 0
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
        self.canShake = self.position[1] == col[1]
        if self.shift != 0:
            col2 = roundPos((col[0], col[1] - 2, col[2]))
            if col2 not in self.gl.cubes.cubes:
                self.position = (self.lastShiftPos[0], col[1], self.lastShiftPos[2])
                return
        self.lastShiftPos = self.position
        self.position = col

    def mouseEvent(self, button):
        blockByVec = self.gl.cubes.hitTest(self.position, self.get_sight_vector())

        if button == 1 and blockByVec[0]:
            self.gl.cubes.remove(blockByVec[0])
        if button == 2 and blockByVec[0]:
            self.inventory.inventory[self.inventory.activeInventory] = [self.gl.cubes.cubes[blockByVec[0]].name, 64]
        if button == 3:
            if blockByVec[0]:
                if blockByVec[0] in self.gl.cubes.cubes:
                    if canOpenBlock(self.gl.cubes.cubes[blockByVec[0]]):
                        openBlockInventory(self, self.gl.cubes.cubes[blockByVec[0]])
                        return
            if blockByVec[1]:
                blockByVec = blockByVec[1][0], blockByVec[1][1], blockByVec[1][2]
                if self.inventory.inventory[self.inventory.activeInventory][0] and \
                        self.inventory.inventory[self.inventory.activeInventory][1]:
                    self.gl.cubes.add(blockByVec, self.inventory.inventory[self.inventory.activeInventory][0], now=True)
                    self.inventory.inventory[self.inventory.activeInventory][1] -= 1

    def collide(self, pos):
        if pos[1] < -80:
            self.dy = 0
            return 0, 60, 0

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
