import pygame
import numpy as np
from Constants import *

class Engine3D:
    def __init__(self, players, objects):
        self.screen = pygame.display.set_mode([Global.WIDTH, Global.HEIGHT], pygame.DOUBLEBUF | pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.players = players
        self.objects = objects
        self.screenTransformation = self.getScreenTransformation()
        
    def render(self):
        self.screen.fill(Color.cyan)
        
        self.players[0].update()
        
        for obj in self.objects:
            obj.project(self.players[0].camera, self.screenTransformation, self.screen)
        for player in self.players[1:]:
            player.project(self.players[0].camera, self.screenTransformation, self.screen)
        
        pygame.draw.line(self.screen, Color.white, [Global.WIDTH / 2 - 10, Global.HEIGHT / 2], [Global.WIDTH / 2 + 10, Global.HEIGHT / 2])
        pygame.draw.line(self.screen, Color.white, [Global.WIDTH / 2, Global.HEIGHT / 2 - 10], [Global.WIDTH / 2, Global.HEIGHT / 2 + 10])
        
        pygame.display.update()
        self.clock.tick(60)
        
    def getScreenTransformation(self):
        return np.array([
            [Global.WIDTH / 2, 0, 0, 0],
            [0, -Global.HEIGHT / 2, 0, 0],
            [0, 0, 1, 0],
            [Global.WIDTH / 2, Global.HEIGHT / 2, 0, 1]
        ])