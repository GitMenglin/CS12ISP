import socket
import pickle
import threading

def handleClient(connection, playerId):
    while True:
        try:
            players.append(pickle.loads(connection.recv(1024)))
            print(f"{players[playerId][0]}(Player{playerId + 1}) connected!")
            break
        except:
            continue
    connection.settimeout(0.05)
    while True:
        try:
            playerCount = len(players)
            connection.sendall(pickle.dumps(playerCount))
            players[playerId] = pickle.loads(connection.recv(1024 * 5))
            for i in range(playerCount):
                if i != playerId:
                    connection.sendall(pickle.dumps(players[i]))
        except ConnectionError:
            break
        except Exception as e:
            if debug:
                print(f"{type(e)}: {e}")
    print(f"{players[playerId][0]}(Player{playerId + 1}) disconnected!")
    connection.close()

debug = True

ip = socket.gethostbyname(socket.gethostname())
port = 1234
serverAddress = (ip, port)
print(serverAddress)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(serverAddress)
server.listen()
playerId = 0
players = []
while True:
    connection, address = server.accept()
    threading.Thread(target=handleClient, args=(connection, playerId)).start()
    playerId += 1
