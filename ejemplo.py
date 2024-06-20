import chess.variant
import pygame
import sys
import chess

board = chess.variant.AntichessBoard()

WIDTH = 650

WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Chess")
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)

class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(col * width)
        self.y = int(row * width)
        self.colour = WHITE

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.colour, (self.x, self.y, WIDTH / 8, WIDTH / 8))

    def setup(self, WIN,boardM):
        
        if boardM[self.row][self.col] != "None":
                WIN.blit(pygame.image.load(self.getImage(boardM[self.row][self.col])), (self.x, self.y))
    
    def getImage(self,letter):
        if letter == 'r':
            return "Images/bRook.png"
        if letter == 'n':
            return "Images/bHorse.png"
        if letter == 'b':
            return "Images/bBishop.png"
        if letter == 'q':
            return "Images/bQueen.png"
        if letter == 'k':
            return "Images/bKing.png"
        if letter == 'p':
            return "Images/bPawn.png"
        
        if letter == 'R':
            return "Images/wRook.png"
        if letter == 'N':
            return "Images/wHorse.png"
        if letter == 'B':
            return "Images/wBishop.png"
        if letter == 'Q':
            return "Images/wQueen.png"
        if letter == 'K':
            return "Images/wKing.png"
        if letter == 'P':
            return "Images/wPawn.png"

        return ""

        """
        For now it is drawing a rectangle but eventually we are going to need it
        to use blit to draw the chess pieces instead
        """

def make_grid(rows, width):
    grid = []
    gap = WIDTH // rows
    print(gap)
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap)
            grid[i].append(node)
            if (i+j)%2 ==1:
                grid[i][j].colour = GREY
    return grid

def draw_grid(win, rows, width):
    gap = width // 8
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))

def update_display(win, grid, rows, width):
    boardM = []
    for i in range(8):
        arr = [str(board.piece_at(chess.Square((i*8+j)))) for j in range(8)]
        boardM.insert(0,arr)

    for row in grid:
        for spot in row:
            spot.draw(win)
            spot.setup(win,boardM)
    draw_grid(win, rows, width)
    pygame.display.update()

def Find_Node(pos, WIDTH):
    interval = WIDTH / 8
    y, x = pos
    rows = y // interval
    columns = x // interval
    x,y = int(rows), int(columns)
    pos = "" + ['a','b','c','d','e','f','g','h'][x] + f"{8-y}"
    return pos

def machine_move(boardCopy):
    max = -99999
    movement = ""
    legal_moves = [str(mov) for mov in boardCopy.legal_moves]
    for move in legal_moves:
        result = alphabeta_pruning(boardCopy.copy(),move,3,-999999,9999999,False)
        if result > max:
            movement = move
            max = result
    return movement

def alphabeta_pruning(boardCopy,movement,depth,alpha,beta,maximizingPlayer):
    if depth == 0:
        return evaluateBoard(boardCopy,movement)
    
    boardCopy.push(chess.Move.from_uci(movement))
    legal_moves = [str(mov) for mov in boardCopy.legal_moves]

    if maximizingPlayer:
        value = -999999
        for move in legal_moves:
            value = max(value,alphabeta_pruning(boardCopy.copy(),move,depth-1,alpha,beta,False))
            if value >= beta:
                break
            alpha = max(alpha,value)
        return value
    else:
        value = 999999
        for move in legal_moves:
            value = min(value,alphabeta_pruning(boardCopy.copy(),move,depth-1,alpha,beta,True))
            if value <= alpha:
                break
            beta = min(beta,value)
        return value

def evaluateBoard(boardCopy,movement):
    value = 0
    boardCopy.push(chess.Move.from_uci(movement))
    for i in range(8):
        for j in range(8):
            piece = str(boardCopy.piece_at(chess.Square((i*8+j))))
            value += getValueOfPiece(piece)
    return value

def getValueOfPiece(letter):
        if letter == 'r':
            return -50
        if letter == 'n':
            return -30
        if letter == 'b':
            return -30
        if letter == 'q':
            return -90
        if letter == 'k':
            return -20
        if letter == 'p':
            return -10
        
        if letter == 'R':
            return 50
        if letter == 'N':
            return 30
        if letter == 'B':
            return 30
        if letter == 'Q':
            return 90
        if letter == 'K':
            return 20
        if letter == 'P':
            return 10

        return 0

def main(WIN, WIDTH):
    movement = ""
    grid = make_grid(8, WIDTH)
    while True:
        pygame.time.delay(50) ##stops cpu dying
        for event in pygame.event.get(): #This quits the program if the player closes the window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                node = Find_Node(pygame.mouse.get_pos(), WIDTH)
                if movement == "":
                    piece = board.piece_at(chess.Square(chess.parse_square(node)))
                    if piece != None and str(piece).isupper(): 
                        movement = node
                    else:
                        print("Not Valid")
                else:
                    movement += node
                    if not chess.Move.from_uci(movement) in board.legal_moves:
                        print("Not valid move")
                        movement = ""
                    else:
                        board.push(chess.Move.from_uci(movement))
                        movement = ""
                        
                        #Turno de la maquina
                        movement = machine_move(board.copy())
                        board.push(chess.Move.from_uci(movement))
                        movement = ""

            update_display(WIN, grid, 8, WIDTH)



main(WIN, WIDTH) 