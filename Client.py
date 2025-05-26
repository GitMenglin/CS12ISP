import socket
import pickle
import pygame
from math import *
import numpy as np

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
cyan = (0, 255, 255)
blue = (0, 0, 255)
globalOrigin = [0., 0., 0., 1.]
WIDTH, HEIGHT = 600, 600

def getTranslationMatrix(tX, tY, tZ):
    return np.array([
        [1, 0, 0, tX],
        [0, 1, 0, tY],
        [0, 0, 1, tZ],
        [0, 0, 0, 1]
    ])

def getRotationMatrix(rX, rY, rZ):
    mX = np.array([
        [1, 0, 0, 0],
        [0, cos(rX), -sin(rX), 0],
        [0, sin(rX), cos(rX), 0],
        [0, 0, 0, 1]
    ])
    mY = np.array([
        [cos(rY), 0, sin(rY), 0],
        [0, 1, 0, 0],
        [-sin(rY), 0, cos(rY), 0],
        [0, 0, 0, 1]
    ])
    mZ = np.array([
        [cos(rZ), -sin(rZ), 0, 0],
        [sin(rZ), cos(rZ), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    return mX @ mY @ mZ

def getScalingMatrix(sX, sY, sZ):
    return np.array([
        [sX, 0, 0, 0],
        [0, sY, 0, 0],
        [0, 0, sZ, 0],
        [0, 0, 0, 1]
    ])

def translate(vertices, tX, tY, tZ):
    transformation = getTranslationMatrix(tX, tY, tZ)
    return [vertex @ transformation for vertex in vertices]

def rotate(vertices, rX, rY, rZ):
    transformation = getRotationMatrix(rX, rY, rZ)
    return [vertex @ transformation for vertex in vertices]

def scale(vertices, sX, sY, sZ):
    transformation = getScalingMatrix(sX, sY, sZ)
    return [vertex @ transformation for vertex in vertices]

class Geometry:
    globalBasisVectors = [[
        np.array([0, 0, 0, 1]),
        np.array([1, 0, 0, 1]),
        np.array([0, 1, 0, 1]),
        np.array([0, 0, 1, 1])
    ], [
        [0, 1],
        [0, 2],
        [0, 3]
    ]]
    
    camera = [[
        np.array([0.0, 0.0, 0.0, 1.0]),
        np.array([-0.25, -0.25, 0.5, 1.0]),
        np.array([-0.25, 0.25, 0.5, 1.0]),
        np.array([0.25, 0.25, 0.5, 1.0]),
        np.array([0.25, -0.25, 0.5, 1.0]),
        np.array([0.0, 0.0, 0.5, 1.0])
    ], [
        [0, 1, 2],
        [0, 2, 3],
        [0, 3, 4],
        [0, 1, 4]
    ]]
    
    cube = [[
        np.array([0, 0, 0, 1]),
        np.array([0, 1, 0, 1]),
        np.array([1, 1, 0, 1]),
        np.array([1, 0, 0, 1]),
        np.array([0, 0, 1, 1]),
        np.array([0, 1, 1, 1]),
        np.array([1, 1, 1, 1]),
        np.array([1, 0, 1, 1])
        ], [
            [0, 1, 2, 3],
            [4, 7, 6, 5],
            [0, 4, 5, 1],
            [2, 6, 7, 3],
            [1, 5, 6, 2],
            [0, 3, 7, 4]
        ]]


class Camera:
    def __init__(self, globalPosition):
        self.globalPosition = globalPosition
        self.basisVectors = [
            np.array([0, 0, 1, 1]),
            np.array([0, 1, 0, 1]),
            np.array([1, 0, 0, 1])
        ]
        self.pitch = 0
        self.yaw = 0
        self.cameraTransformation = self.getCameraTranslation() @ self.getCameraRotation()
        self.translationalSpeed = 0.1
        self.angularSpeed = 0.01
        
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
        self.basisVectors = [
            np.array([0, 0, 1, 1]),
            np.array([0, 1, 0, 1]),
            np.array([1, 0, 0, 1])
        ]
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

class Player:
    def __init__(self, globalPosition=globalOrigin, geometry=Geometry.camera):
        self.globalPosition = np.array(globalPosition)
        self.vertices = geometry[0]
        self.faces = geometry[1]
        self.camera = Camera(self.globalPosition)
        self.name = ""
        self.font = pygame.font.SysFont("Arial", 20)
        
    def update(self):
        self.camera.control()
        self.globalPosition = self.camera.globalPosition
        self.camera.updateCameraTransformation()
        
    def project(self, camera, screenTransformation, screen):
        cameraTransformation = camera.cameraTransformation
        projectionMatrix = camera.projectionMatrix
        globalSpaceVertices = [vertex + np.array([*self.globalPosition[:3], 0.]) for vertex in rotate(self.vertices, self.camera.pitch, self.camera.yaw, 0)]
        cameraSpaceVertices = [vertex @ cameraTransformation for vertex in globalSpaceVertices]
        clippingSpaceVertices = [vertex @ projectionMatrix if vertex[2] > 0 else None for vertex in cameraSpaceVertices]
        normalizedVertices = [[coordinate / vertex[3] for coordinate in vertex] if vertex is not None else None for vertex in clippingSpaceVertices]
        screenSpaceVertices = [vertex @ screenTransformation if vertex is not None else None for vertex in normalizedVertices]
        for face in self.faces:
            polygon = [screenSpaceVertices[vertex] for vertex in face if screenSpaceVertices[vertex] is not None]
            if len(polygon) > 1:
                pygame.draw.polygon(screen, yellow, [vertex[:2] for vertex in polygon], 1)
        for vertex in screenSpaceVertices:
            if vertex is not None and 0 <= vertex[0] <= WIDTH and 0 <= vertex[1] <= HEIGHT:
                pygame.draw.circle(screen, yellow, vertex[:2], 2)
        if screenSpaceVertices[0] is not None and 0 <= screenSpaceVertices[0][0] <= WIDTH and 0 <= screenSpaceVertices[0][1] <= HEIGHT:
            screen.blit(self.font.render(self.name, True, black, white), [screenSpaceVertices[0][0] - 5 * len(self.name), screenSpaceVertices[0][1] - 10])

class Object3D:
    def __init__(self, geometry, color=green):
        self.vertices = geometry[0]
        self.faces = geometry[1]
        self.color = color
        
    def project(self, camera, screenTransformation, screen):
        cameraTransformation = camera.cameraTransformation
        projectionMatrix = camera.projectionMatrix
        cameraSpaceVertices = [vertex @ cameraTransformation for vertex in self.vertices]
        clippingSpaceVertices = [vertex @ projectionMatrix if vertex[2] > 0 else None for vertex in cameraSpaceVertices]
        normalizedVertices = [[coordinate / vertex[3] for coordinate in vertex] if vertex is not None else None for vertex in clippingSpaceVertices]
        screenSpaceVertices = [vertex @ screenTransformation if vertex is not None else None for vertex in normalizedVertices]
        
        for face in self.faces:
            polygon = [cameraSpaceVertices[vertex] for vertex in face if cameraSpaceVertices[vertex] is not None]
            vertexCount = len(polygon)
            if vertexCount > 2:
                a = polygon[0][:3] - polygon[1][:3]
                b = polygon[2][:3] - polygon[1][:3]
                normal = np.cross(a, b)
                center = np.array([0., 0., 0.])
                for vertex in polygon:
                    center += vertex[:3]
                if np.dot(normal, center) > 0:
                    polygon = [screenSpaceVertices[vertex] for vertex in face if screenSpaceVertices[vertex] is not None]
                    pygame.draw.polygon(screen, self.color, [vertex[:2] for vertex in polygon])
                    pygame.draw.polygon(screen, blue, [vertex[:2] for vertex in polygon], 1)
                    for vertex in polygon:
                        if vertex is not None and 0 <= vertex[0] <= WIDTH and 0 <= vertex[1] <= HEIGHT:
                            pygame.draw.circle(screen, blue, vertex[:2], 2)

class Engine3D:
    def __init__(self, players, objects):
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.players = players
        self.objects = objects
        self.screenTransformation = self.getScreenTransformation()
        
    def render(self):
        self.screen.fill(cyan)
        
        self.players[0].update()
        
        for obj in self.objects:
            obj.project(self.players[0].camera, self.screenTransformation, self.screen)
        for player in self.players[1:]:
            player.project(self.players[0].camera, self.screenTransformation, self.screen)
        
        pygame.draw.line(self.screen, white, [WIDTH / 2 - 10, HEIGHT / 2], [WIDTH / 2 + 10, HEIGHT / 2])
        pygame.draw.line(self.screen, white, [WIDTH / 2, HEIGHT / 2 - 10], [WIDTH / 2, HEIGHT / 2 + 10])
        
        pygame.display.update()
        self.clock.tick(60)
        
    def getScreenTransformation(self):
        return np.array([
            [WIDTH / 2, 0, 0, 0],
            [0, -HEIGHT / 2, 0, 0],
            [0, 0, 1, 0],
            [WIDTH / 2, HEIGHT / 2, 0, 1]
        ])

def main():
    ip = socket.gethostbyname(socket.gethostname())
    port = 1234
    address = (ip, port)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(address)
    name = input("Enter your name: ")
    
    pygame.init()
    players = [Player()]
    objects = [Object3D(Geometry.cube)]
    engine = Engine3D(players, objects)
    
    objects[0].vertices = [vertex + np.array([0.5, 0, 0.5, 0]) for vertex in objects[0].vertices]
    
    client.sendall(pickle.dumps([name, np.append(players[0].globalPosition[:3], 1), players[0].camera.pitch, players[0].camera.yaw]))
    client.settimeout(0.025)
    
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
        try:
            playerCount = pickle.loads(client.recv(20))
            while playerCount > len(players):
                players.append(Player())
            client.sendall(pickle.dumps([name, np.append(players[0].globalPosition[:3], 1), players[0].camera.pitch, players[0].camera.yaw]))
            for i in range(playerCount - 1):
                players[i + 1].name, players[i + 1].globalPosition, players[i + 1].camera.pitch, players[i + 1].camera.yaw = pickle.loads(client.recv(256))
        except:
            pass
        
        pygame.display.set_caption(f"{name}: {[int(coordinate) for coordinate in players[0].globalPosition[:3]]}")
        engine.render()
        
    client.close()
    pygame.quit()

main()
