
import chess.variant
import pygame as p
from board import Game 
from board import Move
import chess
from board import inverseChessNotation
import random


# valores iniciales
width = height = 512
dimension = 8
size = height // dimension
max_fps = 15
images = {}
p.font.init()
font = p.font.Font(None, 36)
screen = p.display.set_mode((width, height))


boardd = chess.variant.SuicideBoard()

def loadImages():
    pieces = ['bRook','bHorse','bBishop','bQueen','bKing','bPawn',
              'wRook','wHorse','wBishop','wQueen','wKing','wPawn']
    
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load(f'Images/{piece}.png'),(size,size))


def main():
    p.init()
    p.display.set_caption("Ajedrez suicida")
    icon = p.image.load("images/icono.png")
    p.display.set_icon(icon)
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    running = True
    
    # variables para el tablero
    obj = Game()
    loadImages()
    sqSelected = ()
    playerClicks = []
    
    # verificar ganador
    blancas = False
    negras = False
    
    # Inicio del bucle
    while running:
        for e in p.event.get():
            outcome = boardd.outcome()
            if outcome:
                if outcome.winner == chess.WHITE:
                    blancas = True
                    running = False # terminar bucle si ya se tiene un ganador
                elif outcome.winner == chess.BLACK:
                    negras = True
                    running = False # terminar bucle si ya se tiene un ganador
            if obj.whiteToMove == False: # Si el turno de las blancas está en False
                movement = machine_move(boardd.copy()) # El turno lo tiene la IA
                if movement:  
                    if chess.Move.from_uci(movement) in boardd.legal_moves:
                        boardd.push(chess.Move.from_uci(movement))
                        start, end = inverseChessNotation(movement)
                        move = Move(start, end, obj.board)
                        print(move.getChessNotation())
                        obj.makeMove(move)
                        
                    else:
                        print(f"Invalid move: {movement}")
                else:
                    print("No valid moves available")
                movement = ""
                
                # hacer el movimiento tambien en la board de pygame, obj.board 
           
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//size
                row = location[1]//size
                if sqSelected == (row,col) and obj:
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    if obj.whiteToMove == True and obj.board[playerClicks[0][0]][playerClicks[0][1]][0] == 'w':
                        if obj.board[playerClicks[1][0]][playerClicks[1][1]][0] != "w":
                            move = Move(playerClicks[0], playerClicks[1],obj.board)
                            if str(move.getChessNotation()) in [str(mov) for mov in boardd.legal_moves]:
                                print(move.getChessNotation())
                                obj.makeMove(move)
                                boardd.push(chess.Move.from_uci(move.getChessNotation()))
                            else:
                                print("Movimiento ilegal")
                                                       
                    sqSelected = ()
                    playerClicks = []
        
            
        drawGame(screen,obj)
        clock.tick(max_fps)
        p.display.flip()

    if blancas:
        show_small_screen("Ganaron las piezas blancas", font)
    elif negras:
        show_small_screen("Ganaron las piezas negras", font)
    
    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()            

def machine_move(boardCopy):
    max = -99999
    movement = ""
    legal_moves = [str(mov) for mov in boardCopy.legal_moves] # Movimientos legales segun libreria Antichess
    
    if not legal_moves: # Si no hay movimientos legales
        print("No legal moves available.")
        return movement
    
    for move in legal_moves:
        result = alphabeta_pruning(boardCopy.copy(),move,3,-999999,9999999,False) # Funcion que realiza la poda.

        if result > max:
            movement = move
            max = result
            
    if not movement:
        movement = random.choice(legal_moves) 
            
    return movement


# Funcion Poda Alfa-Beta
def alphabeta_pruning(boardCopy,movement,depth,alpha,beta,maximizingPlayer):
    if depth == 0 or boardCopy.is_game_over(): #Si se llega a la profundidad indicada o si perdí
        return evaluateBoard(boardCopy,movement) # retorna el valor heuristico del nodo
    
    boardCopy.push(chess.Move.from_uci(movement)) # Hace el movimiento
    legal_moves = [str(mov) for mov in boardCopy.legal_moves] # Muestra todos los movimientos legales del nuevo tablero

    if maximizingPlayer:
        value = -999999
        for move in legal_moves:
            value = max(value,alphabeta_pruning(boardCopy.copy(),move,depth-1,alpha,beta,False)) 
            # funcion recursiva para encontrar el valor de cada uno de mis hijos MIN
            if value >= beta: # Si mi hijo actual es mayor o igual a beta
                break # Poda
            alpha = max(alpha,value) # El alfa se actualiza con el mayor valor que se escogió entre los MIN podando
        return value
    else:
        value = 999999
        for move in legal_moves:
            value = min(value,alphabeta_pruning(boardCopy.copy(),move,depth-1,alpha,beta,True))
            # funcion recursiva para encontrar el valor de cada uno de mis hijos MAX
            if value <= alpha: # Si mi hijo actual es menor o igual a beta 
                break # Poda
            beta = min(beta,value)
        return value

# Funcion que maneja la heuristica
def evaluateBoard(boardCopy,movement):
    value = 0 # valor final de la funcion heuristica
    boardCopy.push(chess.Move.from_uci(movement)) # hace el movimiento
    for i in range(8):
        for j in range(8):
            piece = str(boardCopy.piece_at(chess.Square((i*8+j)))) #toma el string o el valor de la pieza
            if piece:
                value += getValueOfPiece(piece)
    return value

# Funcion heuristica
def getValueOfPiece(letter):

# PIEZAS NEGRAS (MAX) Busca el mayor valor para ganar.
# Caso: Cuando MIN captura las piezas de la IA el valor se reduce a cero
# Entonces, encuentra su mayor valor.

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

# PIEZAS BLANCAS (MIN) Buscan el menor valor para ganar.
# Caso: Cuando MAX captura las piezas del usuario el valor se reduce a cero.
# Entonces, encuentra su menor valor.
  
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


def show_small_screen(message, font):

    small_screen_width, small_screen_height = 400, 100
    small_screen = p.Surface((small_screen_width, small_screen_height))
    
    small_screen_x = (width - small_screen_width) // 2
    small_screen_y = (height - small_screen_height) // 2

    small_screen.fill("white")

    text = font.render(message, True, "black")
    text_rect = text.get_rect(center=(small_screen_width // 2, small_screen_height // 2))

    small_screen.blit(text, text_rect)

    screen.blit(small_screen, (small_screen_x, small_screen_y))
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