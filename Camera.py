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
        self.pitch = pitch
        self.yaw = yaw
        self.cameraTransformation = self.getCameraTranslation() @ self.getCameraRotation()
        self.translationalSpeed = 0.08
        self.angularSpeed = 0.02
        
        self.horizontalFieldOfView = pi / 2
        self.verticalFieldOfView = self.horizontalFieldOfView * (HEIGHT / WIDTH)
        self.nearClippingPlane = 0.1
        self.farClippingPlane = 100
        self.projectionMatrix = self.getProjectionMatrix()
        
    def control(self):
        keyPressed = pygame.key.get_pressed()
        if keyPressed[pygame.K_w]:
            self.globalPosition += self.basisVectors[0] * self.translationalSpeed
        if keyPressed[pygame.K_s]:
            self.globalPosition -= self.basisVectors[0] * self.translationalSpeed
        if keyPressed[pygame.K_SPACE]:
            self.globalPosition += self.basisVectors[1] * self.translationalSpeed
        if keyPressed[pygame.K_LSHIFT]:
            self.globalPosition -= self.basisVectors[1] * self.translationalSpeed
        if keyPressed[pygame.K_d]:
            self.globalPosition += self.basisVectors[2] * self.translationalSpeed
        if keyPressed[pygame.K_a]:
            self.globalPosition -= self.basisVectors[2] * self.translationalSpeed

        if keyPressed[pygame.K_UP]:
            self.pitch += self.angularSpeed
        if keyPressed[pygame.K_DOWN]:
            self.pitch -= self.angularSpeed
        if keyPressed[pygame.K_LEFT]:
            self.yaw += self.angularSpeed
        if keyPressed[pygame.K_RIGHT]:
            self.yaw -= self.angularSpeed

    def updateCameraTransformation(self):
        self.basisVectors = np.array([
            np.array([0, 0, 1, 1]),
            np.array([0, 1, 0, 1]),
            np.array([1, 0, 0, 1])
        ])
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

    def getProjectionMatrix(self):
        near = self.nearClippingPlane
        far = self.farClippingPlane
        right = tan(self.horizontalFieldOfView / 2)
        left = -right
        top = tan(self.verticalFieldOfView / 2)
        bottom = -top
        return np.array([
            [2 / (right - left), 0, 0, 0],
            [0, 2 / (top - bottom), 0, 0],
            [0, 0, (far + near) / (far - near), 1],
            [0, 0, -2 * far * near / (far - near), 0]
            ])
