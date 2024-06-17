import chess

# Crear un tablero de ajedrez
board = chess.Board()

# Imprimir el tablero
print(board)

# Imprimir los posibles movimientos
for move in board.legal_moves:
    print(move)