import pygame as pg
from .constants import SQR_SIZE, COLS, ROWS, HEIGHT, WIDTH
from .colors import BLACK, WHITE, BLUE
from .board import Board
from .piece import Piece


class Game:
    def __init__(self, screen):
        '''
        initialises the class with following parameters: the selcted piece, the active player, a dictionnary of valid moves
        '''
        self._init()
        self.screen = screen

    def __repr__(self):
        if self.turn == WHITE:
            return "Game: Turn={}, Winner={}"\
                .format('WHITE', self.winner())
        else:
            return "Game: Turn={}, Winner={}"\
                .format('BLACK', self.winner())


    def _init(self):
        self.selection = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = {}

    def update(self):
        '''
        this updates the array and the display
        '''
        self.board.draw(self.screen)
        self.draw_valid_moves(self.valid_moves)
        pg.display.update()

    def select(self, row, col):
        '''
        here there are two possibilities: either a piece is already selected so the action is to select a row, col where it is to be moved to
        or no piece is selected in this case selection selects that piece
        '''            
        if self.selection:
            result = self._move(row, col)
            if not result:
                self.selection = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selection = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        '''
        '''
        piece = self.board.get_piece(row, col)
        if self.selection and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selection, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
            #print('DEBUG turn', self.turn)
        else:
            return False
        return True

    def change_turn(self):
        '''
        changes the variable turn from white to black and from black to white
        '''
        self.valid_moves = {}
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def draw_valid_moves(self, valid_moves):
        for move in valid_moves:
            row, col = move
            pg.draw.circle(self.screen, BLUE, (col*SQR_SIZE+SQR_SIZE/2, row*SQR_SIZE+SQR_SIZE/2), 10)

    def winner(self):
        return self.board.winner()

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()

    def restart(self):
        self._init()