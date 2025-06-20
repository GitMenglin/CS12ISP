import pygame
import noise
import random
from Entity import *
from Constants import *

class Engine3D:
    def __init__(self):
        self.screen = None
        self.clock = None
        self.players = None
        self.entities = None
        self.maxX, self.maxY, self.maxZ = None, None, None
        self.excavateStart = 0
        self.coolDownStart = 0
        self.synchronization = None
        self.paused = False
        self.done = False
        self.reconnect = False
        
        self.font = pygame.font.SysFont("Arial", 30)
        self.menu = pygame.sprite.Sprite()
        self.menu.image = pygame.Surface([100, 50])
        self.menu.image.fill(green)
        self.menu.rect = self.menu.image.get_rect(center=[WIDTH//2, HEIGHT//10])
        self.menuButton = pygame.sprite.Group([self.menu])

    def render(self, keyPressed):
        self.synchronization = None
        self.screen.fill(void)
        self.players[0].update(keyPressed, self.paused)
        self.project()
        self.players[0].displayHotBar(self.screen)
        
        if self.paused:
            x, y = pygame.mouse.get_pos()
            mousePressed = pygame.mouse.get_pressed()
            if self.menu.rect.collidepoint(x, y):
                self.menu.image.fill(yellow)
                if mousePressed[0]:
                    self.reconnect = True
            else:
                self.menu.image.fill(green)
            
            self.menuButton.draw(self.screen)
            self.screen.blit(self.font.render("Menu", True, blue), [WIDTH//2 - 40, HEIGHT//10 - 20])
        
        pygame.display.update()
        self.clock.tick(40)

    def project(self):
        Block.target = None
        entitiesArrangement = self.arrangeEntities()
        playersArrangement, playerCount = self.arrangePlayers()
        
        mouseKeyPressed = pygame.mouse.get_pressed()
        if not mouseKeyPressed[0]:
            self.excavateStart = pygame.time.get_ticks()
        if not self.paused:
            if Block.target:
                Block.target[0].selected = True
                if mouseKeyPressed[0] and pygame.time.get_ticks() - self.excavateStart > 1000:
                    self.synchronization = [None, Block.target[0].placement[:3]]
                    x, y, z = self.synchronization[1]
                    self.entities[x][y][z] = None
                    self.excavateStart = pygame.time.get_ticks()
                if mouseKeyPressed[2]:
                    if pygame.time.get_ticks() - self.coolDownStart > 200:
                        self.placeBlock(Block.target)
                    self.coolDownStart = pygame.time.get_ticks()
            else:
                self.excavateStart = pygame.time.get_ticks()
        
        playerRendered = 0
        for entity in entitiesArrangement:
            while (playerRendered < playerCount and 
                   playersArrangement[playerRendered][1] > entity[1]):
                playersArrangement[playerRendered][0].project(self.players[0].camera, self.screen)
                playerRendered += 1
            entity[0].project(self.screen)
            cameraRelativeCenter = entity[0].center[:3] - self.players[0].camera.globalPosition[:3]
            horizontalDistance = sqrt(cameraRelativeCenter[0]**2 + cameraRelativeCenter[2]**2)
            verticalDistance = entity[0].center[1] - self.players[0].camera.globalPosition[1]
            if horizontalDistance <= 0.75 and -2.25 <= verticalDistance <= 1.25:
                self.players[0].checkCollisionVertical(entity[0])
            if horizontalDistance <= 1.25 and -1.75 <= verticalDistance <= 0.75:
                self.players[0].checkCollisionHorizontal(entity[0])
            BlockPool.release(entity[0])
        while playerRendered < playerCount:
            playersArrangement[playerRendered][0].project(self.players[0].camera, self.screen)
            playerRendered += 1
        
        pygame.draw.line(self.screen, white, [WIDTH / 2 - 10, HEIGHT / 2], [WIDTH / 2 + 10, HEIGHT / 2])
        pygame.draw.line(self.screen, white, [WIDTH / 2, HEIGHT / 2 - 10], [WIDTH / 2, HEIGHT / 2 + 10])

    def placeBlock(self, target):
        placement = target[0].placement[:3] + Block.normalsArranged[target[1]]
        if any([all([placement[i] == floor(player.globalPosition[i]) if i != 1 else placement[i] == floor(player.globalPosition[i]) or placement[i] == floor(player.globalPosition[i]) - 1 for i in range(3)]) for player in self.players if player]):
            return
        
        x, y, z = placement
        if 0 <= x < self.maxX and 0 <= y < self.maxY and 0 <= z < self.maxZ and self.entities[x][y][z] is None:
            self.entities[x][y][z] = self.players[0].hotBarSelection
            self.synchronization = [self.players[0].hotBarSelection, placement]

    def arrangeEntities(self):
        entitiesArrangement = []
        x, y, z = floor(self.players[0].globalPosition[0] - renderingRadius), floor(self.players[0].globalPosition[1] - renderingRadius), floor(self.players[0].globalPosition[2] - renderingRadius)
        
        for j in range(min(int(y + renderingRange - 1), self.maxY), max(y - 1, 0), -1):
            overlaid = True
            for i in range(max(x, 0), min(int(x + renderingRange), self.maxX)):
                for k in range(max(z, 0), min(int(z + renderingRange), self.maxZ)):
                    blockType = self.entities[i][j][k]
                    if blockType:
                        block = BlockPool.acquire(blockType, [i, j, k])
                        blockInCameraSpaceCenter = block.center @ self.players[0].camera.cameraTransformation
                        arrangementValue = sqrt(blockInCameraSpaceCenter[0]**2 + blockInCameraSpaceCenter[1]**2 + blockInCameraSpaceCenter[2]**2)
                        if arrangementValue > renderingRadius:
                            BlockPool.release(block)
                            continue
                        
                        horizontalRelativeBlockCenter = (block.center[:3] - self.players[0].camera.globalPosition[:3])[::2]
                        horizontalRelativeBlockCenter /= sqrt(horizontalRelativeBlockCenter[0]**2 + horizontalRelativeBlockCenter[1]**2)
                        cameraBasisZ = self.players[0].camera.basisVectors[0][::2]
                        cameraBasisZ /= sqrt(cameraBasisZ[0]**2 + cameraBasisZ[1]**2)
                        
                        horizontalAngle = acos(np.dot(horizontalRelativeBlockCenter, cameraBasisZ))
                        if ((horizontalAngle > 1.5 * horizontalFieldOfView / 2) and arrangementValue > 3.5):
                            BlockPool.release(block)
                            continue
                        elif not self.entities[i][min(j + 1, self.maxY - 1)][k]: pass
                        elif not self.entities[min(i + 1, self.maxX - 1)][j][k]: pass
                        elif not self.entities[i - 1][j][k]: pass
                        elif not self.entities[i][j][min(k + 1, self.maxZ - 1)]: pass
                        elif not self.entities[i][j][k - 1]: pass
                        elif not self.entities[i][j - 1][k]: pass
                        elif self.entities[min(i + 1, self.maxX - 1)][j][k] == "leaves": pass
                        elif self.entities[i - 1][j][k] == "leaves": pass
                        elif self.entities[i][j][min(k + 1, self.maxZ - 1)] == "leaves": pass
                        elif self.entities[i][j][k - 1] == "leaves": pass
                        elif self.entities[i][min(j + 1, self.maxY - 1)][k] == "leaves": pass
                        elif self.entities[i][j - 1][k] == "leaves": pass
                        elif i == 0 or j == 0 or k == 0 or i == self.maxX or j == self.maxY or k == self.maxZ: pass
                        else:
                            BlockPool.release(block)
                            continue
                        block.preprocess(self.players[0].camera)
                        if not entitiesArrangement:
                            entitiesArrangement.append([block, arrangementValue])
                            overlaid = False
                            continue
                        
                        entitiesArranged = []
                        inserted = False
                        for arranged in entitiesArrangement:
                            if arrangementValue > arranged[1] and not inserted:
                                entitiesArranged.append([block, arrangementValue])
                                inserted = True
                            entitiesArranged.append(arranged)
                        if not inserted:
                            entitiesArranged.append([block, arrangementValue])
                        entitiesArrangement = entitiesArranged
                    overlaid = False
            if overlaid: break
        
        return entitiesArrangement

    def arrangePlayers(self):
        if len(self.players) > 1:
            playersArrangement = []
            playerCount = 0
            for player in self.players[1:]:
                if not playersArrangement:
                    if player:
                        playersArrangement.append([player, player.getArrangementValue(self.players[0].camera)])
                        playerCount += 1
                    continue
                if player:
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
        stretch = random.randint(10, worldSize // 6)
        scale = random.randint(int(0.75 * stretch), int(1.25 * stretch))
        self.maxX, self.maxY, self.maxZ = worldSize, worldSize // 3, worldSize
        self.entities = [[[None for _ in range(self.maxZ)] for _ in range(self.maxY)] for _ in range(self.maxX)]
        
        treeSpawnX = random.randint(16, 24)
        treeSpawnZ = [random.randint(16, self.maxZ - 17) for _ in range(6)]
        
        for x in range(self.maxX):
            for z in range(self.maxZ):
                y = int(stretch * noise.pnoise2(x / scale, z / scale, octaves=4) + worldSize // 6)
                for i in range(y, -1, -1):
                    if y - i >= 4 or i <= worldSize // 12:
                        self.entities[x][i][z] = "stone"
                    elif i == y:
                        self.entities[x][i][z] = "grassBlock"
                    else:
                        self.entities[x][i][z] = "dirt"
                if x == worldSize // 2 and z == worldSize // 2:
                    self.players[0].camera.globalPosition[1] = y + 3
                elif x == treeSpawnX and z in treeSpawnZ:
                    self.generateTree(x, y + 1, z, y + random.randint(4, 8))
                    treeSpawnZ.remove(z)
                    if not treeSpawnZ:
                        treeSpawnX = min(x + random.randint(4, 10), self.maxX - 17)
                        treeSpawnZ = [random.randint(16, self.maxZ - 17) for _ in range(6)]
        
        return [self.entities, [self.maxX, self.maxY, self.maxZ, self.players[0].camera.globalPosition[1]]]

    def generateTree(self, x, y, z, treeTop):
        if y <= treeTop:
            self.generateTree(x, y + 1, z, treeTop)
            completion = treeTop - y
            if completion < 2:
                for i in range(-2, 3):
                    for j in range(-2, 3):
                        if not self.entities[x + i][y][z + j]:
                            if abs(i) != 2 or abs(j) != 2 or completion == 1:
                                self.entities[x + i][y][z + j] = "leaves"
                if completion == 0:
                    if not self.entities[x][y + 1][z]:
                        self.entities[x][y + 1][z] = "leaves"
                    if not self.entities[x + 1][y + 1][z]:
                        self.entities[x + 1][y + 1][z] = "leaves"
                    if not self.entities[x - 1][y + 1][z]:
                        self.entities[x - 1][y + 1][z] = "leaves"
                    if not self.entities[x][y + 1][z + 1]:
                        self.entities[x][y + 1][z + 1] = "leaves"
                    if not self.entities[x][y + 1][z - 1]:
                        self.entities[x][y + 1][z - 1] = "leaves"
            self.entities[x][y][z] = "log"

    def loadTerrain(self, loadingPacket):
        self.entities = loadingPacket[0]
        self.maxX, self.maxY, self.maxZ, self.players[0].camera.globalPosition[1] = loadingPacket[1]
