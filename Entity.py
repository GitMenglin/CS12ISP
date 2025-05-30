import pygame
from math import *
import numpy as np
from Constants import *

class Block:
    target = None
    
    def __init__(self, geometry, shift=[0, 0, 0], color=green):
        self.vertices = geometry[0]
        self.faces = geometry[1]
        self.color = color
        self.shift(*shift)
        self.cameraSpaceVertices = None
        self.selected = False

    def getArrangementValue(self, camera):
        cameraTransformation = camera.cameraTransformation
        self.cameraSpaceVertices = self.vertices @ cameraTransformation
        center = np.array([0., 0., 0.])
        vertexCount = 0
        for vertex in self.cameraSpaceVertices:
            center += vertex[:3]
            vertexCount += 1
        center /= vertexCount
        arrangementValue = sqrt(sqrt(center[0]**2 + center[1]**2)**2 + center[2]**2)
        
        if center[2] < 5 and -0.5 < center[0] < 0.5 and -0.5 < center[1] < 0.5:
            if Block.target is None:
                Block.target = [self, arrangementValue]
            elif Block.target[1] > arrangementValue:
                Block.target = [self, arrangementValue]
        
        return arrangementValue

    def project(self, screen):
        clippingSpaceVertices = self.cameraSpaceVertices @ projectionMatrix
        normalizedVertices = np.array([vertex / vertex[3] if nearClippingPlane < vertex[3] < farClippingPlane else np.array([0, 0, 0, 1]) for vertex in clippingSpaceVertices])
        screenSpaceVertices = normalizedVertices @ screenTransformation
        screenSpaceVertices = [vertex if vertex[2] > 0 else None for vertex in screenSpaceVertices]
        
        for face in self.faces:
            polygon = [self.cameraSpaceVertices[vertex] for vertex in face]
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
                    if self.selected:
                        pygame.draw.polygon(screen, red, [vertex[:2] for vertex in polygon])
                    else:
                        pygame.draw.polygon(screen, (0, 255, 255 - adjustment), [vertex[:2] for vertex in polygon])
                    pygame.draw.polygon(screen, (0, 255 - adjustment, 255), [vertex[:2] for vertex in polygon], 1)
        self.selected = False

    def shift(self, sX, sY, sZ):
        self.vertices = np.array([vertex + np.array([sX, sY, sZ, 0]) for vertex in self.vertices])
