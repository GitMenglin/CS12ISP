import pygame
from math import *
import numpy as np
from Constants import *

class Block:
    target = None
    normalsArranged = [np.array([0, 0, -1, 0]), np.array([0, 0, 1, 0]), 
                       np.array([-1, 0, 0, 0]), np.array([1, 0, 0, 0]),
                       np.array([0, 1, 0, 0]), np.array([0, -1, 0, 0])]
    
    def __init__(self, geometry, placement=[0, 0, 0, 0], color=green):
        self.vertices = geometry[0]
        self.faces = geometry[1]
        self.color = color
        self.placement = np.array(placement)
        self.shift(self.placement)
        self.cameraSpaceVertices = None
        self.cameraSpaceCenter = None
        self.transformedFaces = None
        self.selected = False

    def preprocess(self, camera):
        self.cameraSpaceVertices = self.vertices @ camera.cameraTransformation
        clippingSpaceVertices = self.cameraSpaceVertices @ projectionMatrix
        normalizedVertices = np.array([vertex / vertex[3] if nearClippingPlane < vertex[3] < farClippingPlane else np.array([0, 0, 0, 1]) for vertex in clippingSpaceVertices])
        screenSpaceVertices = normalizedVertices @ screenTransformation
        screenSpaceVertices = [vertex if vertex[2] > 0 else None for vertex in screenSpaceVertices]
        
        blockCenter = np.array([0., 0., 0.])
        self.selected = False
        self.transformedFaces = []
        faceCount = len(self.faces)
        for i in range(faceCount):
            polygon = [self.cameraSpaceVertices[vertex] for vertex in self.faces[i]]
            a = polygon[0][:3] - polygon[1][:3]
            b = polygon[2][:3] - polygon[1][:3]
            normal = np.cross(a, b)
            faceCenter = np.array([0., 0., 0.])
            vertexCount = 0
            for vertex in polygon:
                faceCenter += vertex[:3]
                vertexCount += 1
            faceCenter /= vertexCount
            culled = np.dot(normal, faceCenter) <= 0
            distance = sqrt(sqrt(faceCenter[0]**2 + faceCenter[1]**2)**2 + faceCenter[2]**2)
            blockCenter += faceCenter
            
            if not culled:
                if len(polygon) == 4:
                    if faceCenter[2] < 5 and np.dot(polygon[0][:2], polygon[2][:2]) + np.dot(polygon[1][:2], polygon[3][:2]) < -0.3:
                        if Block.target is None:
                            Block.target = [self, i, distance]
                        elif distance < Block.target[2]:
                            Block.target = [self, i, distance]
                
                polygon = [screenSpaceVertices[vertex] for vertex in self.faces[i] if screenSpaceVertices[vertex] is not None]
                self.transformedFaces.append([polygon, distance])
            else:
                self.transformedFaces.append(None)
        
        blockCenter /= faceCount
        arrangementValue = sqrt(sqrt(blockCenter[0]**2 + blockCenter[1]**2)**2 + blockCenter[2]**2)
        self.cameraSpaceCenter = blockCenter
        return arrangementValue

    def project(self, screen):
        for i in range(len(self.transformedFaces)):
            face = self.transformedFaces[i]
            if face is not None and len(face[0]) > 2:
                adjustment = 255 * (1 / 2)**(face[1] / 100)
                if self.selected and i == Block.target[1]:
                    pygame.draw.polygon(screen, red, [vertex[:2] for vertex in face[0]])
                else:
                    pygame.draw.polygon(screen, (0, 255, 255 - adjustment), [vertex[:2] for vertex in face[0]])
                pygame.draw.polygon(screen, (0, 255 - adjustment, 255), [vertex[:2] for vertex in face[0]], 1)

    def shift(self, placement):
        self.vertices = np.array([vertex + placement for vertex in self.vertices])
