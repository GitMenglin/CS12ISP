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
        
    def render(self, paused):
        self.screen.fill(cyan)
        self.players[0].update(paused)
        self.project()
        
        pygame.display.update()
        self.clock.tick(60)

    def project(self):
        Block.target = None
        Block.targetFaceNormal = None
        entitiesArrangement = self.arrangeEntities()
        playersArrangement, playerCount = self.arrangePlayers()
        
        playerRendered = 0
        for entity in entitiesArrangement:
            while (playerRendered < playerCount and 
                   playersArrangement[playerRendered][1] > entity[1]):
                playersArrangement[playerRendered][0].project(self.players[0].camera, self.screen)
                playerRendered += 1
            entity[0].project(self.screen)
        while playerRendered < playerCount:
            playersArrangement[playerRendered][0].project(self.players[0].camera, self.screen)
            playerRendered += 1
        
        pygame.draw.line(self.screen, white, [WIDTH / 2 - 10, HEIGHT / 2], [WIDTH / 2 + 10, HEIGHT / 2])
        pygame.draw.line(self.screen, white, [WIDTH / 2, HEIGHT / 2 - 10], [WIDTH / 2, HEIGHT / 2 + 10])
        
        if Block.target is not None:
            Block.target[0].selected = True
            if not pygame.mouse.get_pressed()[0]:
                self.excavateStart = pygame.time.get_ticks()
            elif pygame.mouse.get_pressed()[0] and pygame.time.get_ticks() - self.excavateStart > 1000:
                self.entities.remove(Block.target[0])
                self.excavateStart = pygame.time.get_ticks()
            if pygame.mouse.get_pressed()[2]:
                if pygame.time.get_ticks() - self.coolDownStart > 200:
                    self.placeBlock(Block.target[0])
                self.coolDownStart = pygame.time.get_ticks()
        else:
            self.excavateStart = pygame.time.get_ticks()

    def placeBlock(self, target):
        placement = target.placement + Block.targetFaceNormal[0]
        
        # temporary
        for entity in self.entities:
            if placement[0] == entity.placement[0] and placement[1] == entity.placement[1] and placement[2] == entity.placement[2]:
                return
        self.entities.append(Block(Geometry.cube, [*placement]))

    def arrangeEntities(self):
        entitiesArrangement = [[self.entities[0], self.entities[0].getArrangementValue(self.players[0].camera)]]
        for entity in self.entities[1:]:
            entitiesArranged = []
            inserted = False
            arrangementValue = entity.getArrangementValue(self.players[0].camera)
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
