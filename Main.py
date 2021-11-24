import pygame
import pygame as pg
from Chess import BackEnd

pg.init()  # we do this to initialize all imported pygame modules
board_pixel_size = 512
num_of_rows = 8
tile_size = board_pixel_size // num_of_rows  # 512 pixels divided by 8 rows
chess_piece_images = {}  # we use this to store the images of the chess pieces

def load_images():
    """
    We are creating a dictionary of callable images so we can easily reference them throughout the code.
    """
    chess_pieces = ['BR', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BR', "BP", "WR", "WN", "WB", "WQ", "WK", "WB", "WN",
                    "WR", "WP"]
    for piece in chess_pieces:
        chess_piece_images[piece] = pg.transform.scale(pg.image.load("images/" + piece + ".png"),
                                                       (tile_size, tile_size))
def main():
    # pg.init()
    screen = pg.display.set_mode(
        (board_pixel_size, board_pixel_size))  # initializes a screen for display with size 512x512
    screen.fill(pg.Color("white"))
    chess_game = BackEnd.Chess()
    valid_moves = chess_game.get_valid_moves()
    move_made = False  # flag variable for when a move is made
    load_images()
    selected_square = ()  # stores the column and row of the tile that was selected
    draw_chess_game(screen, chess_game, valid_moves, selected_square)
    clock = pg.time.Clock()
    running = True
    player_click = [] # this will be two tuples, where the first tuple is the first selected tile and the second
    # tuple is where the user wants to move the chess piece

    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            # mouse handler
            elif e.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos()  # stores the (x,y) coordinates of the mouse
                col = location[
                          0] // tile_size  # By dividing the x location by the tile_size, we get the integer value of
                # the function
                row = location[1] // tile_size
                if selected_square == (row,col): # we check here to see if the user selected the same tile twice
                    # if the user did select the same tile twice, then we want to unselect
                    selected_square = () # deselects the tile
                    player_click = [] # clears where the player clicked
                else:
                    selected_square = (row,col)
                    player_click.append(selected_square) # storing the clicks (1st and 2nd)
                if len(player_click) == 2: # we only want to make the move if the user clicked 2 separate tiles
                    move = BackEnd.Move(player_click[0], player_click[1], chess_game.board)
                    print(move.get_chess_notation())
                    if move in valid_moves:
                        chess_game.make_move(move)
                        move_made = True
                    selected_square = ()
                    player_click = []

            # key handler
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_u: # undo the move when u is pressed
                    chess_game.undo_move()
                    move_made = True # sets this back to True so move_made function works properly

        if move_made: # we do not want to run the logic to get the valid moves on every action. Only when a valid
                        # move is made. Therefore, we have this IF statement and the move_made variable to control that.
            valid_moves = chess_game.get_valid_moves()
            move_made = False

        draw_chess_game(screen, chess_game, valid_moves, selected_square)
        clock.tick(15)
        pg.display.flip()

def draw_chess_game(screen, chess_game, valid_moves, selected_square):
    """
    Creates the chess game with the board and pieces
    """
    draw_board(screen)  # draw tiles
    highlight_squares(screen, chess_game, valid_moves, selected_square)
    draw_pieces(screen, chess_game.board)  # draw pieces on top of the tiles


def draw_board(screen):
    """
    Draws the tiles on the board by looping through 8 rows and columns
    """
    colors = [pg.Color(235,232,206), pg.Color(122,148,85)]
    for row in range(num_of_rows):
        for col in range(num_of_rows):
            color = colors[((row + col) % 2)]
            pg.draw.rect(screen, color, pg.Rect(col * tile_size, row * tile_size, tile_size,
                                                tile_size))  # this moves along the columns and rows by using TILE_SIZE


def draw_pieces(screen, board):
    """
    Draws the pieces on the board by referencing the instance of the Board class from BackEnd
    """
    for row in range(num_of_rows):
        for col in range(num_of_rows):
            chess_piece = board[row][col]
            if chess_piece != "--":  # we only want to draw a piece on a non-empty tile
                screen.blit(chess_piece_images[chess_piece],
                            pg.Rect(col * tile_size, row * tile_size, tile_size, tile_size))

def highlight_squares(screen, chess_game, valid_moves, selected_square):
    """
    This will highlight the selected square and then show in a different highlighted color, the possible moves for that
    piece.
    """
    if selected_square != ():
        row, col = selected_square
        if chess_game.board[row][col][0] == ('W' if chess_game.white_to_move else "B"):
        # We need to make sure the selected square is a piece that can be moved on the user's turn.
        # We can use an if statement inside an if statement to keep it short
            h = pg.Surface((tile_size, tile_size))
            h.set_alpha(125) # this sets the level of transparency (0 to 255)
            h.fill(pg.Color('blue')) # chooses the color of the piece
            screen.blit(h, (col * tile_size, row * tile_size)) # places the color defined above on the tile
            # we also need to highlight the moves of that square
            h.fill(pg.Color('red')) # chooses the color of the possible moves
            for move in valid_moves:
                if move.start_row == row and move.start_col == col: # this means that the move is starting from the piece
                    screen.blit(h, (move.end_col * tile_size, move.end_row * tile_size))

if __name__ == "__main__":
    main()
