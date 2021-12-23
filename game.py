from checkWin import *

checkWinFuncs = [checkWinDown, checkWinSides, checkWinDiagNEtoSW, checkWinDiagSEtoNW]


def client_game(client_socket, PLAYER):
    table = json.loads(client_socket.recv(1024).decode(FORMAT))
    time.sleep(0.2)
    game = json.loads(client_socket.recv(1024).decode(FORMAT))
    
    while True:
        tableCopy = table
        printTable(table)

        row = getRow(table)
        col = columnIndexByRow(table, row)
        

        while col == -1:
            coloredPrint('\n[ERROR] IndexError: OUT OF BOUNDS!', RED)

            printTable(table)

            row = getRow(table)
            col = columnIndexByRow(table, row)


        turn = [col, row, PLAYER]

        client_socket.send(json.dumps(turn).encode(FORMAT))
        
        table = json.loads(client_socket.recv(1024).decode(FORMAT))
        time.sleep(0.2)

        tableCopy[col][row] = PLAYER
        
        if table == "WIN!":
            game = json.loads(client_socket.recv(1024).decode(FORMAT))
            printTable(tableCopy)
            coloredPrint("You won this round!", GREEN)
            return game

        elif table == "YOU LOST!":
            tableCopy = json.loads(client_socket.recv(1024).decode(FORMAT))
            time.sleep(0.2)
            game = json.loads(client_socket.recv(1024).decode(FORMAT))

            printTable(tableCopy)
            coloredPrint("You lost this round!", RED)
            return game

        game = json.loads(client_socket.recv(1024).decode(FORMAT))

        time.sleep(0.5)



def server_game(conn, addr, table, difficulty, game):
    conn.send(json.dumps(table).encode(FORMAT))
    time.sleep(0.2)
    conn.send(json.dumps(game).encode(FORMAT))
    
    data = [0, 0, 1]
    win = False

    while not win:
        game['turns'] += 1
        data = json.loads(conn.recv(1024).decode(FORMAT))
        table[data[0]][data[1]] = data[2]
        win = isWin(checkWinFuncs, table, data[0], data[1], data[2])
        if win:
            table = "WIN!"
            game['player'] += 1
            conn.send(json.dumps(table).encode(FORMAT))
            time.sleep(0.2)
            conn.send(json.dumps(game).encode(FORMAT))
            return game

        

        if difficulty == '1':
            win = serverTurn(table, checkWinFuncs, conn, game)
            if win:
                return game
        else:
            win = serverTurnHardMode(table, checkWinFuncs, conn, data[2], game)
            if win:
                return game




    print(f'\n[CLIENT DISCONNECTED] on address: {addr}\n')


# Easy Mode
def serverTurn(table, checkWinFuncs, conn, game):
    game['turns'] += 1
    row = random.randint(0, 6)
    col = columnIndexByRow(table, row)

    while col == -1:
        row = random.randint(0, 6)
        col = columnIndexByRow(table, row)

    table[col][row] = SERVER_PLAYER
    win = isWin(checkWinFuncs, table, col, row, SERVER_PLAYER)

    if win:
        game['server'] += 1
        conn.send(json.dumps("YOU LOST!").encode(FORMAT))
        time.sleep(0.2)
        conn.send(json.dumps(table).encode(FORMAT))
        time.sleep(0.2)
        conn.send(json.dumps(game).encode(FORMAT))

    else:
        conn.send(json.dumps(table).encode(FORMAT))
        time.sleep(0.2)
        conn.send(json.dumps(game).encode(FORMAT))


    return win


# Hard mode
def serverTurnHardMode(table, checkWinFuncs, conn, player, game):
    game['turns'] += 1

    for row in range(7):
        col = columnIndexByRow(table, row)
        if isWin(checkWinFuncs, table, col, row, SERVER_PLAYER):
            table[col][row] = SERVER_PLAYER
            game['server'] += 1
            conn.send(json.dumps("YOU LOST!").encode(FORMAT))
            time.sleep(0.2)
            conn.send(json.dumps(table).encode(FORMAT))
            time.sleep(0.2)
            conn.send(json.dumps(game).encode(FORMAT))
            return True
                
        if col == -1:
            continue

    for row in range(7):
        col = columnIndexByRow(table, row)
        if isWin(checkWinFuncs, table, col, row, player):
            table[col][row] = SERVER_PLAYER
            conn.send(json.dumps(table).encode(FORMAT))
            time.sleep(0.2)
            conn.send(json.dumps(game).encode(FORMAT))
            return
                
        if col == -1:
            continue
    
    row = random.randint(0, 6)
    col = columnIndexByRow(table, row)

    while not col:
        row = random.randint(0, 6)
        col = columnIndexByRow(table, row)

    table[col][row] = SERVER_PLAYER
    conn.send(json.dumps(table).encode(FORMAT))
    time.sleep(0.2)
    conn.send(json.dumps(game).encode(FORMAT))
