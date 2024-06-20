
import chess.variant
import pygame as p
from minimax import Game 
from minimax import Move
import chess
from minimax import inverseChessNotation

boardd = chess.variant.SuicideBoard()
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
    winner = None
    sqSelected = ()
    playerClicks = []
    
    while running:
        for e in p.event.get():
            outcome = boardd.outcome()
            if outcome:
                if outcome.winner == chess.WHITE:
                    print("¡Las blancas ganaron!")
                elif outcome.winner == chess.BLACK:
                    print("¡Las negras ganaron!")
            if obj.whiteToMove == False:
                movement = machine_move(boardd.copy())
                if movement == "":
                    print("Ganan las negras")
                if movement:  # Check if movement is not empty
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

        
                
            if e.type == p.QUIT:
                running = False
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
                
        white_pieces, black_pieces = count_pieces(obj.board)
        if white_pieces <= 2:
            show_winner("Ganaron las piezas negras")
        elif black_pieces <= 2:
            show_winner("Ganaron las piezas blancas")

        if winner:
            winner_screen = show_winner(winner)
            screen.blit(winner_screen, (0, 0))
        else:
            # Aquí iría el código para actualizar la pantalla del juego normal
            screen.fill(p.Color("blue"))
            
        drawGame(screen,obj)
        clock.tick(max_fps)
        p.display.flip()
        
def show_winner(winner):
    winner_screen = p.Surface((window_width, window_height))
    font = p.font.Font(None, 36)
    message = f"¡{winner} ganan!"
    winner_screen.fill(p.Color("white"))
    text_surface = font.render(message, True, p.Color("black"))
    text_rect = text_surface.get_rect(center=(window_width // 2, window_height // 2))
    winner_screen.blit(text_surface, text_rect)
    return winner_screen

    
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
            

def machine_move(boardCopy):
    max = -99999
    movement = ""
    legal_moves = [str(mov) for mov in boardCopy.legal_moves]
    print(legal_moves[0])
    
    if not legal_moves: # Check if there are no legal moves
        print("No legal moves available.")
        return movement
    
    for move in legal_moves:
        print(f"Considering move: {move}")
        result = alphabeta_pruning(boardCopy.copy(),move,3,-999999,9999999,False)
        print(f"Result for move {move}: {result}")
        if result > max:
            movement = move
            max = result
            
    if not movement:
        print("No valid moves found despite legal moves being present.")
            
    return movement

def alphabeta_pruning(boardCopy,movement,depth,alpha,beta,maximizingPlayer):
    if depth == 0 or boardCopy.is_game_over():
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
            if piece:
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

def count_pieces(board):
    white_pieces = 0
    black_pieces = 0
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece.startswith('w'):
                white_pieces += 1
            elif piece.startswith('b'):
                black_pieces += 1
    return white_pieces, black_pieces

    

if __name__ == '__main__':
    main()