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
    subprocess.call([sys.executable, "-m", "pip", "install", "pygame"])
try:
    import numpy as np
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", "numpy"])


def main():
    ip = socket.gethostbyname(socket.gethostname())
    port = 1234
    address = (ip, port)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(address)
    # name = input("Enter your name: ")
    name = "Steve"
    paused = False
    escCoolDownStart = 0
    
    pygame.init()
    pygame.mouse.set_visible(paused)
    players = [Player()]
    entities = [Block(Geometry.cube, [i, 0, j, 0]) for j in range(10) for i in range(10)]
    engine = Engine3D(players, entities)
    
    client.sendall(pickle.dumps([name, np.append(players[0].globalPosition[:3], 1), players[0].camera.pitch, players[0].camera.yaw, engine.synchronization]))
    client.settimeout(0.05)
    
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
        try:
            playerCount = pickle.loads(client.recv(20))
            while playerCount > len(players):
                players.append(Player())
            client.sendall(pickle.dumps([name, np.append(players[0].globalPosition[:3], 1), players[0].camera.pitch, players[0].camera.yaw, engine.synchronization]))
            for i in range(playerCount - 1):
                raw = pickle.loads(client.recv(1024 * 5))
                if isinstance(raw, list):
                    players[i + 1].name, players[i + 1].globalPosition, players[i + 1].camera.pitch, players[i + 1].camera.yaw, synchronization = raw
                    if synchronization is not None:
                        try:
                            engine.entities.pop(int(synchronization))
                            print("excavated")
                        except IndexError:
                            engine.entities.pop(int(synchronization) - 1)
                            print("excavated")
                        except TypeError:
                            engine.entities.append(Block(Geometry.cube, synchronization))
                            print("placed")
        except Exception as e:
            print(f"{type(e)}: {e}")
        
        if pygame.key.get_pressed()[pygame.K_ESCAPE] and pygame.time.get_ticks() - escCoolDownStart > 200:
            paused = not paused
            pygame.mouse.set_visible(paused)
            escCoolDownStart = pygame.time.get_ticks()
        pygame.display.set_caption(f"{name}: {[int(coordinate) for coordinate in players[0].globalPosition[:3]]}")
        engine.render(paused)
        
    client.close()
    pygame.quit()

main()
