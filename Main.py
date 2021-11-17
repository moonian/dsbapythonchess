import pygame as pg
from Chess import BackEnd

pg.init()  # we do this to initialize all imported pygame modules
tile_size = 64  # 512 pixels divided by 8 rows
chess_piece_images = {}  # we use this to store the images of the chess pieces


def load_images():
    """
    We are creating a dictionary of callable images so we can easily reference them throughout the code.
    """
    chess_pieces = ['BR', 'BKn', 'BB', 'BQ', 'BK', 'BB', 'BKn', 'BR', "BP", "WR", "WKn", "WB", "WQ", "WK", "WB", "WKn",
                    "WR", "WP"]
    for piece in chess_pieces:
        chess_piece_images[piece] = pg.transform.scale(pg.image.load("images/" + piece + ".png"),
                                                       (tile_size, tile_size))
def main():
    # pg.init()
    screen = pg.display.set_mode(
        (512, 512))  # initializes a screen for display with size 512x512
    screen.fill(pg.Color("white"))
    chess_game = BackEnd.Chess()
    load_images()
    draw_chess_game(screen, chess_game)
    clock = pg.time.Clock()
    running = True
    selected_square = ()  # stores the column and row of the tile that was selected
    player_click = [] # this will be two tuples, where the first tuple is the first selected tile and the second
    # tuple is where the user wants to move the chess piece

    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
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
                    chess_game.make_move(move)
                    selected_square = ()
                    player_click = []

        draw_chess_game(screen, chess_game)
        clock.tick(15)
        pg.display.flip()

def draw_chess_game(screen, chess_game):
    """
    Creates the chess game with the board and pieces
    """
    draw_board(screen)  # draw tiles
    draw_pieces(screen, chess_game.board)  # draw pieces on top of the tiles


def draw_board(screen):
    """
    Draws the tiles on the board by looping through 8 rows and columns
    """
    colors = [pg.Color("white"), pg.Color("gray")]
    for row in range(8):
        for col in range(8):
            color = colors[((row + col) % 2)]
            pg.draw.rect(screen, color, pg.Rect(col * tile_size, row * tile_size, tile_size,
                                                tile_size))  # this moves along the columns and rows by using TILE_SIZE


def draw_pieces(screen, board):
    """
    Draws the pieces on the board by referencing the instance of the Board class from BackEnd
    """
    for row in range(8):
        for col in range(8):
            chess_piece = board[row][col]
            if chess_piece != "--":  # we only want to draw a piece on a non-empty tile
                screen.blit(chess_piece_images[chess_piece],
                            pg.Rect(col * tile_size, row * tile_size, tile_size, tile_size))


if __name__ == "__main__":
    main()
