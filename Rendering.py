import pygame
import numpy as np
from Constants import *

class Engine3D:
    def __init__(self, players, entities):
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.DOUBLEBUF | pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.players = players
        self.entities = entities
        self.screenTransformation = self.getScreenTransformation()
        
    def render(self):
        self.screen.fill(cyan)
        self.players[0].update()
        self.project()
        
        pygame.display.update()
        self.clock.tick(60)

    def project(self):
        entitiesArrangement = self.arrangeEntities()
        playersArrangement, playerCount = self.arrangePlayers()
        
        playerRendered = 0
        for entity in entitiesArrangement:
            while (playerRendered < playerCount and 
                   playersArrangement[playerRendered][1] > entity[1]):
                playersArrangement[playerRendered][0].project(self.players[0].camera, self.screenTransformation, self.screen)
                playerRendered += 1
            entity[0].project(self.players[0].camera, self.screenTransformation, self.screen)
        while playerRendered < playerCount:
            playersArrangement[playerRendered][0].project(self.players[0].camera, self.screenTransformation, self.screen)
            playerRendered += 1
            
        pygame.draw.line(self.screen, white, [WIDTH / 2 - 10, HEIGHT / 2], [WIDTH / 2 + 10, HEIGHT / 2])
        pygame.draw.line(self.screen, white, [WIDTH / 2, HEIGHT / 2 - 10], [WIDTH / 2, HEIGHT / 2 + 10])

    def arrangeEntities(self):
        entitiesArrangement = [[self.entities[0], self.entities[0].getArrangementValue(self.players[0].camera)]]
        for entity in self.entities:
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

    def getScreenTransformation(self):
        return np.array([
            [WIDTH / 2, 0, 0, 0],
            [0, -HEIGHT / 2, 0, 0],
            [0, 0, 1, 0],
            [WIDTH / 2, HEIGHT / 2, 0, 1]
        ])
