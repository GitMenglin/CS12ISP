import pygame
import numpy as np
from MathUtil import *
from Camera import Camera
from GeometryLib import Geometry
from Constants import *

class Player:
    def __init__(self, globalPosition=[1., 3., 1., 1.], pitch=0, yaw=-pi / 6, geometry=Geometry.camera):
        self.globalPosition = np.array(globalPosition)
        self.camera = Camera(self.globalPosition, pitch, yaw)
        self.vertices = geometry[0]
        self.faces = geometry[1]
        self.name = ""
        self.font = pygame.font.SysFont("Arial", 20)
        self.collided = False
        self.velocityY = 0.08

    def update(self, paused):
        self.camera.control(paused)
        self.globalPosition = self.camera.globalPosition
        self.camera.updateCameraTransformation()
        # if not paused and not self.collided:
        #     self.camera.globalPosition -= np.array([0, 1, 0, 1]) * self.velocityY
        
    def checkCollision(self, block):
        x, y, z = block.cameraSpaceCenter
        if y >= -2:
            self.collided = True

    def getArrangementValue(self, camera):
        cameraTransformation = camera.cameraTransformation
        cameraSpacePosition = self.globalPosition @ cameraTransformation
        return sqrt(sqrt(cameraSpacePosition[0]**2 + cameraSpacePosition[1]**2)**2 + cameraSpacePosition[2]**2)

    def project(self, camera, screen):
        cameraTransformation = camera.cameraTransformation
        globalSpaceVertices = np.array([vertex + np.array([*self.globalPosition[:3], 0.]) for vertex in rotate(self.vertices, self.camera.pitch, self.camera.yaw, 0)])
        cameraSpaceVertices = globalSpaceVertices @ cameraTransformation
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
                distance = sqrt(sqrt(center[0]**2 + center[1]**2)**2 + center[2]**2)
                if len(polygon) > 2:
                    adjustment = 255 * (1 / 2)**(distance / 100)
                    pygame.draw.polygon(screen, (adjustment, 255, 255 - adjustment), [vertex[:2] for vertex in polygon])
                    pygame.draw.polygon(screen, (0, 255 - adjustment, 255), [vertex[:2] for vertex in polygon], 1)
        if screenSpaceVertices[0] is not None and cameraSpaceVertices[0][2] < 10 and 0 <= screenSpaceVertices[0][0] <= WIDTH and 0 <= screenSpaceVertices[0][1] <= HEIGHT:
            screen.blit(self.font.render(self.name, True, black, white), [screenSpaceVertices[0][0] - 5 * len(self.name), screenSpaceVertices[0][1] - 10])
