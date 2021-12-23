import socket, time
from colors import *
from checkWin import coloredPrint
from game import client_game

HOST = '127.0.0.1'
PORT = 60000
FORMAT = 'utf-8'
ADDRESS = (HOST, PORT)


def start_client():
    try:
        start_time = time.time()

        client_socket.connect(ADDRESS)

        PLAYER = int(client_socket.recv(1024).decode(FORMAT))
    
        print("\n" + client_socket.recv(1024).decode(FORMAT))

        wants_to_play = input(f'\nMenu:\n1. Exit\n2. Play\n>>> [Player {PLAYER}]: ')
        while wants_to_play != '1' and wants_to_play != '2':
            coloredPrint('\n[ERROR] Invalid input!', RED)
            wants_to_play = input(f'\nMenu:\n1. Exit\n2. Play\n>>> [Player {PLAYER}]: ')
        if wants_to_play == '1':
            print('\n[EXIT...]')
            time.sleep(1)
            return

        difficulty = input(f'\nMode:\n1. Easy\n2. Hard\n>>> [Player {PLAYER}]: ')
        while difficulty != '1' and difficulty != '2':
            coloredPrint('\n[ERROR] Invalid input!', RED)
            difficulty = input(f'\nMode:\n1. Easy\n2. Hard\n>>> [Player {PLAYER}]: ')

        client_socket.send(difficulty.encode(FORMAT))
        
        num_of_wins = input(f'\nPlease choose a number of wins for a player to win the game\n>>> [Player {PLAYER}]: ')
        while not num_of_wins.isnumeric() or int(num_of_wins) <= 0:
            coloredPrint('\n[ERROR] Invalid input!', RED)
            num_of_wins = input(f'\nPlease choose a number of wins for a player to win the game\n>>> [Player {PLAYER}]: ')

        client_socket.send(num_of_wins.encode(FORMAT))

        while True:
            game = client_game(client_socket, PLAYER)
            print(f"\nResults:\n\
                \nPlayer: {game['player']}\
                \nServer: {game['server']}")
                
            if game['server'] == game['total']:
                print(f"Rounds: {game['server'] + game['player']}\nTurns: {game['turns']}\nTotal time played (Hours/Minutes/Seconds): {(time.time() - start_time) % 3600}::{(time.time() - start_time) % 60}::{time.time() - start_time}")
                coloredPrint('\nYou lost the game! Good luck next time :)\n', MAGENTA)
                break
            
            if game['player'] == game['total']:
                print(f"Total rounds played: {game['server'] + game['player']}\nTotal turns played: {game['turns']}\nTotal time played (Hours/Minutes/Seconds): {round(time.time() - start_time) // 3600}::{round(time.time() - start_time) // 60}::{round(time.time() - start_time) % 60}")
                coloredPrint('\nYou won the game! Hurray!\n', MAGENTA)
                break

    except Exception as e:
        print(e)

    
    input("Press 'Enter' to exit...")
    client_socket.close()
    print('\n[CLOSING CONNECTION] client closed socket!')


if __name__ == '__main__':
    IP = socket.gethostbyname(socket.gethostname())
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print('[CLIENT] started running')
    start_client()
    print('\n[CLIENT] connection lost')