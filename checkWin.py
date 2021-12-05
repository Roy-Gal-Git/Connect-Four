ROWMAX = 7
COLMAX = 6


# Checks if there's a win diagonally from South-East to North-West
def checkWinDiagSEtoNW(table, col, row, player):
    direction = 'se'
    counter = 1
    while row <= ROWMAX and col <= COLMAX:
        if counter == 4:
            print(f'The winner is player #{player}!')
            return
        
        result = checkSE(table, col, row, player, direction, counter)
        if result:
            col = result[0]
            row = result[1]
            direction = result[2]
            counter = result[3]
        else:
            return


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
    originalCol = col
    originalRow = row

    while row <= ROWMAX and col <= COLMAX and col >= 0 and row >= 0:
        if counter == 4:
            print(f'The winner is player #{player}!')
            return

        result = checkNE(table, col, row, player, direction, counter)
        if result:
            col = result[0]
            row = result[1]
            direction = result[2]
            counter = result[3]
        else:
            return

        result = checkSW(table, col, row, player, direction, counter)
        if result:
            col = result[0]
            row = result[1]
            direction = result[2]
            counter = result[3]
        else:
            return
        

def checkSE(table, col, row, player, direction, counter):
    if col == COLMAX or row == ROWMAX:
        col -= counter + 1
        row -= counter + 1
        direction = 'nw'
        return [col, row, direction, counter]


    if table[col + 1][row + 1] == player and direction == 'se':
            counter += 1
            col += 1
            row += 1
    elif table[col + 1][row + 1] != player and direction == 'se':
        col -= counter
        row -= counter
        direction = 'nw'
    
    
    return [col, row, direction, counter]


def checkNW(table, col, row, player, direction, counter):
    if col < 0 or row < 0:
        return

    if table[col][row] == player and direction == 'nw':
            counter += 1
            col -= 1
            row -= 1
    elif table[col][row] != player and direction == 'nw':
        return [col, row, direction, counter]

    
    return [col, row, direction, counter]


def checkNE(table, col, row, player, direction, counter):
    if col < 0 or row == ROWMAX:
        col += counter + 1
        row -= counter + 1
        direction = 'sw'
        return [col, row, direction, counter]


    if table[col - 1][row + 1] == player and direction == 'ne':
            counter += 1
            col -= 1
            row += 1

    elif table[col - 1][row + 1] != player and direction == 'ne':
        col += counter
        row -= counter
        direction = 'sw'
    

    return [col, row, direction, counter]


def checkSW(table, col, row, player, direction, counter):
    if col == COLMAX or row < 0:
        return

    if table[col][row] == player and direction == 'sw':
            counter += 1
            col += 1
            row -= 1
    elif table[col][row] != player and direction == 'sw':
        return
    

    return [col, row, direction, counter]
