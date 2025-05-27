import pygame
from math import *
import numpy as np
from Constants import *

class Block:
    def __init__(self, geometry, shift=[0, 0, 0], color=Color.green):
        self.vertices = geometry[0]
        self.faces = geometry[1]
        self.color = color
        self.shift(*shift)
        
    def project(self, camera, screenTransformation, screen):
        cameraTransformation = camera.cameraTransformation
        projectionMatrix = camera.projectionMatrix
        cameraSpaceVertices = self.vertices @ cameraTransformation
        clippingSpaceVertices = cameraSpaceVertices @ projectionMatrix
        normalizedVertices = np.array([vertex / vertex[3] if camera.nearClippingPlane < vertex[3] < camera.farClippingPlane else np.array([0, 0, 0, 1]) for vertex in clippingSpaceVertices])
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
                    pygame.draw.polygon(screen, (0, 255, 255 - adjustment), [vertex[:2] for vertex in polygon])
                    pygame.draw.polygon(screen, (0, 255 - adjustment, 255), [vertex[:2] for vertex in polygon], 1)

    def shift(self, sX, sY, sZ):
        self.vertices = np.array([vertex + np.array([sX, sY, sZ, 0]) for vertex in self.vertices])

    def getTransformedCenter(self, camera):
        cameraTransformation = camera.cameraTransformation
        cameraSpaceVertices = self.vertices @ cameraTransformation
        center = np.array([0., 0., 0.])
        vertexCount = 0
        for vertex in cameraSpaceVertices:
            center += vertex[:3]
            vertexCount += 1
        return center / vertexCount
