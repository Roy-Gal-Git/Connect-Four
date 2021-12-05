ROWMAX = 7
COLMAX = 6


# Checks if there's a win diagonally from South-East to North-West
def checkWinDiagSEtoNW(table, col, row, player):
    direction = 'se'
    counter = 1
    col += 1
    row += 1
    while True:
        if counter == 4:
            print(f'The winner is player #{player}!')
            return

        if direction == 'se':
            result = checkSE(table, col, row, player, direction, counter)
            if result:
                col = result[0]
                row = result[1]
                direction = result[2]
                counter = result[3]
            else:
                return

        else:
            result = checkNW(table, col, row, player, direction, counter)
            if result:
                col = result[0]
                row = result[1]
                direction = result[2]
                counter = result[3]
            else:
                return
        

# Checks if there's a win diagonally from North-East to South-West
def checkWinDiagNEtoSW(table, col, row, player):
    direction = 'ne'
    counter = 1
    col -= 1
    row += 1

    while True:
        if counter == 4:
            print(f'The winner is player #{player}!')
            return
        if direction == 'ne':
            result = checkNE(table, col, row, player, direction, counter)
            if result:
                col = result[0]
                row = result[1]
                direction = result[2]
                counter = result[3]
            else:
                return
        
        else:
            result = checkSW(table, col, row, player, direction, counter)
            if result:
                col = result[0]
                row = result[1]
                direction = result[2]
                counter = result[3]
            else:
                return
        
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


# Checks if there's a win on the sides
def checkWinSides(table, col, row, player):
    direction = 'right'
    counter = 1
    row += 1

    while row <= ROWMAX and row >= 0:
        if counter == 4:
            print(f'The winner is player #{player}!')
            return
        if row >= ROWMAX:
            direction = 'left'
            row -= counter

        if table[col][row] == player and direction == 'right':
            counter += 1
            row += 1
        elif table[col][row] != player and direction == 'right':
            direction = 'left'
            row -= counter

        if table[col][row] == player and direction == 'left':
            counter += 1
            row -= 1
        elif table[col][row] != player and direction == 'right':
            return
    return
