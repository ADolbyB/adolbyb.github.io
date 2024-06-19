# Handles the game and player's turn to move, available legal moves, etc
import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from .board import Board

# Game Class interfaces with the board
# Keeps game separate from main loop checking buttons, movement, etc
class Game:
    def __init__(self, win): # could define game window in here, BUT in the case we want more than one instance running at the same time
        self._init()
        self.win = win # game window

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
    
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {} # dictionary to define legal moves

    def winner(self):
        return self.board.winner()

    def reset(self): # user reset to start a new game
        self._init()

    def select(self, row, col): # determies is a move can be performed or not
        if self.selected: # if the piece is already selected
            result = self._move(row, col) # move selected piece to row/col
            if not result: # if move is not legal (wrong space, etc)
                self.selected = None # reset the selection
                self.select(row, col) # reselect a row and column
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True # valid selection returns true

        return False # Invalid selection returns false.

    def _move(self, row, col): # private: used by select only
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves: # can only move to empty space == 0
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else: 
            return False

        return True # move is successful

    
    def draw_valid_moves(self, moves): # loop through dictionary
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    # AI Function definition # 3
    def get_board(self):
        return self.board

    # AI Function definition # 4
    def ai_move(self, board):
        self.board = board
        self.change_turn()