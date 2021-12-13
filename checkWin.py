import random, json, os, sys, time
from colors import *

ROWMAX = 7
COLMAX = 6
FORMAT = 'utf-8'
SERVER_PLAYER = 7


# Checks if there's a win on the sides
def checkWinSides(table, col, row, player):
    direction = 'right'
    counter = 1
    row += 1

    for i in range(5):
        if counter == 4:
            return True

        if row >= ROWMAX:
            direction = 'left'
            row -= counter + 1

        if table[col][row] == player and direction == 'right':
            counter += 1
            row += 1

        elif table[col][row] != player and direction == 'right':
            direction = 'left'
            row -= counter + 1

        elif table[col][row] == player and direction == 'left':
            counter += 1
            row -= 1

        elif table[col][row] != player and direction == 'left':
            return False


# Checks if there's a win downwards
def checkWinDown(table, col, row, player):
    counter = 1
    col += 1

    for i in range(5):
        if counter == 4:
            return True

        if col >= COLMAX:
            return False

        if table[col][row] == player:
            counter += 1
            col += 1

        else:
            return False


# Checks if there's a win diagonally from South-East to North-West
def checkWinDiagSEtoNW(table, col, row, player):
    direction = 'se'
    counter = 1
    col += 1
    row += 1
    for i in range(5):
        if counter == 4:
            return True

        if direction == 'se':
            result = checkSE(table, col, row, player, direction, counter)
            if result:
                col = result[0]
                row = result[1]
                direction = result[2]
                counter = result[3]
            else:
                return False

        else:
            result = checkNW(table, col, row, player, direction, counter)
            if result:
                col = result[0]
                row = result[1]
                direction = result[2]
                counter = result[3]
            else:
                return False
        

# Checks if there's a win diagonally from North-East to South-West
def checkWinDiagNEtoSW(table, col, row, player):
    direction = 'ne'
    counter = 1
    col -= 1
    row += 1

    for i in range(5):
        if counter == 4:
            return True

        if direction == 'ne':
            result = checkNE(table, col, row, player, direction, counter)
            if result:
                col = result[0]
                row = result[1]
                direction = result[2]
                counter = result[3]
            else:
                return False
        
        else:
            result = checkSW(table, col, row, player, direction, counter)
            if result:
                col = result[0]
                row = result[1]
                direction = result[2]
                counter = result[3]
            else:
                return False
    

# Diagonal helper-function 
def checkSE(table, col, row, player, direction, counter):
    if col >= COLMAX or row >= ROWMAX:
        col -= counter + 1
        row -= counter + 1
        direction = 'nw'
        return [col, row, direction, counter]


    if table[col][row] == player and direction == 'se':
            counter += 1
            col += 1
            row += 1
    elif table[col][row] != player and direction == 'se':
        col -= counter + 1
        row -= counter + 1
        direction = 'nw'
        return [col, row, direction, counter]
    
    return [col, row, direction, counter]


# Diagonal helper-function
def checkNW(table, col, row, player, direction, counter):
    if col < 0 or row < 0:
        return

    if table[col][row] == player and direction == 'nw':
            counter += 1
            col -= 1
            row -= 1
    elif table[col][row] != player and direction == 'nw':
        return

    
    return [col, row, direction, counter]


# Diagonal helper-function
def checkNE(table, col, row, player, direction, counter):
    if col < 0 or row >= ROWMAX:
        col += counter + 1
        row -= counter + 1
        direction = 'sw'
        return [col, row, direction, counter]

    if table[col][row] == player and direction == 'ne':
        counter += 1
        col -= 1
        row += 1


    elif table[col][row] != player and direction == 'ne':
        col += counter + 1
        row -= counter + 1
        direction = 'sw'
    

    return [col, row, direction, counter]


# Diagonal helper-function
def checkSW(table, col, row, player, direction, counter):
    if col >= COLMAX or row < 0:
        return

    if table[col][row] == player and direction == 'sw':
            counter += 1
            col += 1
            row -= 1
    elif table[col][row] != player and direction == 'sw':
        return
    

    return [col, row, direction, counter]


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
    print()
    for line in table:
        for element in line:
            if element in range(1, 6):
                coloredPrint(element, RED, end='  ')
            elif element == 7:
                coloredPrint(element, BLUE, end='  ')
            else:
                print(element, end='  ')
        print()

    print("_  " * 7)

    for num in range(1, 8):
        print(num, end="  ")
    print("\n")


# Returns the first column index that no player set a unit
# in a selected row.
def columnIndexByRow(table, row):
    for i in range(5, -1, -1):
        if table[i][row] == 0:
            return i
    return -1


# Prints colored text in terminal
def coloredPrint(text, color, end='\n'):
    os.system('color')
    sys.stdout.write(color)
    print(text, end=end)
    sys.stdout.write("\033[0;0m")


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


# Easy Mode
def serverTurn(table, checkWinFuncs, conn, addr):
    row = random.randint(0, 6)
    col = columnIndexByRow(table, row)

    while col == -1:
        row = random.randint(0, 6)
        col = columnIndexByRow(table, row)

    table[col][row] = SERVER_PLAYER
    win = isWin(checkWinFuncs, table, col, row, SERVER_PLAYER)

    if win:
        conn.send(json.dumps("YOU LOST!").encode(FORMAT))
        time.sleep(0.2)
        conn.send(json.dumps(table).encode(FORMAT))
    else:
        conn.send(json.dumps(table).encode(FORMAT))

    return win


# Hard mode
def serverTurnHardMode(table, checkWinFuncs, conn, addr, player):
    for row in range(7):
        col = columnIndexByRow(table, row)
        if isWin(checkWinFuncs, table, col, row, SERVER_PLAYER):
            table[col][row] = SERVER_PLAYER
            conn.send(json.dumps("YOU LOST!").encode(FORMAT))
            time.sleep(0.2)
            conn.send(json.dumps(table).encode(FORMAT))
            return
                
        if col == -1:
            continue

    for row in range(7):
        col = columnIndexByRow(table, row)
        if isWin(checkWinFuncs, table, col, row, player):
            table[col][row] = SERVER_PLAYER
            conn.send(json.dumps(table).encode(FORMAT))
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
