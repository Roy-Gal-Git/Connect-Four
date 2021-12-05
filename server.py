from checkWin import checkWinDiagNEtoSW, checkWinDiagSEtoNW

table = [
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
]

checkWinDiagSEtoNW(table, 0, 3, 1)
checkWinDiagNEtoSW(table, 0, 3, 1)
