n = 8

board = [[0]*n for _ in range(n)]
n_solutions = 0

def nextValid(board, col):
    validCells = set()
    for i in range(n):
        isValid = True
        for j in range(0, col):
            if board[i][j] != 0:
                isValid = False
                break
        if not isValid:
            continue
        
        k = 1
        while ((i - k) >= 0) and ((col - k) >= 0):
            if board[i-k][col-k] != 0:
                isValid = False
                break
            k += 1
        if not isValid:
            continue

        k = 1
        while ((i + k) < n) and ((col - k) >= 0):
            if board[i+k][col-k] != 0:
                isValid = False
                break
            k += 1
        if not isValid:
            continue

        validCells.add(i)

    return validCells


def getSolutionIndex(board):
    index = []
    for i in range(n):
        for j in range(n):
            if board[j][i] != 0:
                index.append(j)
                break
    return index

def solveNqueensRecursive(board, i=0):
    global n_solutions
    if i == n:
        index = getSolutionIndex(board)
        if len(index) == n:
            print index
            n_solutions += 1
        else:
            return

    validCells = nextValid(board, i)
    for k in validCells:
        board[k][i] = 1
        solveNqueensRecursive(board, i+1)
        board[k][i] = 0

    return

def solveNqueens(board):
    global n_solutions
    validCells_0 = nextValid(board, 0)
    for i_0 in validCells_0:
        board[i_0][0] = 1
        validCells_1 = nextValid(board, 1)
        for i_1 in validCells_1:
            board[i_1][1] = 1
            validCells_2 = nextValid(board, 2)
            for i_2 in validCells_2:
                board[i_2][2] = 1
                validCells_3 = nextValid(board, 3)
                for i_3 in validCells_3:
                    board[i_3][3] = 1
                    validCells_4 = nextValid(board, 4)
                    for i_4 in validCells_4:
                        board[i_4][4] = 1
                        validCells_5 = nextValid(board, 5)
                        for i_5 in validCells_5:
                            board[i_5][5] = 1
                            validCells_6 = nextValid(board, 6)
                            for i_6 in validCells_6:
                                board[i_6][6] = 1
                                validCells_7 = nextValid(board, 7)
                                if len(validCells_7) == 1:
                                    i_7 = validCells_7.pop()
                                    print i_0, i_1, i_2, i_3, i_4, i_5, i_6, i_7
                                    n_solutions += 1
                                board[i_6][6] = 0
                            board[i_5][5] = 0
                        board[i_4][4] = 0
                    board[i_3][3] = 0
                board[i_2][2] = 0
            board[i_1][1] = 0
        board[i_0][0] = 0
    return


from time import time

start_1 = time()
solveNqueensRecursive(board)
end_1 = time()

#n_solutions = 0
#start_2 = time()
#solveNqueens(board)
#end_2 = time()

print end_1 - start_1  # recursive solution is slightly slower, but more readible and extendible
#print end_2 - start_2
print n_solutions