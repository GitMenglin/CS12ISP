import socket
import pickle
import zlib
import subprocess
import sys
import cProfile
import pstats
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

def gameLoop(engine, client, multiplayer, name):
    pygame.mouse.set_visible(engine.paused)
    escCoolDownStart = 0
    pygame.mouse.get_rel()
    while not engine.done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or engine.players[0].globalPosition[1] < -16 or engine.reconnect:
                engine.done = True
        
        if multiplayer:
            try:
                playerCount = receive(client)
                if isinstance(playerCount, int):
                    while playerCount > len(engine.players):
                        engine.players.append(Player())
                    while playerCount < len(engine.players):
                        engine.players.pop()
                    send(client, engine.done)
                    send(client, [name, np.array([*engine.players[0].globalPosition[:3], 1.]), engine.players[0].camera.pitch, engine.players[0].camera.yaw, engine.players[0].swing, engine.players[0].currentSkin, engine.synchronization])
                    for i in range(playerCount - 1):
                        data = receive(client)
                        if isinstance(data, list) and len(data) == 7:
                            engine.players[i + 1].name, engine.players[i + 1].globalPosition, engine.players[i + 1].camera.pitch, engine.players[i + 1].camera.yaw, engine.players[i + 1].swing, engine.players[i + 1].currentSkin, synchronization = data
                            if isinstance(synchronization, list):
                                x, y, z = synchronization[1]
                                blockType = synchronization[0]
                                if blockType:
                                    engine.entities[x][y][z] = blockType
                                else:
                                    engine.entities[x][y][z] = None
                        else:
                            break
            except Exception as e:
                if debug:
                    print(f"{type(e)}: {e}")
        
        keyPressed = pygame.key.get_pressed()
        if keyPressed[pygame.K_ESCAPE] and pygame.time.get_ticks() - escCoolDownStart > 200:
            engine.paused = not engine.paused
            pygame.mouse.set_visible(engine.paused)
            escCoolDownStart = pygame.time.get_ticks()
        playerCoords = [round(coordinate.item()) for coordinate in engine.players[0].globalPosition[:3]]
        pygame.display.set_caption(f"{name}: {playerCoords}\tFPS: {round(engine.clock.get_fps())}")
        engine.render(keyPressed)
    if engine.reconnect:
        return True
    client.close()
    pygame.quit()

def menu(engine):
    ip = socket.gethostbyname(socket.gethostname())
    port = 1234
    address = (ip, port)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    engine.screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
    engine.clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 30)
    multiplayer = True
    
    pygame.display.set_caption("Attempting to connect to the server...")
    try:
        client.connect(address)
        pygame.display.set_caption("Server connection successful! :)")
    except:
        multiplayer = False
        pygame.display.set_caption("Server connection failed! Switching to single-player mode...")
    
    name = ""
    nameConfirmed = False
    steve = pygame.sprite.Sprite()
    steve.image = pygame.Surface([100, 100])
    steve.image.fill(green)
    steve.rect = steve.image.get_rect(center=[WIDTH//3, 2*HEIGHT//3])
    alex = pygame.sprite.Sprite()
    alex.image = pygame.Surface([100, 100])
    alex.image.fill(green)
    alex.rect = alex.image.get_rect(center=[2*WIDTH//3, 2*HEIGHT//3])
    skinGroup = pygame.sprite.Group([steve, alex])
    skin = None
    while (not nameConfirmed or not skin) and not engine.done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                engine.done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    nameConfirmed = True
                elif not nameConfirmed:
                    name += event.unicode
        
        x, y = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed()
        if steve.rect.collidepoint(x, y) or skin == "steve":
            steve.image.fill(yellow)
            if mousePressed[0]:
                skin = "steve"
        else:
            steve.image.fill(green)
        if alex.rect.collidepoint(x, y) or skin == "alex":
            alex.image.fill(yellow)
            if mousePressed[0]:
                skin = "alex"
        else:
            alex.image.fill(green)
        
        engine.screen.fill(void)
        skinGroup.draw(engine.screen)
        engine.screen.blit(font.render("Steve", True, blue), [WIDTH//3 - 7.5 * 5, 2*HEIGHT//3 - 20])
        engine.screen.blit(font.render("Alex", True, blue), [2*WIDTH//3 - 7.5 * 4, 2*HEIGHT//3 - 20])
        engine.screen.blit(font.render(text := "Type in your player name", True, blue), [WIDTH//2 - 7.5 * len(text), HEIGHT//3 - 30])
        engine.screen.blit(font.render(name, True, blue, green), [WIDTH//2 - 7.5 * len(name), HEIGHT//3 + 30])
        pygame.display.update()
        engine.clock.tick(40)
    if engine.done:
        client.close()
        pygame.quit()
        return False
    else:
        engine.players = [Player(skin=skin)]
        if multiplayer:
            try:
                playerCount = receive(client)
                if isinstance(playerCount, int):
                    while playerCount > len(engine.players):
                        engine.players.append(Player())
                send(client, [name, np.array([*engine.players[0].globalPosition[:3], 1.]), engine.players[0].camera.pitch, engine.players[0].camera.yaw, engine.players[0].swing, engine.players[0].currentSkin, engine.synchronization])
                if playerCount == 0:
                    send(client, engine.generateTerrain())
                else:
                    engine.loadTerrain(receive(client))
                client.settimeout(0.05)
            except Exception as e:
                if debug:
                    print(f"{type(e)}: {e}")
        else:
            engine.generateTerrain()
        return gameLoop(engine, client, multiplayer, name)

def main():
    pygame.init()
    while menu(Engine3D()):
        pass

if profile:
    profiler = cProfile.Profile()
    profiler.enable()
    
    main()
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumtime')
    stats.print_stats()
else:
    main()
