# board class: responsible for draing the board and pieces
import pygame
from .constants import BLACK, ROWS, COLS, RED, WHITE, SQUARE_SIZE
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12 # define the amount of red and black pieces each player begins with
        self.red_kings = self.white_kings = 0 # no one starts with king pieces
        self.create_board()

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2): # even indices are red, odd are black
                pygame.draw.rect(win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # AI definition #1 for Minimax: White = AI
    def evaluate(self): # Evaluate score of the board (AI difficulty)
        return self.white_left - self.red_left + (self.white_kings * 1.5 - self.red_kings * 1.5) # Edit: Increase weight of King Pieces

    # AI Minimax Function #2:
    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        #print(f'self.white_left = {self.white_left}')      # debug
        #print(f'self.white_kings = {self.white_kings}')    # debug
        #print(f'self.red_left = {self.red_left}')          # debug
        #print(f'self.red_kings = {self.red_kings}')        # debug
        if (row == ROWS - 1 or row == 0):   # last or 1st row of the board, make piece a KING
            aKing = piece.isKing()          # Check If Piece is already a King Piece (affects Minimax Score)
            #print(f'aKing = {aKing}')      # debug
            if aKing == False:
                piece.make_king()
                if piece.color == WHITE:
                    self.white_kings += 1
                else:
                    self.red_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self): # draw out checker piece arrangements: 3 total rows of 12 total pieces
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else: # add a zero instead to keep track of the board
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        else:
            return None

    def get_valid_moves(self, piece):
        moves = {}
        left  = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king: # determine valid direction of movement
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves # returns a dictionary

    def _traverse_left(self, start, stop, step, color, left, skipped=[]): # step = up or down
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0: # found an empty square
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break # just in case ??
            elif current.color == color: # if its a friendly square
                break # do nothing, not a valid move
            else:
                last = [current]

            left -= 1
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0: # found an empty square
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break # just in case ??
            elif current.color == color: # if its a friendly square
                break # do nothing, not a valid move
            else:
                last = [current]
            
            right += 1
        return moves