import pygame
from math import *
import numpy as np
from GeometryLib import Geometry
from MathUtil import *
from Constants import *

# AI recommended Object Pooling for block creation management and reduced garbage collection pressure
class BlockPool:
    pool = []
    
    def acquire(geometry, placement):
        if BlockPool.pool:
            block = BlockPool.pool.pop()
            block.__init__(geometry, placement)
            return block
        return Block(geometry, placement)
    
    def release(block):
        BlockPool.pool.append(block)

class Block:
    target = None
    normalsArranged = [np.array([0, 0, -1]), np.array([0, 0, 1]), 
                       np.array([-1, 0, 0]), np.array([1, 0, 0]),
                       np.array([0, 1, 0]), np.array([0, -1, 0])]
    
    def __init__(self, geometry, placement=[0, 0, 0]):
        self.vertices = geometry[0]
        self.faces = geometry[1]
        self.colors = geometry[2]
        self.placement = np.array([*placement, 1])
        self.center = translate(self.placement, 0.5, 0.5, 0.5)
        self.shift()
        self.eligible = False
        self.cameraSpaceVertices = None
        self.cameraSpaceCenter = None
        self.transformedFaces = None
        self.selected = False

    def preprocess(self, camera):
        self.cameraSpaceCenter = self.center @ camera.cameraTransformation
        self.cameraSpaceCenter = self.cameraSpaceCenter[:3]
        arrangementValue = np.linalg.norm(self.cameraSpaceCenter)
        self.eligible = self.cameraSpaceCenter[2] >= -1.25 and arrangementValue <= renderingRadius
        if not self.eligible:
            return arrangementValue
        self.cameraSpaceVertices = self.vertices @ camera.cameraTransformation
        clippingSpaceVertices = self.cameraSpaceVertices @ projectionMatrix
        normalizedVertices = np.array([vertex / vertex[3] if nearClippingPlane < vertex[3] < farClippingPlane else np.array([0, 0, 0, 1]) for vertex in clippingSpaceVertices])
        screenSpaceVertices = normalizedVertices @ screenTransformation
        screenSpaceVertices = [vertex if vertex[2] > 0 else None for vertex in screenSpaceVertices]
        
        self.selected = False
        self.transformedFaces = []
        for i in range(len(self.faces)):
            transformedPolygon = [self.cameraSpaceVertices[vertex] for vertex in self.faces[i]]
            a = transformedPolygon[0][:3] - transformedPolygon[1][:3]
            b = transformedPolygon[2][:3] - transformedPolygon[1][:3]
            normal = np.cross(a, b)
            faceCenter = np.array([0., 0., 0.])
            vertexCount = 0
            for vertex in transformedPolygon:
                faceCenter += vertex[:3]
                vertexCount += 1
            faceCenter /= vertexCount
            culled = np.dot(normal, faceCenter) <= 0
            distance = np.linalg.norm(faceCenter)
            
            if not culled:
                if len(transformedPolygon) == 4:
                    if faceCenter[2] < 5 and np.dot(transformedPolygon[0][:2], transformedPolygon[2][:2]) + np.dot(transformedPolygon[1][:2], transformedPolygon[3][:2]) < -0.3:
                        if Block.target is None:
                            Block.target = [self, i, distance]
                        elif distance < Block.target[2]:
                            Block.target = [self, i, distance]
                
                transformedPolygon = [screenSpaceVertices[vertex] for vertex in self.faces[i] if screenSpaceVertices[vertex] is not None]
                self.transformedFaces.append(transformedPolygon)
            else:
                self.transformedFaces.append(None)
        
        return arrangementValue

    def project(self, screen):
        for i in range(len(self.transformedFaces)):
            face = self.transformedFaces[i]
            if face is not None and len(face) > 2:
                if self.selected and i == Block.target[1]:
                    pygame.draw.polygon(screen, [min(1.25 * color, 255) for color in self.colors[i]], [vertex[:2] for vertex in face])
                else:
                    pygame.draw.polygon(screen, self.colors[i], [vertex[:2] for vertex in face])
                pygame.draw.polygon(screen, [0.75 * color for color in self.colors[i]], [vertex[:2] for vertex in face], 1)

    def shift(self):
        self.vertices = translate(self.vertices, *self.placement[:3])
