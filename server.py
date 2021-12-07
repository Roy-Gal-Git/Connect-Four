from checkWin import checkWinDiagNEtoSW, checkWinDiagSEtoNW, checkWinSides, checkWinDown

table = [
    [1, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0],
    [1, 0, 0, 1, 0, 1, 0],
    [1, 0, 1, 0, 0, 0, 1],
    [0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
]

checkWinFuncs = [checkWinDown, checkWinSides, checkWinDiagNEtoSW, checkWinDiagSEtoNW]


def isWin(funcs, table, col, row, player):
    try:
        for func in funcs:
            if func(table, col, row, player):
                return True
        return False

    except IndexError as e:
        print(f'[ERROR] {e}')

isWin(checkWinFuncs, table, 1, 4, 1)