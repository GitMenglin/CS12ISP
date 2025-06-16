import pygame
import numpy as np
from MathUtil import *
from Camera import Camera
from GeometryLib import Geometry
from Constants import *

class Player:
    def __init__(self, globalPosition=[worldSize // 2 + 0.5, 0., worldSize // 2 + 0.5, 1.], pitch=0, yaw=0, geometry="steve"):
        self.globalPosition = np.array(globalPosition)
        self.camera = Camera(self.globalPosition, pitch, yaw)
        self.geometry = geometry
        self.cameraSpacePosition = None
        self.cameraSpaceDistance = None
        self.name = ""
        self.font = pygame.font.SysFont("Arial", 15)
        self.velocityY = -0.01
        self.landed = False
        self.jumpCoolDownStart = 0
        self.swing = 0
        self.walkingStart = 0
        self.hotBar = [[name, block] for name, block in Geometry.blocks.items()]
        self.hotBarSelection = self.hotBar[0]

    def update(self, paused):
        self.camera.control(paused)
        self.globalPosition = self.camera.globalPosition
        self.camera.update()
        
        if not paused:
            if pygame.key.get_pressed()[pygame.K_SPACE] and self.landed and pygame.time.get_ticks() - self.jumpCoolDownStart > 600:
                self.velocityY = 0.15
                self.jumpCoolDownStart = pygame.time.get_ticks()
            self.camera.globalPosition += np.array([0, 1, 0, 1]) * self.velocityY
            self.velocityY -= 0.01
            
            keyPressed = pygame.key.get_pressed()
            currentTime = pygame.time.get_ticks()
            if keyPressed[pygame.K_a]: self.swing = pi / 6 * sin((currentTime - self.walkingStart) * 2 * pi / 1000)
            elif keyPressed[pygame.K_d]: self.swing = -pi / 6 * sin((currentTime - self.walkingStart) * 2 * pi / 1000)
            if keyPressed[pygame.K_w]: self.swing = pi / 3 * sin((currentTime - self.walkingStart) * 2 * pi / 1000)
            elif keyPressed[pygame.K_s]: self.swing = -pi / 3 * sin((currentTime - self.walkingStart) * 2 * pi / 1000)
            elif not (keyPressed[pygame.K_a] or keyPressed[pygame.K_d]):
                self.swing += -0.1 * self.swing
                self.walkingStart = pygame.time.get_ticks()
            
            if keyPressed[pygame.K_0]: self.geometry = "steve"
            elif keyPressed[pygame.K_1]: self.hotBarSelection = self.hotBar[0]
            elif keyPressed[pygame.K_2]: self.hotBarSelection = self.hotBar[1]
            elif keyPressed[pygame.K_3]: self.hotBarSelection = self.hotBar[2]
            elif keyPressed[pygame.K_4]: self.hotBarSelection = self.hotBar[3]
            elif keyPressed[pygame.K_5]: self.hotBarSelection = self.hotBar[4]
            elif keyPressed[pygame.K_RALT]: self.geometry = "herobrine"

    def checkCollisionVertical(self, block):
        x, y, z = block.center[:3] - self.camera.globalPosition[:3]
        
        landing = -2 <= y <= 0 and abs(x) <= 0.5 and abs(z) <= 0.5
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
        self.cameraSpacePosition = translate(self.globalPosition, 0, -0.5, 0) @ camera.cameraTransformation
        self.cameraSpaceDistance = np.linalg.norm(self.cameraSpacePosition[:3])
        return self.cameraSpaceDistance

    def project(self, camera, screen):
        if self.cameraSpaceDistance <= 10:
            rX = [self.camera.pitch, 0, self.swing, -self.swing, -self.swing, self.swing]
            shift = [-0.1, -0.1, -0.225, -0.225, -0.8, -0.8]
            geometry = Geometry.players[self.geometry]
            
            partsArrangement = []
            for i in range(len(geometry)):
                localCenter = np.array([0., 0., 0.])
                for vertex in geometry[i][0][:8]:
                    localCenter += vertex[:3]
                localCenter /= 8
                cameraRelativeCenter = translate(rotate(np.array([*localCenter, 1.0]), rX[i], self.camera.yaw, 0), *translate(self.globalPosition, 0, shift[i], 0)[:3]) @ camera.cameraTransformation
                arrangementValue = np.linalg.norm(cameraRelativeCenter[:3])
                
                if not partsArrangement:
                    partsArrangement.append([i, arrangementValue])
                    continue
                partsArranged = []
                inserted = False
                for arranged in partsArrangement:
                    if arrangementValue > arranged[1] and not inserted:
                        partsArranged.append([i, arrangementValue])
                        inserted = True
                    partsArranged.append(arranged)
                if not inserted:
                    partsArranged.append([i, arrangementValue])
                partsArrangement = partsArranged
            
            for part in partsArrangement:
                self.projectPart(geometry[part[0]], rX[part[0]], shift[part[0]], camera, screen)
            
            clippingSpacePosition = translate(self.cameraSpacePosition, 0, 1.15, 0) @ projectionMatrix
            normalizedPosition = clippingSpacePosition / clippingSpacePosition[3] if clippingSpacePosition[3] > 0 else np.array([-1, -1, -1, 1])
            screenSpacePosition = normalizedPosition @ screenTransformation
            screenSpacePosition = screenSpacePosition if screenSpacePosition[2] > 0 else None
            if screenSpacePosition is not None:
                x, y = screenSpacePosition[0], screenSpacePosition[1]
                if 0 <= x <= WIDTH and 0 <= y <= HEIGHT:
                    screen.blit(self.font.render(self.name, True, black, white), [x - 3.75 * len(self.name), y - 7.5])

    def projectPart(self, part, rX, shift, camera, screen):
        globalSpaceVertices = np.array([translate(vertex, *translate(self.globalPosition, 0, shift, 0)[:3]) for vertex in rotate(part[0], rX, self.camera.yaw, 0)])
        cameraSpaceVertices = globalSpaceVertices @ camera.cameraTransformation
        clippingSpaceVertices = cameraSpaceVertices @ projectionMatrix
        normalizedVertices = np.array([vertex / vertex[3] if vertex[3] > 0 else np.array([-1, -1, -1, 1]) for vertex in clippingSpaceVertices])
        screenSpaceVertices = normalizedVertices @ screenTransformation
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
