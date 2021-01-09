import pygame as pg
from .colors import BLACK, D_BROWN, L_BROWN, WHITE #relative import of the defined colors
from .constants import WIDTH, HEIGHT, ROWS, COLS, SQR_SIZE
from .piece import Piece

class Board:
    def __init__(self):
        '''
        init contains the components of the array behind the board, 
        which piece is selected, the number of black/white pieces/queens
        '''
        self.board = []
        self.white_pieces_left = 12
        self.black_pieces_left = 12
        self.white_queens = 0
        self.black_queens = 0
        self.create_board()
    
    def __repr__(self):
        return "Board={}".format(self.board)

    def draw_black_white_squares(self, screen):
        '''
        draws the board, this only includes the dark and light brown squares
        '''
        screen.fill(D_BROWN)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2): #fills the board like a checker board
                pg.draw.rect(screen, L_BROWN, (row*SQR_SIZE, col*SQR_SIZE, SQR_SIZE, SQR_SIZE))

    def create_board(self):
        '''
        draws initial position of the black and white pieces onto the board
        '''
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, BLACK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, screen):
        '''
        draws the board and the pieces
        '''
        self.draw_black_white_squares(screen)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw_piece(screen)

    def get_piece(self, row, col):
        return self.board[row][col]

    def move(self, piece, row, col):
        '''
        move the piece from its position to the position given by row and col
        '''
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col] 
        piece.move(row, col)
        if row == ROWS-1 or row == 0:
            piece.transition_to_queen()
            if piece.color == WHITE:
                self.white_queens += 1
            else:
                self.black_queens += 1

    def remove(self, pieces):
        '''
        remove pieces by setting them to zero
        '''
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == WHITE:
                    self.white_pieces_left -= 1
                else:
                    self.black_pieces_left -= 1

    def winner(self):
        if self.white_pieces_left <= 0:
            return 'BLACK has won'
        elif self.black_pieces_left <= 0:
            return 'WHITE has won'
        return None


    # def get_valid_moves(self, piece):
    #     '''
    #     returns a dictionary containing all the possible moves given a state of the game and a selected piece
    #     '''
    #     valid_moves = {}
    #     left = piece.col - 1 #what col is left of the chosen piece
    #     right = piece.col - 1 #what col is right of the chosen piece
    #     row = piece.row #in what row is the piece

    #     if piece.color == WHITE or piece.is_queen:
    #         #start at the row below the current one: row+1
    #         #stop at the min between row+3 (2 rows below the starting position) and ROWS 
    #         #the steping direction is 1
    #         #right is where we start to get the next col
    #         valid_moves.update(self.left_diagonal(row+1, min(row+3, ROWS), 1, piece.color, left))
    #         valid_moves.update(self.right_diagonal(row+1, min(row+3, ROWS), 1, piece.color, right))
    #     if piece.color == BLACK or piece.is_queen:
    #         #start at the row above the current one: row-1
    #         #stop at the maximum between row-3 (2 rows above the starting position) and -1 
    #         #the steping direction is -1
    #         #left is where we start to get the next col
    #         valid_moves.update(self.left_diagonal(row-1, max(row-3, -1), -1, piece.color, left))
    #         valid_moves.update(self.right_diagonal(row-1, max(row-3, -1), -1, piece.color, right))

    #     return valid_moves

    # def left_diagonal(self, start, stop, step, color, left, skipped=[]):
    #     '''
    #     moving possibilities in the left diagonal of a piece
    #     '''
    #     valid_moves = {}
    #     last = []
    #     for r in range(start, stop, step):
    #         if left < 0: #if the left col is outside of the board
    #             break 
    #         current = self.board[r][left]
    #         if current == 0: #this means that we found an empty sqr
    #             if skipped and not last:
    #                 break
    #             elif skipped:
    #                 valid_moves[(r, left)] = last + skipped
    #             else: 
    #                 valid_moves[(r, left)] = last #the move is added to the valid moves
    #             if last: #here we go when we skipped over some piece and check if we can double or triple jump
    #                 if step == -1: #recalculate the row given that we have made a first jump
    #                     row = max(r-3, 0)
    #                 else:
    #                     row = min(r+3, ROWS)
    #                 valid_moves.update(self.left_diagonal(r+step, row, step, color, left-1, skipped=last))
    #                 valid_moves.update(self.right_diagonal(r+step, row, step, color, left+1, skipped=last))
    #             break
    #         elif current.color == color: #if the color is equal to the current color we cant move in this direction
    #             break
    #         else: #if it was not the current color then it is the other color and we go back into the first if state
    #             last = [current]

    #         left -= 1 
    #     return valid_moves

    # def right_diagonal(self, start, stop, step, color, right, skipped=[]):
    #     '''
    #     moving possibilities in the right diagonal of a piece
    #     '''
    #     valid_moves = {}
    #     last = []
    #     for r in range(start, stop, step):
    #         if right >= COLS: #if the left col is outside of the board
    #             break 
    #         current = self.board[r][right]
    #         if current == 0: #this means that we found an empty sqr
    #             if skipped and not last:
    #                 break
    #             elif skipped:
    #                 valid_moves[(r, right)] = last + skipped
    #             else: 
    #                 valid_moves[(r, right)] = last #the move is added to the valid moves
    #             if last: #here we go when we skipped over some piece and check if we can double or triple jump
    #                 if step == -1: #recalculate the row given that we have made a first jump
    #                     row = max(r-3, 0)
    #                 else:
    #                     row = min(r+3, ROWS)
    #                 valid_moves.update(self.left_diagonal(r+step, row, step, color, right-1, skipped=last))
    #                 valid_moves.update(self.right_diagonal(r+step, row, step, color, right+1, skipped=last))
    #             break
    #         elif current.color == color: #if the color is equal to the current color we cant move in this direction
    #             break
    #         else: #if it was not the current color then it is the other color and we go back into the first if state
    #             last = [current]

    #         right += 1 
    #     return valid_moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
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
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves

    def get_valid_moves(self, piece):
        '''
        returns a dictionary containing the valid moves of a given piece
        '''
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == BLACK or piece.is_queen:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.is_queen:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
    
        return moves

    def get_all_pieces(self, color):
        '''
        returns all the pieces of a color
        '''
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def evaluate(self):
        '''
        determines the score of the board, this is used in the minimax function
        '''
        score = self.white_pieces_left - self.black_pieces_left + (self.white_queens*0.5) - (self.black_queens*0.5)
        return score
