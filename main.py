import pygame as pg
import time
from dame.constants import WIDTH, HEIGHT, SQR_SIZE
from dame.colors import D_BROWN, L_BROWN, BLACK, WHITE, BLUE
from dame.board import Board
from dame.piece import Piece
from dame.game import Game


SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('DAME')
pg.font.init()


def get_piece_position_from_mouse(mouse_position):
    '''
    get the position in the array given the clicking of the mouse button using int division
    '''
    x, y = mouse_position
    row = y // SQR_SIZE
    col = x // SQR_SIZE
    return row, col

def main():
    '''
    main loop of the game    
    '''
    game_over = False
    clock = pg.time.Clock() #define fps
    game = Game(SCREEN)

    while not game_over:
        clock.tick(30)

        if game.winner() != None:
            print(game.winner())
            break

        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_over = True

            if event.type == pg.MOUSEBUTTONDOWN:
                row, col = get_piece_position_from_mouse(pg.mouse.get_pos())
                game.select(row, col)

        game.update()

    pg.quit()

main()