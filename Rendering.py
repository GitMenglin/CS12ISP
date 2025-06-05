import pygame
from Entity import Block
from GeometryLib import Geometry
from Constants import *

class Engine3D:
    def __init__(self, players, entities):
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.DOUBLEBUF | pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.players = players
        self.entities = entities
        self.excavateStart = 0
        self.coolDownStart = 0
        self.synchronization = None
        
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
                self.synchronization = self.entities.index(Block.target[0])
                self.entities.pop(self.synchronization)
                self.excavateStart = pygame.time.get_ticks()
            if pygame.mouse.get_pressed()[2]:
                if pygame.time.get_ticks() - self.coolDownStart > 200:
                    self.placeBlock(Block.target)
                self.coolDownStart = pygame.time.get_ticks()
        else:
            self.excavateStart = pygame.time.get_ticks()
        
        playerRendered = 0
        self.players[0].collided = False
        for entity in entitiesArrangement:
            while (playerRendered < playerCount and 
                   playersArrangement[playerRendered][1] > entity[1]):
                playersArrangement[playerRendered][0].project(self.players[0].camera, self.screen)
                playerRendered += 1
            entity[0].project(self.screen)
            if abs(entity[0].cameraSpaceCenter[0]) <= 0.75 and abs(entity[0].cameraSpaceCenter[2]) <= 0.75:
                self.players[0].checkCollision(entity[0])
        while playerRendered < playerCount:
            playersArrangement[playerRendered][0].project(self.players[0].camera, self.screen)
            playerRendered += 1
        
        pygame.draw.line(self.screen, white, [WIDTH / 2 - 10, HEIGHT / 2], [WIDTH / 2 + 10, HEIGHT / 2])
        pygame.draw.line(self.screen, white, [WIDTH / 2, HEIGHT / 2 - 10], [WIDTH / 2, HEIGHT / 2 + 10])

    def placeBlock(self, target):
        placement = target[0].placement + Block.normalsArranged[target[1]]
        for entity in self.entities:
            if placement[0] == entity.placement[0] and placement[1] == entity.placement[1] and placement[2] == entity.placement[2]:
                return
        self.entities.append(Block(Geometry.cube, placement))
        self.synchronization = placement

    def arrangeEntities(self):
        entitiesArrangement = [[self.entities[0], self.entities[0].preprocess(self.players[0].camera)]]
        for entity in self.entities[1:]:
            entitiesArranged = []
            inserted = False
            arrangementValue = entity.preprocess(self.players[0].camera)
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
