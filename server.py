# Imports
from checkWin import *
import socket, threading, time
from game import server_game

# Define constants
HOST = '127.0.0.1'
PORT = 60000
FORMAT = 'utf-8'
ADDRESS = (HOST, PORT)


# Prepares the server to start the game with all of the information it needs
def start_server():
    server_socket.bind(ADDRESS)

    print(f"[LISTENING] server is listening on {HOST}")

    server_socket.listen(5)

    connection_limit = 5
    
    while True:
        connected_clients = threading.active_count() - 1

        if threading.active_count() == 1:
            print('[ACTIVE CONNECTIONS] 0\n')

        connection, address = server_socket.accept()

        if connected_clients >= connection_limit:
            connection.send("Too many connections, Please try again later!".encode(FORMAT))
            connection.close()
            connected_clients -= 1
            continue
        
        try:
            thread = threading.Thread(target=handle_client, args=(connection, address))
            thread.start()

        except Exception as e:
            print("Too many connections! Please try again later.")
            continue


# Handles the connection between the client and the server
def handle_client(conn, addr):
    print(f'[CLIENT CONNECTED] on address {addr}')

    try:
        player = str(threading.active_count() -1)
        conn.send(f'Welcome to Connect-Four!\nYou\'re player #{player}.'.encode(FORMAT))
        time.sleep(0.2)
        conn.send(player.encode(FORMAT))
        time.sleep(0.2)
        difficulty = conn.recv(1024).decode(FORMAT)
        num_of_wins = conn.recv(1024).decode(FORMAT)
        game = { 'total': int(num_of_wins), 'server': 0, 'player': 0 , 'turns': 0}

        while True:
            table = [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]
            ]

            game = server_game(conn, addr, table, difficulty, game)
            if game['server'] == game['total'] or game['player'] == game['total']:
                break

    except Exception as e:
        print(e)
        print(f'[CLIENT CONNECTION INTERRUPTED] on address: {addr}')


if __name__ == '__main__':
    IP = socket.gethostbyname(socket.gethostname())

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("[STARTING] server is starting...")
    start_server()

    print("[SHUTDOWN]")
