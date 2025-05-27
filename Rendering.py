import pygame
import numpy as np
from Constants import *

class Engine3D:
    def __init__(self, players, entities):
        self.screen = pygame.display.set_mode([Global.WIDTH, Global.HEIGHT], pygame.DOUBLEBUF | pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.players = players
        self.entities = entities
        self.screenTransformation = self.getScreenTransformation()
        
    def render(self):
        self.screen.fill(Color.cyan)
        
        self.players[0].update()
        
        self.project()
                
        pygame.draw.line(self.screen, Color.white, [Global.WIDTH / 2 - 10, Global.HEIGHT / 2], [Global.WIDTH / 2 + 10, Global.HEIGHT / 2])
        pygame.draw.line(self.screen, Color.white, [Global.WIDTH / 2, Global.HEIGHT / 2 - 10], [Global.WIDTH / 2, Global.HEIGHT / 2 + 10])
        
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

    def arrangeEntities(self):
        entitiesArrangement = [[self.entities[0], self.entities[0].getTransformedCenter(self.players[0].camera)[2]]]
        for entity in self.entities:
            entitiesArranged = []
            inserted = False
            currentCenterZ = entity.getTransformedCenter(self.players[0].camera)[2]
            for arranged in entitiesArrangement:
                if currentCenterZ > arranged[1] and not inserted:
                    entitiesArranged.append([entity, currentCenterZ])
                    inserted = True
                entitiesArranged.append(arranged)
            if not inserted:
                entitiesArranged.append([entity, currentCenterZ])
            entitiesArrangement = entitiesArranged
        return entitiesArrangement

    def arrangePlayers(self):
        if len(self.players) > 1:
            playersArrangement = [[self.players[1], self.players[1].getTransformedPosition(self.players[0].camera)[2]]]
            playerCount = 0
            for player in self.players[1:]:
                playersArranged = []
                inserted = False
                currentPositionZ = player.getTransformedPosition(self.players[0].camera)[2]
                for arranged in playersArrangement:
                    if currentPositionZ > arranged[1] and not inserted:
                        playersArranged.append([player, currentPositionZ])
                        inserted = True
                    playersArranged.append(arranged)
                if not inserted: 
                    playersArranged.append([player, currentPositionZ])
                playersArrangement = playersArranged
                playerCount += 1
            return [playersArrangement, playerCount]
        else:
            return [[], 0]

    def getScreenTransformation(self):
        return np.array([
            [Global.WIDTH / 2, 0, 0, 0],
            [0, -Global.HEIGHT / 2, 0, 0],
            [0, 0, 1, 0],
            [Global.WIDTH / 2, Global.HEIGHT / 2, 0, 1]
        ])
