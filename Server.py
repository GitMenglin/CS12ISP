import socket
import pickle
import zlib
import threading
import time

class Server:
    def __init__(self):
        self.debug = False
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 1234
        self.serverAddress = (self.ip, self.port)
        print(self.serverAddress)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.serverAddress)
        self.server.listen()
        self.playerId = 0
        self.players = []
        self.loadingPacket = None

    def run(self): 
        while True:
            connection, address = self.server.accept()
            threading.Thread(target=self.handleClient, args=(connection, self.playerId)).start()
            self.playerId += 1

    def send(self, connection, data):
        compressed = zlib.compress(pickle.dumps(data))
        connection.sendall(len(compressed).to_bytes(4))
        connection.sendall(compressed)

    def receive(self, connection):
        size = connection.recv(4)
        if not size:
            return None
        size = int.from_bytes(size)
        
        compressed = b""
        while len(compressed) < size:
            data = connection.recv(size - len(compressed))
            if not data:
                return None
            compressed += data
        return pickle.loads(zlib.decompress(compressed))

    def handleClient(self, connection, playerId):
        self.send(connection, len(self.players))
        self.players.append(self.receive(connection))
        print(f"{self.players[playerId][0]}(Player{playerId + 1}) connected!")
        if len(self.players) == 1:
            self.loadingPacket = self.receive(connection)
        else:
            while not self.loadingPacket:
                time.sleep(0.01)
            self.send(connection, self.loadingPacket)
        connection.settimeout(1.0)
        while True:
            try:
                playerCount = len(self.players)
                self.send(connection, playerCount)
                done = self.receive(connection)
                if isinstance(done, bool) and done:
                    self.players[playerId] = None
                    break
                self.players[playerId] = self.receive(connection)
                if isinstance(self.players[playerId], list) and len(self.players[playerId]) == 7:
                    if isinstance(self.players[playerId][-1], list):
                        x, y, z = self.players[playerId][-1][1]
                        self.loadingPacket[0][x][y][z] = self.players[playerId][-1][0]
                for i in range(playerCount):
                    if i != playerId:
                        self.send(connection, self.players[i])
            except ConnectionError:
                break
            except Exception as e:
                if self.debug:
                    print(f"{type(e)}: {e}")
        connection.close()
        print(f"{self.players[playerId][0]}(Player{playerId + 1}) disconnected!")

Server().run()
