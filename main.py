"""
import pygame as p
from minimax import Game 
from minimax import Move

# valores iniciales
width = height = 512
dimension = 8
size = height // dimension
max_fps = 15
images = {}


def loadImages():
    pieces = ['bRook','bHorse','bBishop','bQueen','bKing','bPawn',
              'wRook','wHorse','wBishop','wQueen','wKing','wPawn']
    
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load(f'Images/{piece}.png'),(size,size))


def main():
    p.init()
    screen = p.display.set_mode((width, height))
    p.display.set_caption("Ajedrez suicida")
    icon = p.image.load("images/icono.png")
    p.display.set_icon(icon)
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    obj = Game()
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//size
                row = location[1]//size
                if sqSelected == (row,col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected)
                
        
        drawGame(screen,obj)
        clock.tick(max_fps)
        p.display.flip()
        

def drawGame(screen, obj):
    drawBoard(screen)
    drawPieces(screen, obj.board)
    

def drawBoard(screen):
    colors = [p.Color(198,155,124), p.Color(177,124,84)]
    
    for i in range(dimension):
        for j in range(dimension):
            color = colors[((i+j)%2)]
            p.draw.rect(screen, color, p.Rect(j*size, i*size, size,size))
            

def drawPieces(screen, board):
    for i in range(dimension):
        for j in range(dimension):
            piece = board[i][j]
            if piece != "--":
                screen.blit(images[piece], p.Rect(j*size, i*size, size, size))
            

if __name__ == '__main__':
    main()

    print('holas prros siiiiiii')
"""
    
import chess

board = chess.Board()
print(type(board))

# Print the chess board
print(board)

# Get a list of all legal moves
legal_moves = list(board.legal_moves)

# Print the legal moves
for move in legal_moves:
    print(move)
    