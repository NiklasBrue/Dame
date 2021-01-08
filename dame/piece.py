import pygame as pg
from .colors import WHITE, BLACK, CROWN
from .constants import WIDTH, HEIGHT, SQR_SIZE, COLS, ROWS

class Piece():

    def __init__(self, row, col, color):
        '''
        position of the piece on the board and in the array, the color, 
        the possible direction the piece can go (down for white, up for black),
        if it is a queen
        '''
        self.row = row
        self.col = col
        self.color = color
        self.is_queen = False
        #these features do not have to be given when defining a piece,
        #they can be computed from the given information
        self.board_x_coord = 0
        self.board_y_coord = 0
        self.calculate_position_on_board()

    def __repr__(self):
        return "Piece: position=({},{}), color={}, queen={}".format(self.row, self.col, self.color, self.is_queen)


    def calculate_position_on_board(self):
        '''
        returns the center of the piece on the board given its row and col in the array
        '''
        self.board_x_coord = self.col*SQR_SIZE + SQR_SIZE//2
        self.board_y_coord = self.row*SQR_SIZE + SQR_SIZE//2

    def transition_to_queen(self):
        '''
        transitions the chosen piece from a pawn to a queen
        '''
        self.is_queen = True

    def draw_piece(self, screen):
        if self.color == BLACK:
            pg.draw.circle(screen, WHITE, (self.board_x_coord, self.board_y_coord), 43)
        else: 
            pg.draw.circle(screen, BLACK, (self.board_x_coord, self.board_y_coord), 43)
        pg.draw.circle(screen, self.color, (self.board_x_coord, self.board_y_coord), 40)
        if self.is_queen:
            screen.blit(CROWN, (self.board_x_coord - CROWN.get_width()/2, self.board_y_coord - CROWN.get_height()/2))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calculate_position_on_board()
