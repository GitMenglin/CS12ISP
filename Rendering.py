import pygame
import noise
import random
from Entity import *
from GeometryLib import Geometry
from Constants import *

class Engine3D:
    def __init__(self, players):
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.DOUBLEBUF | pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.players = players
        self.entities = None
        self.excavateStart = 0
        self.coolDownStart = 0
        self.synchronization = None
        self.generateTerrain()

    def render(self, paused):
        self.synchronization = None
        self.screen.fill(cyan)
        self.players[0].update(paused)
        self.project()
        
        pygame.display.update()
        self.clock.tick(60)

    def project(self):
        Block.target = None
        entitiesArrangement = self.arrangeEntities()
        playersArrangement, playerCount = self.arrangePlayers()
        
        if not pygame.mouse.get_pressed()[0]:
            self.excavateStart = pygame.time.get_ticks()
        if Block.target is not None:
            Block.target[0].selected = True
            if pygame.mouse.get_pressed()[0] and pygame.time.get_ticks() - self.excavateStart > 1000:
                self.synchronization = Block.target[0].placement[:3]
                x, y, z = self.synchronization
                self.entities[x][y][z] = None
                BlockPool.release(Block.target[0])
                self.excavateStart = pygame.time.get_ticks()
            if pygame.mouse.get_pressed()[2]:
                if pygame.time.get_ticks() - self.coolDownStart > 200:
                    self.placeBlock(Block.target)
                self.coolDownStart = pygame.time.get_ticks()
        else:
            self.excavateStart = pygame.time.get_ticks()
        
        playerRendered = 0
        self.players[0].landed = False
        for entity in entitiesArrangement:
            while (playerRendered < playerCount and 
                   playersArrangement[playerRendered][1] > entity[1]):
                playersArrangement[playerRendered][0].project(self.players[0].camera, self.screen)
                playerRendered += 1
            entity[0].project(self.screen)
            cameraRelativeCenter = entity[0].center[:3] - self.players[0].camera.globalPosition[:3]
            horizontalDistance = np.linalg.norm(np.array([cameraRelativeCenter[0], cameraRelativeCenter[2]]))
            if horizontalDistance <= 1.25:
                self.players[0].checkCollisionHorizontal(entity[0])
            if horizontalDistance <= 0.75:
                self.players[0].checkCollisionVertical(entity[0])
        while playerRendered < playerCount:
            playersArrangement[playerRendered][0].project(self.players[0].camera, self.screen)
            playerRendered += 1
        
        pygame.draw.line(self.screen, white, [WIDTH / 2 - 10, HEIGHT / 2], [WIDTH / 2 + 10, HEIGHT / 2])
        pygame.draw.line(self.screen, white, [WIDTH / 2, HEIGHT / 2 - 10], [WIDTH / 2, HEIGHT / 2 + 10])

    def placeBlock(self, target):
        placement = target[0].placement[:3] + Block.normalsArranged[target[1]]
        playerGlobalPosition = self.players[0].globalPosition[:3]
        if all([placement[i] == floor(playerGlobalPosition[i]) if i != 1 else placement[i] == floor(playerGlobalPosition[i]) or placement[i] == floor(playerGlobalPosition[i]) - 1 for i in range(3)]):
            return
        
        x, y, z = placement
        if 0 <= x < len(self.entities) and 0 <= y < len(self.entities[0]) and 0 <= z < len(self.entities[0][0]) and self.entities[x][y][z] is None:
            self.entities[x][y][z] = BlockPool.acquire(Geometry.grassBlock, placement)
            self.synchronization = placement

    def arrangeEntities(self):
        entitiesArrangement = []
        x, y, z = floor(self.players[0].globalPosition[0] - renderingRadius), floor(self.players[0].globalPosition[1] - renderingRadius), floor(self.players[0].globalPosition[2] - renderingRadius)
        
        for i in range(max(x, 0), min(len(self.entities), int(x + renderingRange))):
            for j in range(max(y, 0), min(len(self.entities[0]), int(y + renderingRange))):
                for k in range(max(z, 0), min(len(self.entities[0][0]), int(z + renderingRange))):
                    entity = self.entities[i][j][k]
                    if entity is not None:
                        arrangementValue = entity.preprocess(self.players[0].camera)
                        if not entity.eligible:
                            continue
                        elif not entitiesArrangement:
                            entitiesArrangement.append([entity, arrangementValue])
                            continue
                        
                        entitiesArranged = []
                        inserted = False
                        for arranged in entitiesArrangement:
                            if arrangementValue > arranged[1] and not inserted:
                                entitiesArranged.append([entity, arrangementValue])
                                inserted = True
                            entitiesArranged.append(arranged)
                        if not inserted:
                            entitiesArranged.append([entity, arrangementValue])
                        entitiesArrangement = entitiesArranged
        
        return entitiesArrangement

    def arrangePlayers(self):
        if len(self.players) > 1:
            playersArrangement = [[self.players[1], self.players[1].getArrangementValue(self.players[0].camera)]]
            playerCount = 0
            for player in self.players[1:]:
                playersArranged = []
                inserted = False
                arrangementValue = player.getArrangementValue(self.players[0].camera)
                for arranged in playersArrangement:
                    if arrangementValue > arranged[1] and not inserted:
                        playersArranged.append([player, arrangementValue])
                        inserted = True
                    playersArranged.append(arranged)
                if not inserted: 
                    playersArranged.append([player, arrangementValue])
                playersArrangement = playersArranged
                playerCount += 1
            return [playersArrangement, playerCount]
        else:
            return [[], 0]

    def generateTerrain(self):
        scale = random.randint(int(0.8 * worldSize), int(1.2 * worldSize))
        stretch = random.randint(10, worldSize)
        width, height, depth = worldSize, 2 * worldSize, worldSize
        self.entities = [[[None for _ in range(depth)] for _ in range(height)] for _ in range(width)]
        
        for x in range(width):
            for z in range(depth):
                y = int(stretch * noise.pnoise2(x / scale, z / scale, octaves=4) + worldSize)
                self.entities[x][y][z] = BlockPool.acquire(Geometry.grassBlock, [x, y, z])
                # for i in range(y + 1):
                #     self.entities[x][i][z] = BlockPool.acquire(Geometry.grassBlock, [x, i, z])
                if x == worldSize // 2 and z == worldSize // 2:
                    self.players[0].camera.globalPosition[1] = y + 3
