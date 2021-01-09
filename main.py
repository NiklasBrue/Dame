import pygame as pg
from dame.constants import WIDTH, HEIGHT, SQR_SIZE
from dame.colors import WHITE
from dame.game import Game
from minimax.algorithm import minimax

opponent = input('What opponent would you like to have? (P/AI) ')
if opponent == 'AI' or opponent == 'ai':
    DEPTH = int(input('How strong should it be? (1-4) '))

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

def main(opponent):
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
            game_over = True

        if opponent == 'AI' or opponent == 'ai':
            if game.turn == WHITE:
                score, new_board = minimax(game.get_board(), DEPTH, WHITE, game)
                game.ai_move(new_board)

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    game.restart()

            if event.type == pg.QUIT:
                game_over = True

            if event.type == pg.MOUSEBUTTONDOWN:
                row, col = get_piece_position_from_mouse(pg.mouse.get_pos())
                game.select(row, col)

        game.update()

    pg.quit()



main(opponent)