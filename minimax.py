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
            ['wPawn', 'wPawn', '--', 'wPawn', 'wPawn', 'wPawn', 'wPawn', 'wPawn'],
            ['wRook', 'wHorse', 'wBishop', 'wQueen', 'wKing', 'wBishop', 'wHorse', 'wRook']
        ])
        
        self.whiteToMove = True
        self.moveLog = []
        
    def makeMove(self, move):
        self.board[move.startRow][move.startColumn] = "--"
        self.board[move.endRow][move.endColumn] = move.pieceMoved
        self.moveLog.append(move.pieceMoved)
        self.whiteToMove = not self.whiteToMove
        
        
        
class Move():
    
    ranksToRows = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    
    filesToCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    
    
    def __init__(self, start, end, board):
        self.startRow = start[0]
        self.startColumn = start[1]
        self.endRow = end[0]
        self.endColumn = end[1]
        self.pieceMoved = board[self.startRow][self.startColumn]
        self.pieceCaptured = board[self.endRow][self.endColumn]
        
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startColumn) + self.getRankFile(self.endRow, self.endColumn)
    
    def getRankFile(self, row, column):
        return self.colsToFiles[column] + self.rowsToRanks[row]
        