"""import pygame as p
from minimax import Game 



width = height = 400
dimension = 8
size = height // dimension
max_fps = 15
images = {}


def main():
    print('holas prros siiiiiii')"""
    
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
    