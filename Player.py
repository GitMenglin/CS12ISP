import pygame
import numpy as np
from MathUtil import *
from Camera import Camera
from GeometryLib import Geometry
from Constants import *

class Player:
    def __init__(self, globalPosition=[worldSize // 2 + 0.5, 0., worldSize // 2 + 0.5, 1.], pitch=0, yaw=0, skin="steve"):
        self.globalPosition = np.array(globalPosition)
        self.camera = Camera(self.globalPosition, pitch, yaw)
        self.skin, self.currentSkin = skin, skin
        self.cameraSpacePosition = None
        self.cameraSpaceDistance = None
        self.name = ""
        self.font = pygame.font.SysFont("Arial", 15)
        self.velocityY = -0.01
        self.landed = False
        self.blocked = False
        self.jumpCoolDownStart = 0
        self.swing = 0
        self.walkingStart = 0
        self.hotBar = [blockType for blockType in Geometry.blocks]
        self.hotBarSelection = self.hotBar[0]
        self.hotBarTransformation = getTranslationMatrix(-0.5, -0.5, -0.5) @ getScalingMatrix(20, 20, 20) @ getRotationX(-5 * pi / 6) @ getRotationY(-pi / 4)

    def update(self, keyPressed, paused):
        self.camera.control(paused)
        self.globalPosition = self.camera.globalPosition
        self.camera.update(keyPressed)
        
        if not paused:
            if keyPressed[pygame.K_SPACE] and self.landed and not self.blocked and pygame.time.get_ticks() - self.jumpCoolDownStart > 600:
                self.velocityY = 0.15
                self.jumpCoolDownStart = pygame.time.get_ticks()
            self.camera.globalPosition += np.array([0, 1, 0, 1]) * self.velocityY
            self.velocityY -= 0.01
            
            currentTime = pygame.time.get_ticks()
            if keyPressed[pygame.K_a]: self.swing = pi / 6 * sin((currentTime - self.walkingStart) * 2 * pi / 1000)
            elif keyPressed[pygame.K_d]: self.swing = -pi / 6 * sin((currentTime - self.walkingStart) * 2 * pi / 1000)
            if keyPressed[pygame.K_w]: self.swing = pi / 3 * sin((currentTime - self.walkingStart) * 2 * pi / 1000)
            elif keyPressed[pygame.K_s]: self.swing = -pi / 3 * sin((currentTime - self.walkingStart) * 2 * pi / 1000)
            elif not (keyPressed[pygame.K_a] or keyPressed[pygame.K_d]):
                self.swing += -0.2 * self.swing
                self.walkingStart = pygame.time.get_ticks()
            
            if keyPressed[pygame.K_0]: self.currentSkin = self.skin
            elif keyPressed[pygame.K_1]: self.hotBarSelection = self.hotBar[0]
            elif keyPressed[pygame.K_2]: self.hotBarSelection = self.hotBar[1]
            elif keyPressed[pygame.K_3]: self.hotBarSelection = self.hotBar[2]
            elif keyPressed[pygame.K_4]: self.hotBarSelection = self.hotBar[3]
            elif keyPressed[pygame.K_5]: self.hotBarSelection = self.hotBar[4]
            elif keyPressed[pygame.K_RALT]: self.currentSkin = "herobrine"
        
        self.landed = False
        self.blocked = False

    def displayHotBar(self, screen):
        pygame.draw.rect(screen, gray, [275, 540, 250, 50])
        for i in range(5):
            hotBarGeometry = Geometry.hotBar[self.hotBar[i]]
            if self.hotBar[i] == self.hotBarSelection:
                pygame.draw.rect(screen, white, [50 * i + 275, 540, 50, 50], 4)
            vertices = hotBarGeometry[0] @ getTranslationMatrix(50 * i + 300, 565, 0)
            faceCount = len(hotBarGeometry[1])
            for j in range(faceCount):
                if faceCount == 8 and j == 6:
                    continue
                polygon = [vertices[vertex] for vertex in hotBarGeometry[1][j]]
                pygame.draw.polygon(screen, hotBarGeometry[2][j], [vertex[:2] for vertex in polygon])

    def checkCollisionVertical(self, block):
        x, y, z = block.center[:3] - self.camera.globalPosition[:3]
        
        landing = -2 <= y <= 0 and abs(x) <= 0.5 and abs(z) <= 0.5
        self.blocked = 0 < y <= 0.75
        if not self.landed and landing:
            self.velocityY = 0
        if landing and abs(x) < 0.5 and abs(z) < 0.5:
            self.camera.globalPosition[1] += y + 2
        self.landed = landing

    def checkCollisionHorizontal(self, block):
        x, y, z = block.center[:3] - self.camera.globalPosition[:3]
        
        if -1.75 <= y <= 0.75:
            if abs(x) <= 0.5:
                if 0 < z <= 1:
                    for basis in self.camera.basisVelocities:
                        if basis[2] > 0:
                            basis[2] = 0
                    self.landed = self.velocityY == 0
                elif -1 <= z < 0:
                    for basis in self.camera.basisVelocities:
                        if basis[2] < 0:
                            basis[2] = 0
                    self.landed = self.velocityY == 0
            if abs(z) <= 0.5:
                if 0 < x <= 1:
                    for basis in self.camera.basisVelocities:
                        if basis[0] > 0:
                            basis[0] = 0
                    self.landed = self.velocityY == 0
                elif -1 <= x < 0:
                    for basis in self.camera.basisVelocities:
                        if basis[0] < 0:
                            basis[0] = 0
                    self.landed = self.velocityY == 0

    def getArrangementValue(self, camera):
        self.cameraSpacePosition = translate(self.globalPosition, 0, -0.55, 0) @ camera.cameraTransformation
        self.cameraSpaceDistance = sqrt(self.cameraSpacePosition[0]**2 + self.cameraSpacePosition[1]**2 + self.cameraSpacePosition[2]**2)
        return self.cameraSpaceDistance

    def project(self, camera, screen):
        if self.cameraSpaceDistance <= 10:
            geometry = Geometry.players[self.currentSkin]
            rX = [self.camera.pitch, 0, self.swing, -self.swing, -self.swing, self.swing]
            rotationY = getRotationY(self.camera.yaw)
            offset = [-0.1, -0.1, -0.225, -0.225, -0.8, -0.8]
            
            partsArrangement = []
            for i in range(6):
                localCenter = np.array([0., 0., 0.])
                for vertex in geometry[i][0][:8]:
                    localCenter += vertex[:3]
                localCenter /= 8
                rotation = getRotationX(rX[i]) @ rotationY
                translation = getTranslationMatrix(*(self.globalPosition @ getTranslationMatrix(0, offset[i], 0))[:3])
                transformation = rotation @ translation
                cameraRelativeCenter = (np.array([*localCenter, 1.]) @ transformation)[:3] - camera.globalPosition[:3]
                arrangementValue = sqrt(cameraRelativeCenter[0]**2 + cameraRelativeCenter[1]**2 + cameraRelativeCenter[2]**2)
                
                if not partsArrangement:
                    partsArrangement.append([i, arrangementValue, rotation, translation])
                    continue
                partsArranged = []
                inserted = False
                for arranged in partsArrangement:
                    if arrangementValue > arranged[1] and not inserted:
                        partsArranged.append([i, arrangementValue, rotation, translation])
                        inserted = True
                    partsArranged.append(arranged)
                if not inserted:
                    partsArranged.append([i, arrangementValue, rotation, translation])
                partsArrangement = partsArranged
            
            for part in partsArrangement:
                self.projectPart(geometry[part[0]], part[2], part[3], camera, screen)
            
            cameraSpacePosition = translate(self.cameraSpacePosition, 0, 1.15, 0)
            normalizedPosition = np.array([*(cameraSpacePosition[:3] / cameraSpacePosition[2]), 1.]) if cameraSpacePosition[2] > 0 else np.array([-1, -1, -1, 1])
            screenSpacePosition = normalizedPosition @ cameraToClippingToScreenTransformation
            screenSpacePosition = screenSpacePosition if screenSpacePosition[2] > 0 else None
            if screenSpacePosition is not None:
                x, y = screenSpacePosition[0], screenSpacePosition[1]
                if 0 <= x <= WIDTH and 0 <= y <= HEIGHT:
                    screen.blit(self.font.render(self.name, True, black, white), [x - 3.75 * len(self.name), y - 7.5])

    def projectPart(self, part, rotation, translation, camera, screen):
        globalToCameraTransformation = rotation @ translation @ camera.cameraTransformation
        cameraSpaceVertices = part[0] @ globalToCameraTransformation
        normalizedVertices = np.array([np.array([*(vertex[:3] / vertex[2]), 1.]) if vertex[2] > 0 else np.array([-1, -1, -1, 1]) for vertex in cameraSpaceVertices])
        screenSpaceVertices = normalizedVertices @ cameraToClippingToScreenTransformation
        screenSpaceVertices = [vertex if vertex[2] > 0 else None for vertex in screenSpaceVertices]
        
        for j in range(len(part[1])):
            polygon = [cameraSpaceVertices[vertex] for vertex in part[1][j]]
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
                polygon = [screenSpaceVertices[vertex] for vertex in part[1][j] if screenSpaceVertices[vertex] is not None]
                if len(polygon) > 2:
                    pygame.draw.polygon(screen, part[2][j], [vertex[:2] for vertex in polygon])
                    pygame.draw.polygon(screen, [0.75 * color for color in part[2][j]], [vertex[:2] for vertex in polygon], 1)
