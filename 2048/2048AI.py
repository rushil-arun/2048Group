import pygame
import random
import time
from copy import deepcopy
import math
pygame.init()
width = 600
window = pygame.display.set_mode((width, width))

GAP = width // 4
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 165, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
turquoise = (64, 244, 208)
purple = (128, 0, 128)
grey = (128, 128, 128)
pink = (255, 0, 255)
teal = (3, 255, 188)
neon = (172, 255, 3)
border = 5
turn2 = 0
score = 0
realDepth = 4
a = None
numFont = pygame.font.SysFont("comicsans", 50)
reverseList = [(3, 3), (3, 2), (3, 1), (3, 0), (2, 3), (2, 2), (2, 1), (2, 0), (1, 3), (1, 2), (1, 1), (1, 0), (0, 3), (0, 2), (0, 1), (0, 0)]
board = [
    ['', '', '', ''],
    ['', '', '', ''],
    ['', '', '', ''],
    ['', '', '', ''],
]
game_over = False

dirList = ['Up', 'Down', 'Left', 'Right']
            
state1 = None
state2 = None
state3 = None
state4 = None

def setCaption():
    pygame.display.set_caption(str(score))

def getOpenSpots():
    spotsOpen = 0
    for i in range(4):
        for z in range(4):
            if board[i][z] == '':
                spotsOpen += 1

    return spotsOpen * 100

def getMaxTile():
    maxTile = 0
    for i in range(4):
        for z in range(4):
            if board[i][z] != '':
                if int(float(board[i][z])) > maxTile:
                    maxTile = int(float(board[i][z]))

    return maxTile

def getTileDistance():
    secondMaxTile = 0
    bestTile = getMaxTile()

    for i in range(4):
        for z in range(4):
            if board[i][z] != '':
                if int(float(board[i][z])) > secondMaxTile and int(float(board[i][z])) < bestTile:
                    secondMaxTile = int(float(board[i][z]))

    for i in range(4):
        for z in range(4):
            if board[i][z] == str(bestTile):
                firstMove = i, z
                break

    for i in range(4):
        for z in range(4):
            if board[i][z] == str(secondMaxTile):
                secondMove = i, z
                return -(math.sqrt(((firstMove[0] - secondMove[0]) ** 2) + ((firstMove[1] - secondMove[1]) ** 2)))

    
    return 0           

def tilePos():
    value = getMaxTile()
    for i in range(4):
        for z in range(4):
            if board[i][z] == str(value):
                move = i, z
                if move == (0, 0) or move == (3, 0) or move == (3, 3) or move == (0, 3):
                    return 200000
                else:
                    return -200000



def drawLines():
    for i in range (1, 4):
        pygame.draw.line(window, white, (i * GAP, 0), (i * GAP, width))
        pygame.draw.line(window, white, (0, i * GAP), (width, i * GAP))

