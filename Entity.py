import pygame
from math import *
import numpy as np
from GeometryLib import Geometry
from MathUtil import *
from Constants import *

# AI recommended Object Pooling for block creation management and reduced garbage collection pressure
class BlockPool:
    pool = []
    
    def acquire(blockType, placement):
        if BlockPool.pool:
            block = BlockPool.pool.pop()
            block.__init__(Geometry.blocks[blockType], placement)
            return block
        return Block(Geometry.blocks[blockType], placement)
    
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
        self.faceCount = len(self.faces)
        self.colors = geometry[2]
        self.placement = np.array([*placement, 1])
        self.center = translate(self.placement, 0.5, 0.5, 0.5)
        self.transformedFaces = None
        self.shift()
        self.selected = False

    def preprocess(self, camera):
        cameraSpaceVertices = self.vertices @ camera.cameraTransformation
        normalizedVertices = np.array([np.array([*(vertex[:3] / vertex[2]), 1.]) if vertex[2] > 0 else np.array([-1, -1, -1, 1]) for vertex in cameraSpaceVertices])
        screenSpaceVertices = normalizedVertices @ cameraToClippingToScreenTransformation
        screenSpaceVertices = [vertex if vertex[2] > 0 else None for vertex in screenSpaceVertices]
        
        self.selected = False
        self.transformedFaces = []
        for i in range(self.faceCount):
            transformedPolygon = [cameraSpaceVertices[vertex] for vertex in self.faces[i]]
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
            distance = sqrt(faceCenter[0]**2 + faceCenter[1]**2 + faceCenter[2]**2)
            
            if not culled:
                if i < 6 and vertexCount >= 3:
                    if 0 < faceCenter[2] < 5 and np.dot(transformedPolygon[0][:2], transformedPolygon[vertexCount // 2][:2]) + np.dot(transformedPolygon[vertexCount // 4][:2], transformedPolygon[3 * vertexCount // 4][:2]) < -0.25:
                        if not Block.target:
                            Block.target = [self, i, distance]
                        elif distance < Block.target[2]:
                            Block.target = [self, i, distance]
                
                transformedPolygon = [screenSpaceVertices[vertex] for vertex in self.faces[i] if screenSpaceVertices[vertex] is not None]
                self.transformedFaces.append(transformedPolygon)
            else:
                self.transformedFaces.append(None)

    def project(self, screen):
        for i in range(self.faceCount):
            polygon = self.transformedFaces[i]
            if polygon and len(polygon) > 2:
                if self.selected and i == Block.target[1]:
                    pygame.draw.polygon(screen, [min(1.25 * color, 255) for color in self.colors[i]], [vertex[:2] for vertex in polygon])
                else:
                    pygame.draw.polygon(screen, self.colors[i], [vertex[:2] for vertex in polygon])
                pygame.draw.polygon(screen, [0.75 * color for color in self.colors[i]], [vertex[:2] for vertex in polygon], 1)

    def shift(self):
        self.vertices = translate(self.vertices, *self.placement[:3])
