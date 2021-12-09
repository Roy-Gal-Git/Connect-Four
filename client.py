import socket, time, json
from colors import *
from checkWin import printTable, columnIndexByRow, coloredPrint

HOST = '127.0.0.1'
PORT = 60000
FORMAT = 'utf-8'
ADDRESS = (HOST, PORT)


# Checks if the input is a valid row
def validInput(row):
    if not row.isnumeric():
        return False
    row = int(row) - 1

    if row < 0 or row > 6:
        return False

    return True


# Gets the row input from the user
def getRow(table):
    row = input("Please pick a row: ")

    while not validInput(row):
        coloredPrint("\n[ERROR] Row not in range! (1-7)", RED)
        printTable(table)
        row = input("Please pick a row: ")

    return int(row) - 1


def start_client():
    try:
        client_socket.connect(ADDRESS)
        PLAYER = int(client_socket.recv(1024).decode(FORMAT))
        
        print("\n" + client_socket.recv(1024).decode(FORMAT))

        table = json.loads(client_socket.recv(1024).decode(FORMAT))
        
        while True:
            tableCopy = table
            printTable(table)
            row = getRow(table)

            col = columnIndexByRow(table, row)
            turn = [col, row, PLAYER]

            client_socket.send(json.dumps(turn).encode(FORMAT))
            
            table = json.loads(client_socket.recv(1024).decode(FORMAT))
            
            tableCopy[col][row] = PLAYER
            
            if table == "WIN!":
                printTable(tableCopy)
                print("You won!")
                break

            elif table == "YOU LOST!":
                tableCopy = json.loads(client_socket.recv(1024).decode(FORMAT))
                printTable(tableCopy)
                print("You lost!")
                break

            time.sleep(0.5)
        
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