def drawNumbers():
    for i in range(4):
        for j in range(4):
            if board[i][j] != '':
                text = numFont.render(str(board[i][j]), 1, white)
                rect = text.get_rect(center=((i* GAP) + (GAP // 2), (j * GAP) + (GAP // 2)))
                window.blit(text, rect)


def drawBoard():
    for i in range(4):
        for j in range(4):
            if board[i][j] == '2':
                pygame.draw.rect(window, red, ((i * GAP) + border, (j * GAP) + border, GAP - (border * 2), GAP - (border * 2)))
            elif board[i][j] == '4':
                pygame.draw.rect(window, orange, ((i * GAP) + border, (j * GAP) + border, GAP - (border * 2), GAP - (border * 2)))
            elif board[i][j] == '8':
                pygame.draw.rect(window, yellow, ((i * GAP) + border, (j * GAP) + border, GAP - (border * 2), GAP - (border * 2)))
            elif board[i][j] == '16':
                pygame.draw.rect(window, green, ((i * GAP) + border, (j * GAP) + border, GAP - (border * 2), GAP - (border * 2)))
            elif board[i][j] == '32':
                pygame.draw.rect(window, blue, ((i * GAP) + border, (j * GAP) + border, GAP - (border * 2), GAP - (border * 2)))
            elif board[i][j] == '64':
                pygame.draw.rect(window, turquoise, ((i * GAP) + border, (j * GAP) + border, GAP - (border * 2), GAP - (border * 2)))
            elif board[i][j] == '128':
                pygame.draw.rect(window, purple, ((i * GAP) + border, (j * GAP) + border, GAP - (border * 2), GAP - (border * 2)))
            elif board[i][j] == '256':
                pygame.draw.rect(window, grey, ((i * GAP) + border, (j * GAP) + border, GAP - (border * 2), GAP - (border * 2)))
            elif board[i][j] == '512':
                pygame.draw.rect(window, pink, ((i * GAP) + border, (j * GAP) + border, GAP - (border * 2), GAP - (border * 2)))
            elif board[i][j] == '1024':
                pygame.draw.rect(window, teal, ((i * GAP) + border, (j * GAP) + border, GAP - (border * 2), GAP - (border * 2)))
            elif board[i][j] == '2048':
                pygame.draw.rect(window, neon, ((i * GAP) + border, (j * GAP) + border, GAP - (border * 2), GAP - (border * 2)))

def pickNewSquare():
    global turn2
    positionOne1 = None
    positionOne2 = None
    openSquares = []
    openSquares2 = []
    openSpots2 = 0
    for i in range(4):
        for z in range(4):
            if board[i][z] == '':
                openSpots2 += 1

    if openSpots2 == 0:
        return None, None, None, None
    if turn2 == 0:
        for i in range(4):
            for j in range(4):
                if board[i][j] == '':
                    openSquares.append((i, j))

        numOne = random.randint(0, len(openSquares) - 1)
        positionOne1 = openSquares[numOne][0]
        positionOne2 = openSquares[numOne][1]
        openSquares.pop(numOne)
        #print(openSquares)
        numTwo = random.randint(0, len(openSquares) - 1)

        return positionOne1, positionOne2, openSquares[numTwo][0], openSquares[numTwo][1]

    else:
        for i in range(4):
            for j in range(4):
                if board[i][j] == '':
                    openSquares2.append((i, j))

        secondNumOne = random.randint(0, len(openSquares2) - 1)
        return openSquares2[secondNumOne][0], openSquares2[secondNumOne][1], None, None


def pickTwoOrFour():
    global turn2
    number = None
    secondNumber = None

    if turn2 == 0:
        choice = random.randint(0, 9)
        choice2 = random.randint(0, 9)
        if choice == 0:
            number = 4
        else:
            number = 2
        if choice2 == 0:
            secondNumber = 4
        else:
            secondNumber = 2
    else:
        choice = random.randint(0, 9)
        if choice == 0:
            number = 4
        else:
            number = 2
        secondNumber = None

    return number, secondNumber


#-------------------------------------------------------------------------------

def moveUp():
    global board
    for i in range(4):
        for j in range(1, 4):
            if board[i][j] != '':
                repX, repY = i, j
                
                temp = board[i][j]

                while True:
                    if repY > 0 and board[repX][repY - 1] == '':
                        repY -= 1
                        board[repX][repY] = str(temp)
                        board[repX][repY + 1] = ''
                    else:
                        break

                #mergeUp()

                

def mergeUp():
    global score
    for p in range(4):
        for q in range(1, 4):
            if board[p][q] == board[p][q-1] and board[p][q] != '':
                score += int(float(board[p][q])) * 2
                board[p][q - 1] = str(int(float(board[p][q])) * 2)
                board[p][q] = ''

#------------------------------------------------------------------------------------------------

def moveDown():
    global board
    for i in reverseList:
        if board[i[0]][i[1]] != '':
            repX, repY = i[0], i[1]
                
            temp = board[i[0]][i[1]]

            while True:
                if repY < 3 and board[repX][repY + 1] == '':
                    repY += 1
                    board[repX][repY] = str(temp)
                    board[repX][repY - 1] = ''
                else:
                    break

            #mergeDown()

def mergeDown():
    global score
    for i in reverseList:
        if i[1] < 3:
            if board[i[0]][i[1]] == board[i[0]][i[1] + 1] and board[i[0]][i[1]] != '':
                score += int(float(board[i[0]][i[1]])) * 2
                board[i[0]][i[1] + 1] = str(int(float(board[i[0]][i[1]])) * 2)
                board[i[0]][i[1]] = ''

#-------------------------------------------------------------------------------------------
def moveLeft():
    global board
    for i in range(1, 4):
        for j in range(4):
            if board[i][j] != '':
                repX, repY = i, j
                
                temp = board[i][j]

                while True:
                    if repX > 0 and board[repX - 1][repY] == '':
                        repX -= 1
                        board[repX][repY] = str(temp)
                        board[repX + 1][repY] = ''
                    else:
                        break
                
                #mergeLeft()
                

def mergeLeft():
    global score
    for p in range(1, 4):
        for q in range(4):
            if board[p][q] == board[p - 1][q] and board[p][q] != '':
                score += int(float(board[p][q])) * 2
                board[p - 1][q] = str(int(float(board[p][q])) * 2)
                board[p][q] = ''

#----------------------------------------------------------------------------------------------------

def moveRight():
    global board
    for i in reverseList:
        if board[i[0]][i[1]] != '':
            repX, repY = i[0], i[1]
                
            temp = board[i[0]][i[1]]

            while True:
                if repX < 3 and board[repX + 1][repY] == '':
                    repX += 1
                    board[repX][repY] = str(temp)
                    board[repX - 1][repY] = ''
                else:
                    break
            
            #mergeRight()

def mergeRight():
    global score
    for i in reverseList:
        if i[0] < 3:
            if board[i[0]][i[1]] == board[i[0] + 1][i[1]] and board[i[0]][i[1]] != '':
                score += int(float(board[i[0]][i[1]])) * 2
                board[i[0] + 1][i[1]] = str(int(float(board[i[0]][i[1]])) * 2)
                board[i[0]][i[1]] = ''
                
#----------------------------------------------------------------------------------------------------------------
def start():
    x, y, w, z = pickNewSquare()
    a, b = pickTwoOrFour()
    board[x][y] = str(a)
    board[w][z] = str(b)

start()

def changeTurn():
    global board
    x, y, w, z = pickNewSquare()
    a, b = pickTwoOrFour()
    if x == y == w == z == None:
        pass
    else:
        board[x][y] = str(a)

def scoreTiedPosition():
    spots = 0
    finalScore = 0
    distanceList = []
    for i in range(4):
        for z in range(4):
            if board[i][z] != '':
                if int(float(board[i][z])) >= 8:
                    squareDist = math.sqrt((((i * GAP) - (width / 2)) ** 2) + (((z * GAP) - (width / 2)) ** 2))
                    distanceList.append(squareDist)

    for i in distanceList:
        finalScore += (i * 350)
    
    for i in range(1, 4):
        for z in range(4):
            if board[i][z] != '':
                if board[i][z] == board[i-1][z] and int(float(board[i][z])) >= 2:
                    finalScore += 1500000

    for i in range(4):
        for z in range(1, 4):
            if board[i][z] != '':
                if board[i][z] == board[i][z-1] and int(float(board[i][z])) >= 2:
                    finalScore += 1500000
    
    for i in range(3):
        for z in range(4):
            if board[i][z] != '':
                if board[i][z] == board[i+1][z] and int(float(board[i][z])) >= 2:
                    finalScore += 1500000

    for i in range(4):
        for z in range(3):
            if board[i][z] != '':
                if board[i][z] == board[i][z+1] and int(float(board[i][z])) >= 2:
                    finalScore += 1500000

    for i in range(4):
        for j in range(4):
            if board[i][j] == '2':
                finalScore += 5
            elif board[i][j] == '4':
                finalScore += 55
            elif board[i][j] == '8':
                finalScore += 220
            elif board[i][j] == '16':
                finalScore += 900
            elif board[i][j] == '32':
                finalScore += 3800
            elif board[i][j] == '64':
                finalScore += 16000
            elif board[i][j] == '128':
                finalScore += 65000
            elif board[i][j] == '256':
                finalScore += 275000
            elif board[i][j] == '512':
                finalScore += 1100000
            elif board[i][j] == '1024':
                finalScore += 4000000
            elif board[i][j] == '2048':
                finalScore += 16500000


    for i in range(4):
        for z in range(4):
            if board[i][z] == '':
                spots += 1

    finalScore += (spots * 3500000)
    finalScore += (score * 600)

    return finalScore


def algorithm(depth, maxPlayer):
    global state1, state2, state3, state4, board, score
    result1, result2, result3, result4 = checkLoss()
    if result1 == result2 == result3 == result4 == True or depth == 0:
        if result1 == result2 == result3 == result4 == True:
            return 0
        if depth == 0:
            return (score * 20) + ((getOpenSpots() ** 2) * getMaxTile()) + tilePos() #+ getTileDistance() #- change this to test the results. 
            #return scoreTiedPosition()

    if maxPlayer:
        bestScore = -(float('inf'))
        for i in dirList:
            if i == 'Up':
                a = score
                copyBoard3 = deepcopy(board)
                moveUp()
                mergeUp()
                moveUp()
                if copyBoard3 == board:
                    pass
                else:
                    changeTurn()
                mmScore = algorithm(depth - 1, True)
                score = a
                board = deepcopy(copyBoard3)
                bestScore = max(mmScore, bestScore)

            if i == 'Down':
                a = score
                copyBoard3 = deepcopy(board)
                moveDown()
                mergeDown()
                moveDown()
                if copyBoard3 == board:
                    pass
                else:
                    changeTurn()
                mmScore = algorithm(depth - 1, True)
                score = a
                board = deepcopy(copyBoard3)
                bestScore = max(mmScore, bestScore)
            if i == 'Left':
                a = score
                copyBoard3 = deepcopy(board)
                moveLeft()
                mergeLeft()
                moveLeft()
                if copyBoard3 == board:
                    pass
                else:
                    changeTurn()
                mmScore = algorithm(depth - 1, True)
                score = a
                board = deepcopy(copyBoard3)
                bestScore = max(mmScore, bestScore)
            if i == 'Right':
                a = score
                copyBoard3 = deepcopy(board)
                moveRight()
                mergeRight()
                moveRight()
                if copyBoard3 == board:
                    pass
                else:
                    changeTurn()
                mmScore = algorithm(depth - 1, True)
                score = a
                board = deepcopy(copyBoard3)
                bestScore = max(mmScore, bestScore)

        return bestScore
        


    

def pickMove():
    global game_over, board, score
    bestScore = -(float('inf'))
    bestMove = None
    copyBoard2 = deepcopy(board)
    for i in dirList:
        if i == 'Up':
            a = score
            #print("a" + str(a))
            copyBoard = deepcopy(board)
            moveUp()
            mergeUp()
            moveUp()
            if copyBoard == board:
                pass
            else:
                changeTurn()
            mmScore = algorithm(realDepth, True)
            score = a
            board = deepcopy(copyBoard2)
            if mmScore > bestScore:
                bestScore = mmScore
                bestMove = 'Up'
        if i == 'Down':
            #board = deepcopy(copyBoard2)
            a = score
            #print("a" + str(a))
            copyBoard = deepcopy(board)
            moveDown()
            mergeDown()
            moveDown()
            if copyBoard == board:
                pass
            else:
                changeTurn()
            mmScore = algorithm(realDepth, True)
            score = a
            board = deepcopy(copyBoard2)
            if mmScore > bestScore:
                bestScore = mmScore
                bestMove = 'Down'
        if i == 'Left':
            #board = deepcopy(copyBoard2)
            a = score
            #print("a" + str(a))
            copyBoard = deepcopy(board)
            moveLeft()
            mergeLeft()
            moveLeft()
            if copyBoard == board:
                pass
            else:
                changeTurn()
            mmScore = algorithm(realDepth, True)
            score = a
            board = deepcopy(copyBoard2)
            if mmScore > bestScore:
                bestScore = mmScore
                bestMove = 'Left'
        if i == 'Right':
            #board = deepcopy(copyBoard2)
            a = score
            #print("a" + str(a))
            copyBoard = deepcopy(board)
            moveRight()
            mergeRight()
            moveRight()
            if copyBoard == board:
                pass
            else:
                changeTurn()
            mmScore = algorithm(realDepth, True)
            score = a
            board = deepcopy(copyBoard2)
            if mmScore > bestScore:
                bestScore = mmScore
                bestMove = 'Right'
    

    if bestMove == 'Up':
        copyBoard = deepcopy(board)
        moveUp()
        mergeUp()
        moveUp()
        if copyBoard == board:
            pass
        else:
            changeTurn()
    if bestMove == 'Down':
        copyBoard = deepcopy(board)
        moveDown()
        mergeDown()
        moveDown()
        if copyBoard == board:
            pass
        else:
            changeTurn()
    if bestMove == 'Right':
        copyBoard = deepcopy(board)
        moveRight()
        mergeRight()
        moveRight()
        if copyBoard == board:
            pass
        else:
            changeTurn()
    if bestMove == 'Left':
        copyBoard = deepcopy(board)
        moveLeft()
        mergeLeft()
        moveLeft()
        if copyBoard == board:
            pass
        else:
            changeTurn()


def checkLoss():
    openSpots = 0
    upBlocked = False
    rightBlocked = False
    leftBlocked = False
    downBlocked = False
    for i in range(4):
        for z in range(4):
            if board[i][z] == '':
                openSpots += 1

    if openSpots == 0:
        for i in range(4):
            for z in range(1, 4):
                if board[i][z] == board[i][z - 1]:
                    upBlocked = False
                    break
                else:
                    upBlocked = True
        
        for i in range(4):
            for z in range(3):
                if board[i][z] == board[i][z + 1]:
                    downBlocked = False
                    break
                else:
                    downBlocked = True

        for i in range(1, 4):
            for z in range(4):
                if board[i][z] == board[i - 1][z]:
                    leftBlocked = False
                    break
                else:
                    leftBlocked = True

        for i in range(3):
            for z in range(4):
                if board[i][z] == board[i + 1][z]:
                    rightBlocked = False
                    break
                else:
                    rightBlocked = True

    return upBlocked, downBlocked, leftBlocked, rightBlocked


while not game_over:
    if turn2 == 0:
        drawNumbers()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                copyBoard = deepcopy(board)
                moveUp()
                mergeUp()
                moveUp()
                if copyBoard == board:
                    pass
                else:
                    changeTurn()
            if event.key == pygame.K_DOWN:
                copyBoard = deepcopy(board)
                moveDown()
                mergeDown()
                moveDown()
                if copyBoard == board:
                    pass
                else:
                    changeTurn()
            if event.key == pygame.K_LEFT:
                copyBoard = deepcopy(board)
                moveLeft()
                mergeLeft()
                moveLeft()
                if copyBoard == board:
                    pass
                else:
                    changeTurn()
            if event.key == pygame.K_RIGHT:
                copyBoard = deepcopy(board)
                moveRight()
                mergeRight()
                moveRight()
                if copyBoard == board:
                    pass
                else:
                    changeTurn()

    check1, check2, check3, check4 = checkLoss()
    if check1 == check2 == check3 == check4 == True:
        print(board, check1, check2, check3, check4)
        game_over = True

    pickMove()
    window.fill(black)
    setCaption()
    drawBoard()
    drawNumbers()
    drawLines()
    
    
    

    pygame.display.update()

    turn2 += 1

#pygame.time.wait(6000)   
pygame.quit()