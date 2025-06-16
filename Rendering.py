import pygame
import noise
import random
from Entity import *
from GeometryLib import Geometry
from Constants import *

class Engine3D:
    def __init__(self, players):
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.players = players
        self.entities = None
        self.excavateStart = 0
        self.coolDownStart = 0
        self.synchronization = None

    def render(self, paused):
        self.synchronization = None
        self.screen.fill(void)
        self.players[0].update(paused)
        self.project(paused)
        
        pygame.display.update()
        self.clock.tick(40)

    def project(self, paused):
        Block.target = None
        entitiesArrangement = self.arrangeEntities()
        playersArrangement, playerCount = self.arrangePlayers()
        
        if not paused:
            if not pygame.mouse.get_pressed()[0]:
                self.excavateStart = pygame.time.get_ticks()
            if Block.target:
                Block.target[0].selected = True
                if pygame.mouse.get_pressed()[0] and pygame.time.get_ticks() - self.excavateStart > 1000:
                    self.synchronization = [None, Block.target[0].placement[:3]]
                    x, y, z = self.synchronization[1]
                    BlockPool.release(self.entities[x][y][z])
                    self.entities[x][y][z] = None
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
            horizontalDistance = np.linalg.norm(cameraRelativeCenter[::2])
            if horizontalDistance <= 0.75:
                self.players[0].checkCollisionVertical(entity[0])
            if horizontalDistance <= 1.25:
                self.players[0].checkCollisionHorizontal(entity[0])
        while playerRendered < playerCount:
            playersArrangement[playerRendered][0].project(self.players[0].camera, self.screen)
            playerRendered += 1
        
        pygame.draw.line(self.screen, white, [WIDTH / 2 - 10, HEIGHT / 2], [WIDTH / 2 + 10, HEIGHT / 2])
        pygame.draw.line(self.screen, white, [WIDTH / 2, HEIGHT / 2 - 10], [WIDTH / 2, HEIGHT / 2 + 10])

    def placeBlock(self, target):
        placement = target[0].placement[:3] + Block.normalsArranged[target[1]]
        if any([all([placement[i] == floor(player.globalPosition[i]) if i != 1 else placement[i] == floor(player.globalPosition[i]) or placement[i] == floor(player.globalPosition[i]) - 1 for i in range(3)]) for player in self.players]):
            return
        
        x, y, z = placement
        if 0 <= x < len(self.entities) and 0 <= y < len(self.entities[0]) and 0 <= z < len(self.entities[0][0]) and self.entities[x][y][z] is None:
            self.entities[x][y][z] = BlockPool.acquire(self.players[0].hotBarSelection[1], placement)
            self.synchronization = [self.players[0].hotBarSelection[0], placement]

    def arrangeEntities(self):
        entitiesArrangement = []
        x, y, z = floor(self.players[0].globalPosition[0] - renderingRadius), floor(self.players[0].globalPosition[1] - renderingRadius), floor(self.players[0].globalPosition[2] - renderingRadius)
        
        for i in range(max(x, 0), min(len(self.entities), int(x + renderingRange))):
            for j in range(max(y, 0), min(len(self.entities[0]), int(y + renderingRange))):
                for k in range(max(z, 0), min(len(self.entities[0][0]), int(z + renderingRange))):
                    entity = self.entities[i][j][k]
                    if entity is not None:
                        if (self.entities[i + 1][j][k] is not None and self.entities[i - 1][j][k] is not None and
                            self.entities[i][j + 1][k] is not None and self.entities[i][j - 1][k] is not None and
                            self.entities[i][j][k + 1] is not None and self.entities[i][j][k - 1] is not None):
                            continue
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
        stretch = random.randint(10, worldSize // 10)
        scale = random.randint(int(0.75 * stretch), int(1.25 * stretch))
        width, height, depth = worldSize, worldSize // 5, worldSize
        self.entities = [[[None for _ in range(depth)] for _ in range(height)] for _ in range(width)]
        loadingPacket = [[[None for _ in range(depth)] for _ in range(height)] for _ in range(width)]
        
        for x in range(width):
            for z in range(depth):
                y = int(stretch * noise.pnoise2(x / scale, z / scale, octaves=4) + worldSize // 10)
                for i in range(y, -1, -1):
                    if y - i >= 4 or i <= worldSize // 20:
                        self.entities[x][i][z] = BlockPool.acquire(Geometry.stone, [x, i, z])
                        loadingPacket[x][i][z] = "stone"
                    elif i == y:
                        self.entities[x][i][z] = BlockPool.acquire(Geometry.grassBlock, [x, i, z])
                        loadingPacket[x][i][z] = "grassBlock"
                    else:
                        self.entities[x][i][z] = BlockPool.acquire(Geometry.dirt, [x, i, z])
                        loadingPacket[x][i][z] = "dirt"
                if x == worldSize // 2 and z == worldSize // 2:
                    self.players[0].camera.globalPosition[1] = y + 3
        
        return [loadingPacket, [width, height, depth, self.players[0].camera.globalPosition[1]]]

    def loadTerrain(self, loadingPacket):
        width, height, depth, spawnHeight = loadingPacket[1]
        self.entities = [[[None for _ in range(depth)] for _ in range(height)] for _ in range(width)]
        self.players[0].camera.globalPosition[1] = spawnHeight
        
        for x in range(width):
            for y in range(height):
                for z in range(depth):
                    blockType = loadingPacket[0][x][y][z]
                    if blockType:
                        self.entities[x][y][z] = BlockPool.acquire(Geometry.blocks[blockType], [x, y, z])
