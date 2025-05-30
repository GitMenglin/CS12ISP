import socket
import pickle
import subprocess
import sys
from GeometryLib import Geometry
from Player import Player
from Entity import *
from Rendering import Engine3D

try:
    import pygame
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])

try:
    import numpy as np
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])

def main():
    ip = socket.gethostbyname(socket.gethostname())
    port = 1234
    address = (ip, port)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(address)
    # name = input("Enter your name: ")
    name = "Steve"
    
    pygame.init()
    players = [Player()]
    entities = [Block(Geometry.cube, [i, 0, j]) for j in range(10) for i in range(10)]
    engine = Engine3D(players, entities)
    
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
