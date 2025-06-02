import pygame
from math import *
import numpy as np
from MathUtil import *
from Constants import *

class Camera:
    def __init__(self, globalPosition, pitch, yaw):
        self.globalPosition = globalPosition
        self.basisVectors = np.array([
            np.array([0, 0, 1, 1]),
            np.array([0, 1, 0, 1]),
            np.array([1, 0, 0, 1])
        ])
        self.velocity = self.basisVectors
        self.pitch = pitch
        self.yaw = yaw
        self.cameraTransformation = self.getCameraTranslation() @ self.getCameraRotation()
        self.translationalSpeed = 0.08
        self.angularSpeed = 0.02
        self.wasPaused = False
        
    def control(self, paused):
        if not paused:
            keyPressed = pygame.key.get_pressed()
            if keyPressed[pygame.K_w]:
                self.globalPosition += self.velocity[0] * self.translationalSpeed
            if keyPressed[pygame.K_s]:
                self.globalPosition -= self.velocity[0] * self.translationalSpeed
            if keyPressed[pygame.K_SPACE]:
                self.globalPosition += np.array([0, 1, 0, 1]) * self.translationalSpeed
            if keyPressed[pygame.K_LSHIFT]:
                self.globalPosition -= np.array([0, 1, 0, 1]) * self.translationalSpeed
            if keyPressed[pygame.K_d]:
                self.globalPosition += self.velocity[2] * self.translationalSpeed
            if keyPressed[pygame.K_a]:
                self.globalPosition -= self.velocity[2] * self.translationalSpeed

            x, y = pygame.mouse.get_rel()
            if self.wasPaused:
                x, y = 0, 0
            if y > 0 and self.pitch > -pi / 2 or y < 0 and self.pitch < pi / 2:
                self.pitch -= y * self.angularSpeed
            self.yaw -= x * self.angularSpeed
        self.wasPaused = paused

    def updateCameraTransformation(self):
        self.basisVectors = np.array([
            np.array([0, 0, 1, 1]),
            np.array([0, 1, 0, 1]),
            np.array([1, 0, 0, 1])
        ])
        self.velocity = rotate(self.basisVectors, 0, self.yaw, 0)
        self.basisVectors = rotate(self.basisVectors, self.pitch, self.yaw, 0)
        self.cameraTransformation = self.getCameraTranslation() @ self.getCameraRotation()
    
    def getCameraTranslation(self):
        x, y, z, _ = self.globalPosition
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
            ])

    def getCameraRotation(self):
        basisZ, basisY, basisX = self.basisVectors
        return np.array([
            [basisX[0], basisY[0], basisZ[0] ,0],
            [basisX[1], basisY[1], basisZ[1] ,0],
            [basisX[2], basisY[2], basisZ[2] ,0],
            [0, 0, 0 ,1]
            ])
