import pygame
import pygame as pg
import BackEnd
from pygame.locals import *
import os

pg.init()  # we do this to initialize all imported pygame modules
board_pixel_size = 512 + 200
num_of_rows = 8
tile_size = (board_pixel_size - 200) // num_of_rows  # 512 pixels divided by 8 rows
chess_piece_images = {}  # we use this to store the images of the chess pieces
cwd = os.getcwd()
black = (0, 0, 0)
brown = (193, 154, 107)  #########################
blue = (0, 0, 128)
yellow = (255, 255, 0)
blue = (0, 125, 255)
red = (255, 0, 0)
green = (0, 255, 0)
orange = (255, 100, 0)
white = (255, 255, 255)


# print(tile_size)
def load_images():
    global chess_Rpiece_images
    """
    We are creating a dictionary of callable images so we can easily reference them throughout the code.
    """
    chess_pieces = ['BR', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BR', "BP", "WR", "WN", "WB", "WQ", "WK", "WB", "WN",
                    "WR", "WP"]
    chess_Rpiece_images = {}
    for piece in chess_pieces:
        chess_piece_images[piece] = pg.transform.scale(pg.image.load("images/" + piece + ".png"),
                                                       (tile_size, tile_size))
        chess_Rpiece_images[piece] = pg.transform.scale(pg.image.load("images/" + piece + ".png"),
                                                        (48, 48))
    # print(chess_piece_images)

"""def main():
    1. creates a pg window with "Chess game" and start here for timer start here for regular
    2. user clicks the button
    3. calls the function below
    4. destroy the existing screen"""


