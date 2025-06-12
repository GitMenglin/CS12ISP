import pygame
import numpy as np
from MathUtil import *
from Camera import Camera
from GeometryLib import Geometry
from Constants import *

class Player:
    def __init__(self, globalPosition=[worldSize // 2 + 0.5, 0., worldSize // 2 + 0.5, 1.], pitch=0, yaw=0, geometry=Geometry.camera):
        self.globalPosition = np.array(globalPosition)
        self.camera = Camera(self.globalPosition, pitch, yaw)
        self.vertices = geometry[0]
        self.faces = geometry[1]
        self.name = ""
        self.font = pygame.font.SysFont("Arial", 20)
        self.velocityY = -0.01
        self.landed = False
        self.jumpCoolDownStart = 0

    def update(self, paused):
        self.camera.control(paused)
        self.globalPosition = self.camera.globalPosition
        self.camera.update()
        
        if not paused:
            if pygame.key.get_pressed()[pygame.K_SPACE] and self.landed and pygame.time.get_ticks() - self.jumpCoolDownStart > 600:
                self.velocityY = 0.125
                self.jumpCoolDownStart = pygame.time.get_ticks()
            self.camera.globalPosition += np.array([0, 1, 0, 1]) * self.velocityY
            self.velocityY -= 0.01

    def checkCollisionHorizontal(self, block):
        x, y, z = block.center[:3] - self.camera.globalPosition[:3]
        
        if -1.75 <= y <= 0.75:
            if abs(x) <= 0.5:
                if 0 < z <= 0.7:
                    for basis in self.camera.basisVelocities:
                        if basis[2] > 0:
                            basis[2] = 0
                    self.landed = True
                elif -0.7 <= z < 0:
                    for basis in self.camera.basisVelocities:
                        if basis[2] < 0:
                            basis[2] = 0
                    self.landed = True
            if abs(z) <= 0.5:
                if 0 < x <= 0.7:
                    for basis in self.camera.basisVelocities:
                        if basis[0] > 0:
                            basis[0] = 0
                    self.landed = True
                elif -0.7 <= x < 0:
                    for basis in self.camera.basisVelocities:
                        if basis[0] < 0:
                            basis[0] = 0
                    self.landed = True

    def checkCollisionVertical(self, block):
        x, y, z = block.center[:3] - self.camera.globalPosition[:3]
        
        landing = -2 <= y <= 0
        if not self.landed and landing:
            self.velocityY = 0
        if self.landed and not landing:
            self.velocityY = -0.01
        self.landed = landing
        
        if self.landed and abs(x) < 0.5 and abs(z) < 0.5:
            self.camera.globalPosition[1] += y + 2

    def getArrangementValue(self, camera):
        cameraSpacePosition = self.globalPosition @ camera.cameraTransformation
        return np.linalg.norm(cameraSpacePosition[:3])

    def project(self, camera, screen):
        globalSpaceVertices = np.array([translate(vertex, *self.globalPosition[:3]) for vertex in rotate(self.vertices, self.camera.pitch, self.camera.yaw, 0)])
        cameraSpaceVertices = globalSpaceVertices @ camera.cameraTransformation
        clippingSpaceVertices = cameraSpaceVertices @ projectionMatrix
        normalizedVertices = np.array([vertex / vertex[3] if nearClippingPlane < vertex[3] < farClippingPlane else np.array([0, 0, 0, 1]) for vertex in clippingSpaceVertices])
        screenSpaceVertices = normalizedVertices @ screenTransformation
        screenSpaceVertices = [vertex if vertex[2] > 0 else None for vertex in screenSpaceVertices]
        
        for face in self.faces:
            polygon = [cameraSpaceVertices[vertex] for vertex in face]
            a = polygon[0][:3] - polygon[1][:3]
            b = polygon[2][:3] - polygon[1][:3]
            normal = np.cross(a, b)
            center = np.array([0., 0., 0.])
            vertexCount = 0
            for vertex in polygon:
                center += vertex[:3]
                vertexCount += 1
            center /= vertexCount
            dotProduct = np.dot(normal, center)
            if dotProduct > 0:
                polygon = [screenSpaceVertices[vertex] for vertex in face if screenSpaceVertices[vertex] is not None]
                distance = np.linalg.norm(center[:3])
                if len(polygon) > 2:
                    adjustment = 255 * (1 / 2)**(distance / 100)
                    pygame.draw.polygon(screen, (adjustment, 255, 255 - adjustment), [vertex[:2] for vertex in polygon])
                    pygame.draw.polygon(screen, (0, 255 - adjustment, 255), [vertex[:2] for vertex in polygon], 1)
        if screenSpaceVertices[0] is not None and cameraSpaceVertices[0][2] < 10 and 0 <= screenSpaceVertices[0][0] <= WIDTH and 0 <= screenSpaceVertices[0][1] <= HEIGHT:
            screen.blit(self.font.render(self.name, True, black, white), [screenSpaceVertices[0][0] - 5 * len(self.name), screenSpaceVertices[0][1] - 10])
