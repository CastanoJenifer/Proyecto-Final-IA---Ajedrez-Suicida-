import chess.variant

# Crear un tablero de ajedrez
board = chess.variant.AntichessBoard()

# Imprimir el tablero
print(board)

# Imprimir los posibles movimientos
for move in board.legal_moves:
    print(move)

class arbolMiniMax:
    def __init__(self, board):
        self.board = board
        self.hijos = []
        self.valor = 0