def main():
    # pg.init()
    # Here##############################
    screen = pg.display.set_mode(
        (board_pixel_size, board_pixel_size - 200))  # initializes a screen for display with size 512x512
    # screen.fill(pg.Color("white"))
    screen.fill(brown)
    chess_game = BackEnd.Chess()
    valid_moves = chess_game.get_valid_moves()
    move_made = False  # flag variable for when a move is made
    load_images()
    selected_square = ()  # stores the column and row of the tile that was selected
    draw_chess_game(screen, chess_game, valid_moves, selected_square)
    clock = pg.time.Clock()
    running = True
    player_click = []  # this will be two tuples, where the first tuple is the first selected tile and the second
    # tuple is where the user wants to move the chess piece

    ############   To change timer limit just change timer1 and timer2 ##################3333
    play_time = 30
    timer1 = play_time
    timer2 = play_time
    framCoun1 = 0
    framCoun2 = 0
    fram = 15
    tStr1 = tStr2 = "{0:02d}:{1:02d}".format(30, 0)
    Text(screen, tStr1, 0, 50, white)
    Text(screen, tStr2, 2 * (board_pixel_size) - 200, 50, black)

    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
                exit()
            # mouse handler
            elif e.type == pg.MOUSEBUTTONDOWN:
                location1 = pg.mouse.get_pos()  # stores the (x,y) coordinates of the mouse
                location = location1[0] - 100, location1[1]  # Here###############################3
                col = location[
                          0] // tile_size  # By dividing the x location by the tile_size, we get the integer value of
                # the function
                row = location[1] // tile_size
                # print(row,col)
                if selected_square == (row, col):  # we check here to see if the user selected the same tile twice
                    # if the user did select the same tile twice, then we want to unselect
                    selected_square = ()  # deselects the tile
                    player_click = []  # clears where the player clicked
                else:
                    selected_square = (row, col)
                    player_click.append(selected_square)  # storing the clicks (1st and 2nd)
                if len(player_click) == 2:  # we only want to make the move if the user clicked 2 separate tiles
                    move = BackEnd.Move(player_click[0], player_click[1], chess_game.board)
                    print(move.get_chess_notation())
                    if move in valid_moves:
                        chess_game.make_move(move, 0)
                        move_made = True
                    selected_square = ()
                    player_click = []

            # key handler
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_u:  # undo the move when u is pressed
                    chess_game.undo_move(0)
                    screen.fill(brown)
                    drawRemoved(screen, chess_game.removed, chess_Rpiece_images)
                    move_made = True  # sets this back to True so move_made function works properly

        if move_made:  # we do not want to run the logic to get the valid moves on every action. Only when a valid
            # move is made. Therefore, we have this IF statement and the move_made variable to control that.
            valid_moves = chess_game.get_valid_moves()
            move_made = False

        if chess_game.white_to_move:
            tSec = timer1 * 60 - framCoun1 // fram
            tMin = tSec // 60
            tss = tSec % 60
            if tss <= 0:
                tss = 0
            if tMin <= 0:
                tMin = 0
            framCoun1 += 1
            tStr1 = "{0:02d}:{1:02d}".format(int(tMin), int(tss))


        elif not chess_game.white_to_move:
            tSec = timer2 * 60 - framCoun2 // fram
            tMin = tSec // 60
            tss = tSec % 60
            if tss <= 0:
                tss = 0
            if tMin <= 0:
                tMin = 0
            tStr2 = "{0:02d}:{1:02d}".format(int(tMin), int(tss))
            framCoun2 += 1
        Text(screen, tStr1, 0, 50, white)
        Text(screen, tStr2, 2 * (board_pixel_size) - 200, 50, black)
        drawRemoved(screen, chess_game.removed, chess_Rpiece_images)
        Text(screen, 'White', 0, 0, white)
        draw_chess_game(screen, chess_game, valid_moves, selected_square)
        Text(screen, 'Black', 2 * (board_pixel_size) - 200, 0, black)
        gameEnd(screen, chess_game, timer1 * 60 - framCoun1 // fram, timer2 * 60 - framCoun2 // fram)
        clock.tick(fram)
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
    colors = [pg.Color("white"), pg.Color("gray")]
    for row in range(num_of_rows):
        for col in range(num_of_rows):
            color = colors[((row + col) % 2)]
            # Here#############
            pg.draw.rect(screen, color, pg.Rect(100 + col * tile_size, row * tile_size, tile_size,
                                                tile_size))  # this moves along the columns and rows by using TILE_SIZE


def draw_pieces(screen, board):
    """
    Draws the pieces on the board by referencing the instance of the Board class from BackEnd
    """
    for row in range(num_of_rows):
        for col in range(num_of_rows):
            chess_piece = board[row][col]
            # Here#############
            if chess_piece != "--":  # we only want to draw a piece on a non-empty tile
                screen.blit(chess_piece_images[chess_piece],
                            pg.Rect(100 + col * tile_size, row * tile_size, tile_size, tile_size))


def gameEnd(screen, chess_game, tim1, tim2):
    if chess_game.check_mate or chess_game.stale_mate or tim1 <= 0 or tim2 <= 0:
        print('yes')
        pos = (board_pixel_size) // 2 + 250, (board_pixel_size) // 2 + 100
        clr, clr2 = red, blue
        while True:
            if chess_game.check_mate:
                if chess_game.white_to_move:
                    clr = black
                    clr2 = white
                    txt = 'Black won'
                elif not chess_game.white_to_move:
                    clr = white
                    clr2 = black
                    txt = 'White won'
                Text(screen, txt + ' by Check Mate', *pos, clr)
            elif chess_game.stale_mate:
                Text(screen, 'Match ends in draw due to Stalemate', *pos, clr, clr2)
            elif tim1 <= 0:
                clr = black
                clr2 = white
                txt = 'Black won. White lost by timeout'
                Text(screen, txt, *pos, clr, clr2)
            elif tim2 <= 0:
                clr = white
                clr2 = black
                txt = 'White won. Black lost by timeout'
                Text(screen, txt, *pos, clr, clr2)
            Text(screen, 'Press Escape', pos[0], pos[1] + 50, clr, clr2)
            pg.display.flip()
            for e in pg.event.get():
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        main()
                if e.type == pg.QUIT:
                    exit()


def Text(screen, txt, X, Y, colr, bcolr=brown):
    font = pygame.font.Font('freesansbold.ttf', 20)

    # create a text surface object,
    # on which text is drawn on it.
    text = font.render(txt, True, colr, bcolr)

    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()

    # set the center of the rectangular object.
    textRect.center = ((X + 100) // 2, (Y + 50) // 2)

    # completely fill the surface object
    # with white color

    # copying the text surface object
    # to the display surface object
    # at the center coordinate.
    screen.blit(text, textRect)
    # time.sleep(2)


def drawRemoved(screen, removed, chess_Rpiece_images):
    counW = 0
    counB = 0
    W, B = (2, 100), (board_pixel_size - 100 + 2, 100)
    indx = 0
    # if len(removed)==0:
    #    screen.blit()
    for piece in removed:
        # print(removed)
        if piece[0] == 'B':
            counW += 1
            screen.blit(chess_Rpiece_images[piece],
                        pg.Rect(W[0], W[1], 48, 48))
            W = W[0] + 50, W[1]
            if counW % 2 == 0:
                W = (2, W[1] + 50)
        elif piece[0] == 'W':
            counB += 1
            screen.blit(chess_Rpiece_images[piece],
                        pg.Rect(B[0], B[1], 48, 48))
            B = B[0] + 50, B[1]
            if counB % 2 == 0:
                B = (board_pixel_size - 100 + 2, B[1] + 50)
        indx += 1

def highlight_squares(screen, chess_game, valid_moves, selected_square):
    """	
    This will highlight the selected square and then show in a different highlighted color, the possible moves for that	
    piece. Need to add try and except exception clause to avoid errors.	
    """
    if selected_square != ():
        row, col = selected_square
        if chess_game.board[row][col][0] == ('W' if chess_game.white_to_move else "B"):
        # We need to make sure the selected square is a piece that can be moved on the user's turn.
        # We can use an if statement inside an if statement to keep it short
            h = pg.Surface((tile_size, tile_size))
            h.set_alpha(125) # this sets the level of transparency (0 to 255)
            h.fill(pg.Color('blue')) # chooses the color of the piece
            screen.blit(h, (100 + col * tile_size, row * tile_size)) # places the color defined above on the tile
            # we also need to highlight the moves of that square
            h.fill(pg.Color('red')) # chooses the color of the possible moves
            for move in valid_moves:
                if move.start_row == row and move.start_col == col: # this means that the move is starting from the piece
                    screen.blit(h, (100 + move.end_col * tile_size, move.end_row * tile_size))

if __name__ == "__main__":
    main()
