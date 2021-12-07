# Imports
from checkWin import checkWinDiagNEtoSW, checkWinDiagSEtoNW, checkWinSides, checkWinDown
import socket
import sys
import threading
import json

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


# Run all checkWin functions on a given column and row.
def isWin(funcs, table, col, row, player):
    try:
        for func in funcs:
            if func(table, col, row, player):
                return True
        return False

    except IndexError as e:
        print(f'[ERROR] {e}')


# Print the table so the clients would be able to see the game board
def printTable(table):
    for line in table:
        for element in line:
            print(element, end='  ')
        print()



# Server code
def start_server():
    server_socket.bind(ADDRESS)

    print(f"[LISTENING] server is listening on {HOST}")
    server_socket.listen(5)
    while True:
        if threading.active_count() == 1:
            print('[ACTIVE CONNECTIONS] 0\n')

        connection, address = server_socket.accept()

        # if threading.active_count() - 1 == 0:
        #     thread = threading.Thread(target=handle_client1, args=(connection, address))
        #     thread.start()
        # else:
        #     thread = threading.Thread(target=handle_client2, args=(connection, address))
        #     thread.start()
        thread = threading.Thread(target=handle_client1, args=(connection, address))
        thread.start()


def handle_client1(conn, addr):
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
        conn.send(json.dumps(table).encode(FORMAT))
        data = [0, 0, 1]
        win = False
        while not win:
            data = json.loads(conn.recv(1024).decode(FORMAT))
            table[data[0]][data[1]] = data[2]
            win = isWin(checkWinFuncs, table, data[0], data[1], data[2])
            if win:
                conn.send(json.dumps("WIN!").encode(FORMAT))
            else:
                conn.send(json.dumps(table).encode(FORMAT))
        
        conn.send("WIN!".encode(FORMAT))
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