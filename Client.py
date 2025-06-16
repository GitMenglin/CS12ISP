import socket
import pickle
import zlib
import subprocess
import sys
from GeometryLib import Geometry
from Player import Player
from Entity import *
from Rendering import Engine3D
from Constants import *
try:
    import pygame
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", "pygame"])
try:
    import numpy as np
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", "numpy"])
try:
    import noise
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", "noise"])

def send(client, data):
    compressed = zlib.compress(pickle.dumps(data))
    client.sendall(len(compressed).to_bytes(4))
    client.sendall(compressed)

def receive(client):
    size = client.recv(4)
    if not size:
        return None
    size = int.from_bytes(size)
    
    compressed = b""
    while len(compressed) < size:
        data = client.recv(size - len(compressed))
        if not data:
            return None
        compressed += data
    return pickle.loads(zlib.decompress(compressed))

def main():
    ip = socket.gethostbyname(socket.gethostname())
    port = 1234
    address = (ip, port)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(address)
        name = input("Enter your name: ")
    except:
        name = "Herobrine"
    paused = False
    escCoolDownStart = 0
    
    pygame.init()
    pygame.mouse.set_visible(paused)
    players = [Player()]
    engine = Engine3D(players)
    
    try:
        playerCount = receive(client)
        if isinstance(playerCount, int):
            while playerCount > len(players):
                players.append(Player())
        send(client, [name, np.append(players[0].globalPosition[:3], 1), players[0].camera.pitch, players[0].camera.yaw, players[0].swing, players[0].geometry, engine.synchronization])
        if playerCount == 0:
            send(client, engine.generateTerrain())
        else:
            engine.loadTerrain(receive(client))
        client.settimeout(0.01)
    except Exception as e:
        if debug:
            print(f"{type(e)}: {e}")
        engine.generateTerrain()
    
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        try:
            playerCount = receive(client)
            if isinstance(playerCount, int):
                while playerCount > len(players):
                    players.append(Player())
                send(client, [name, np.append(players[0].globalPosition[:3], 1), players[0].camera.pitch, players[0].camera.yaw, players[0].swing, players[0].geometry, engine.synchronization])
                for i in range(playerCount - 1):
                    data = receive(client)
                    if isinstance(data, list) and len(data) == 7:
                        players[i + 1].name, players[i + 1].globalPosition, players[i + 1].camera.pitch, players[i + 1].camera.yaw, players[i + 1].swing, players[i + 1].geometry, synchronization = data
                        if isinstance(synchronization, list):
                            x, y, z = synchronization[1]
                            blockType = synchronization[0]
                            if blockType:
                                engine.entities[x][y][z] = BlockPool.acquire(Geometry.blocks[blockType], synchronization[1])
                            else:
                                BlockPool.release(engine.entities[x][y][z])
                                engine.entities[x][y][z] = None
                    else:
                        break
        except Exception as e:
            if debug:
                print(f"{type(e)}: {e}")
        
        if pygame.key.get_pressed()[pygame.K_ESCAPE] and pygame.time.get_ticks() - escCoolDownStart > 200:
            paused = not paused
            pygame.mouse.set_visible(paused)
            escCoolDownStart = pygame.time.get_ticks()
        playerCoords = [round(coordinate.item()) for coordinate in players[0].globalPosition[:3]]
        pygame.display.set_caption(f"{name}: {playerCoords}\tFPS: {round(engine.clock.get_fps())}")
        engine.render(paused)
        
    client.close()
    pygame.quit()

main()
