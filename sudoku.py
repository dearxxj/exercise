backtrack = 0


def nextCell(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return -1, -1


def isValid(grid, i, j, value):
    for k in range(9):
        if grid[k][j] == value:
            return False
    for k in range(9):
        if grid[i][k] == value:
            return False
    for k in range((i/3)*3, (i/3)*3+3):
        for n in range((j/3)*3, (j/3)*3+3):
            if grid[k][n] == value:
                return False
    return True

def validGuesses(grid, i, j):
    valid = {1, 2, 3, 4, 5, 6, 7, 8, 9} 
    left = set()
    for k in range(9):
        if grid[k][j] != 0:
            left.add(grid[k][j])
    for k in range(9):
        if grid[i][k] != 0:
            left.add(grid[i][k])
    for k in range((i/3)*3, (i/3)*3+3):
        for n in range((j/3)*3, (j/3)*3+3):
            if grid[k][n] != 0:
                left.add(grid[k][n])
    return valid.difference(left)


def solveSudoku(grid, i=0, j=0):
    global backtrack
    i, j = nextCell(grid)
    if i == -1:
        return True
    for guess in range(1, 10):
        if isValid(grid, i, j, guess):
            grid[i][j] = guess
            if solveSudoku(grid, i, j):
                return True

            grid[i][j] = 0
            backtrack += 1
    return False


def solveSudokuOpt1(grid, i=0, j=0):
    global backtrack
    i, j = nextCell(grid)
    if i == -1:
        return True
    
    guesses = validGuesses(grid, i, j)
    if guesses == []:
        return False
    
    for guess in guesses:
        grid[i][j] = guess
        if solveSudokuOpt1(grid, i, j):
            return True

        grid[i][j] = 0
        backtrack += 1
    return False

def solveSudokuOpt2(grid, i=0, j=0):
    global backtrack
    i, j = nextCell(grid)
    if i == -1:
        return True
    
    for guess in range(1, 10):
        if isValid(grid, i, j, guess):
            implks = makeImplications(grid, i, j, guess)
            if solveSudokuOpt2(grid, i, j):
                return True
            
            clearImplications(grid, implks)
            backtrack += 1
    
    return False

sectors = [[0, 3, 0, 3], [0, 3, 3, 6], [0, 3, 6, 9],
           [3, 6, 0, 3], [3, 6, 3, 6], [3, 6, 6, 9],
           [6, 9, 0, 3], [6, 9, 3, 6], [6, 9, 6, 9]]

def makeImplications(grid, i, j, value):
    global sectors
    implks = [(i, j, value)]
    grid[i][j] = value
    affectedCells = []  # store all cells affected by i, j

    for sector in sectors:
        possibleValues = {1, 2, 3, 4, 5, 6, 7, 8, 9}  #range(1, 10)
        for m in range(sector[0], sector[1]):
            for n in range(sector[2], sector[3]):
                if grid[m][n] in possibleValues:
                    possibleValues.remove(grid[m][n])

        for m in range(sector[0], sector[1]):
            for n in range(sector[2], sector[3]):
                if grid[m][n] == 0:
                    affectedCells.append([m, n, possibleValues.copy()])
    
    for cell in affectedCells:
        cellX, cellY = cell[0], cell[1]
        for m in range(9):
            if grid[cellX][m] in cell[2]:
                cell[2].remove(grid[cellX][m])
        for m in range(9):
            if grid[m][cellY] in cell[2]:
                cell[2].remove(grid[m][cellY])
        if len(cell[2]) == 1:
            left = cell[2].pop()
            #if isValid(grid, cellX, cellY, left): # this is needed if two implks occur in the same sector
            # funny if remove above time, faster and fewer backtracks
            grid[cellX][cellY] = left #cell[2][0]
            implks.append((cellX, cellY, left))

    ## for each implk do the makeImplications() again
    ## reduce the number of backtracks, but takes longer time
    if len(implks) > 1:
        for implk in implks[1:]:
            newImplks = makeImplications(grid, implk[0], implk[1], implk[2])
            if len(newImplks) > 1:
                implks += newImplks[1:]
    #print implks
    return implks

def clearImplications(grid, implks):
    for implk in implks:
        grid[implk[0]][implk[1]] = 0
    return


def printSudoku(grid):
    if solveSudoku(grid):
        print True
        for i in range(9):
            for j in range(8):
                print "[" + str(grid[i][j]) + "]",
            print "[" + str(grid[i][8]) + "]\n"
        print "backtrack = " + str(backtrack)
    else:
        print False
        print "backtrack = " + str(backtrack)

test1 = [[8, 0, 2, 0, 0, 0, 5, 0, 0],
        [0, 0, 0, 9, 0, 0, 0, 8, 0],
        [0, 0, 0, 7, 0, 4, 0, 3, 0],
        [0, 0, 7, 0, 1, 0, 0, 0, 2],
        [0, 5, 0, 2, 0, 9, 0, 1, 0],
        [2, 0, 0, 0, 7, 0, 4, 0, 0],
        [0, 2, 0, 4, 0, 1, 0, 0, 0],
        [0, 6, 0, 0, 0, 8, 0, 0, 0],
        [0, 0, 8, 0, 0, 0, 3, 0, 9]]

test = [[8, 5, 0, 0, 0, 2, 4, 0, 0],
        [7, 2, 0, 0, 0, 0, 0, 0, 9],
        [0, 0, 4, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 7, 0, 0, 2],
        [3, 0, 5, 0, 0, 0, 9, 0, 0],
        [0, 4, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 0, 0, 7, 0],
        [0, 1, 7, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 3, 6, 0, 4, 0]]

from time import time

print validGuesses(test1, 2, 2)    

start = time() 
printSudoku(test1)
end = time()

## funny that fewer backtracks do not mean faster
## solveSudokuOpt1 is the fastest actually for both tests
## solveSudokuOpt2 is the slowest for both tests
print end - start
