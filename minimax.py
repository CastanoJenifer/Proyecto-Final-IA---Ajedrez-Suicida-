import numpy as np

class Game():
    
    def __init__(self):
        self.board = np.array([
            ['bRook', 'bHorse', 'bBishop', 'bQueen', 'bKing', 'bBishop', 'bHorse', 'bRook'],
            ['bPawn', 'bPawn', 'bPawn', 'bPawn', 'bPawn', 'bPawn', 'bPawn', 'bPawn'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wPawn', 'wPawn', 'wPawn', 'wPawn', 'wPawn', 'wPawn', 'wPawn', 'wPawn'],
            ['wRook', 'wHorse', 'wB', 'wQueen', 'wKing', 'wBishop', 'wHorse', 'wRook']
        ])
        
        self.whiteToMove = True
        self.moveLog = []