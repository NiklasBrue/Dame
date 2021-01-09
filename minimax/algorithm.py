import pygame as pg
from copy import deepcopy
from dame.colors import BLACK, WHITE, RED

def minimax(board_config, depth: int, max_player: bool, game, DRAW_MOVES=False):
    '''
    function that is called recursively until the depth reaches 0
    after (depth) iterations the function returns the best score and the best move for the AI
    '''
    if depth == 0 or board_config.winner() != None:
        return board_config.evaluate(), board_config

    if max_player:
        MAX_EVAL = float('-inf')
        best_move = None
        for move in get_all_valid_moves(board_config, WHITE, game, DRAW_MOVES):
            evaluation = minimax(move, depth-1, False, game)[0] # only take the first entry of the minimax return 
            MAX_EVAL = max(MAX_EVAL, evaluation)
            if MAX_EVAL == evaluation:
                best_move = move
        return MAX_EVAL, best_move
    else:
        MIN_EVAL = float('inf')
        best_move = None
        for move in get_all_valid_moves(board_config, BLACK, game, DRAW_MOVES):
            evaluation = minimax(move, depth-1, True, game)[0] # only take the first entry of the minimax return 
            MIN_EVAL = min(MIN_EVAL, evaluation)
            if MIN_EVAL == evaluation:
                best_move = move
        return MIN_EVAL, best_move

def simulate_move_of_piece(piece, move, board_config, game, skip):
    '''
    given a (piece) and a (move) return the new (board_config) keeping in mind
    that if a piece is skipped it has to be deleted
    '''
    board_config.move(piece, move[0], move[1])
    if skip:
        board_config.remove(skip)
    return board_config

def get_all_valid_moves(board_config, color, game, DRAW_MOVES=False):
    '''
    returns an array of shape [board, board, ...] i.e 
    if we move (piece) it results in (board)
    '''
    moves = []
    for piece in board_config.get_all_pieces(color):
        valid_moves = board_config.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            if DRAW_MOVES:
                draw_moves(game, board_config, piece)
            tmp_board = deepcopy(board_config)
            tmp_piece = tmp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move_of_piece(tmp_piece, move, tmp_board, game, skip)
            moves.append(new_board)

    return moves


def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.screen)
    pg.draw.circle(game.screen, RED, (piece.board_x_coord, piece.board_y_coord), 50, 5)
    game.draw_valid_moves(valid_moves.keys()) #passes the keys (row, col) from the dictionnary
    pg.display.update()
    #pg.time.delay(100)