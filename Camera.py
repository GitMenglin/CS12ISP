import pygame
from math import *
import numpy as np
from MathUtil import *
from Constants import *

class Camera:
    def __init__(self, globalPosition, pitch, yaw):
        self.globalPosition = globalPosition
        self.basisVectors = cameraBasisVectors
        self.basisVelocities = cameraBasisVectors
        self.pitch = pitch
        self.yaw = yaw
        self.cameraTransformation = self.getCameraTranslation() @ self.getCameraOrientation()
        self.translationalSpeed = 0.08
        self.angularSpeed = 0.02
        self.wasPaused = False
        
    def control(self, paused):
        if not paused:
            self.globalPosition += self.basisVelocities[0] * self.translationalSpeed
            self.globalPosition += self.basisVelocities[2] * self.translationalSpeed

            x, y = pygame.mouse.get_rel()
            if self.wasPaused:
                x, y = 0, 0
            if y > 0 and self.pitch > -pi / 2 or y < 0 and self.pitch < pi / 2:
                self.pitch -= y * self.angularSpeed
            self.yaw -= x * self.angularSpeed
        self.wasPaused = paused

    def update(self):
        self.basisVelocities = rotate(cameraBasisVectors, 0, self.yaw, 0)
        self.basisVectors = rotate(cameraBasisVectors, self.pitch, self.yaw, 0)
        self.cameraTransformation = self.getCameraTranslation() @ self.getCameraOrientation()
        
        keyPressed = pygame.key.get_pressed()
        if keyPressed[pygame.K_s]:
            self.basisVelocities[0] *= -1
        elif not keyPressed[pygame.K_w]:
            self.basisVelocities[0] *= 0
        if keyPressed[pygame.K_a]:
            self.basisVelocities[2] *= -1
        elif not keyPressed[pygame.K_d]:
            self.basisVelocities[2] *= 0

    def getCameraTranslation(self):
        x, y, z, _ = self.globalPosition
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x, -(y + 0.15), -z, 1]
            ])

    def getCameraOrientation(self):
        basisZ, basisY, basisX = self.basisVectors
        return np.array([
            [basisX[0], basisY[0], basisZ[0] ,0],
            [basisX[1], basisY[1], basisZ[1] ,0],
            [basisX[2], basisY[2], basisZ[2] ,0],
            [0, 0, 0 ,1]
            ])
