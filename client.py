import socket
import time
import json
from server import printTable

HOST = '127.0.0.1'
PORT = 60000
FORMAT = 'utf-8'
ADDRESS = (HOST, PORT)
def convertElementsToInt(data):
    for i in range(len(data)):
        data[i] = int(data[i])

def start_client():
    client_socket.connect(ADDRESS)
    PLAYER = int(client_socket.recv(1024).decode(FORMAT))

    print(client_socket.recv(1024).decode(FORMAT))
    table = json.loads(client_socket.recv(1024).decode(FORMAT))
    while table != "WIN!":
        printTable(table)
        
        turn = input("Please enter a column, and a row: ")
        turn = list(turn.split(' '))
        convertElementsToInt(turn)
        turn.append(PLAYER)

        client_socket.send(json.dumps(turn).encode(FORMAT))
        
        table = json.loads(client_socket.recv(1024).decode(FORMAT))
        time.sleep(0.5)

    if table == "WIN!":
        print("You won!")
    else:
        print("You lost!")
    input("Press 'Enter' to exit...")
    client_socket.close()
    print('\n[CLOSING CONNECTION] client closed socket!')


if __name__ == '__main__':
    IP = socket.gethostbyname(socket.gethostname())
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print('[CLIENT] started running')
    start_client()
    print('\n[CLIENT] connection lost')