from checkWin import checkWinDiagNEtoSW, checkWinDiagSEtoNW, checkWinSides, checkWinDown

table = [
    [1, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0],
    [1, 0, 0, 1, 0, 1, 0],
    [1, 0, 1, 0, 0, 0, 1],
    [0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
]

check = [checkWinDown, checkWinSides, checkWinDiagNEtoSW, checkWinDiagSEtoNW]

for func in check:
    if func(table, 1, 4, 1):
        break
# checkWinDiagSEtoNW(table, 1, 4, 1)
# checkWinDiagNEtoSW(table, 1, 4, 1)
# checkWinSides(table, 0, 6, 1)
# checkWinDown(table, 0, 0, 1)
