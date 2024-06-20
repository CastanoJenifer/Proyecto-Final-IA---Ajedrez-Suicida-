import chess.variant

# Crear un tablero de ajedrez
board = chess.variant.AntichessBoard()

# Imprimir el tablero
print(board.piece_map().values())

# Imprimir los posibles movimientos
for move in board.legal_moves:
    print(move)

class arbolMiniMax:
    def __init__(self, board, depth=0, max_depth=4):
        self.board = board
        self.depth = depth
        self.max_depth = max_depth
        self.hijos = []
        self.valor = self.evaluate()
    
    def evaluate(self):
        piece_values = {
            chess.PAWN: -1,
            chess.KNIGHT: -3,
            chess.BISHOP: -3,
            chess.ROOK: -5,
            chess.QUEEN: -9,
            chess.KING: -2
        }
        pieces = self.board.piece_map().values()
        
        value = sum(piece_values[piece.piece_type] for piece in pieces)
        return value
    
    def minimax(self, is_maximizing):
        if self.depth == self.max_depth:
            return self.valor
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in self.board.legal_moves:
                new_board = self.board.copy()
                new_board.push(move)
                child = arbolMiniMax(new_board, self.depth+1, self.max_depth)
                self.hijos.append(child)
                eval = child.minimax(False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.board.legal_moves:
                new_board = self.board.copy()
                new_board.push(move)
                child = arbolMiniMax(new_board, self.depth+1, self.max_depth)
                self.hijos.append(child)
                eval = child.minimax(True)
                min_eval = min(min_eval, eval)
            return min_eval