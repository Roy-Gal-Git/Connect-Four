# Imports
from checkWin import *
import socket, sys, threading, json, time


# Define constants
HOST = '127.0.0.1'
PORT = 60000
FORMAT = 'utf-8'
ADDRESS = (HOST, PORT)

# Setting up some functions and variables that the server would use to determine if a client won
table = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
]

checkWinFuncs = [checkWinDown, checkWinSides, checkWinDiagNEtoSW, checkWinDiagSEtoNW]


# Server code
def start_server():
    server_socket.bind(ADDRESS)

    print(f"[LISTENING] server is listening on {HOST}")
    server_socket.listen(5)
    while True:
        if threading.active_count() == 6:
            continue
        if threading.active_count() == 1:
            print('[ACTIVE CONNECTIONS] 0\n')

        connection, address = server_socket.accept()

        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()


def handle_client(conn, addr):
    table = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ]
    print(f'[CLIENT CONNECTED] on address {addr}')

    try:
        player = str(threading.active_count() -1)
        conn.send(player.encode(FORMAT))
        conn.send(f'Welcome to Connect-Four!\nYou\'re player #{player}.'.encode(FORMAT))
        time.sleep(0.2)
        difficulty = conn.recv(1024).decode(FORMAT)

        conn.send(json.dumps(table).encode(FORMAT))
        data = [0, 0, 1]
        win = False

        while not win:
            data = json.loads(conn.recv(1024).decode(FORMAT))
            table[data[0]][data[1]] = data[2]
            win = isWin(checkWinFuncs, table, data[0], data[1], data[2])
            if win:
                table = "WIN!"
                conn.send(json.dumps(table).encode(FORMAT))
                break

            

            if difficulty == '1':
                win = serverTurn(table, checkWinFuncs, conn, addr)
            else:
                win = serverTurnHardMode(table, checkWinFuncs, conn, addr, data[2])




        print(f'\n[CLIENT DISCONNECTED] on address: {addr}\n')

    except Exception as e:
        print(e)
        print(f'[CLIENT CONNECTION INTERRUPTED] on address: {addr}')


if __name__ == '__main__':
    IP = socket.gethostbyname(socket.gethostname())

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("[STARTING] server is starting...")
    start_server()

    print("[SHUTDOWN]")
