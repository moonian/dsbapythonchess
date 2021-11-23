from typing import Dict


class Chess():
    """
    Defines the current game state of
    """

    def __init__(self):
        # Create an 8x8 2D list with each element of the list representing a piece. The first character is
        # the team of the piece. The second character is the piece.
        self.board = [
            ["BR", "BN", "BB", "BQ", "BK", "BB", "BN", "BR"],
            ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
            ["WR", "WN", "WB", "WQ", "WK", "WB", "WN", "WR"]]
        self.white_to_move = True
        self.move_log = []  # We want to store the moves so that we can undo moves later on

    def make_move(self, move):
        """
        This function moves the chess piece by leaving behind an empty piece and updating the board with the
        new location. We also log the move in the move_log list created before. Finally, we switch the turn of the
        player. This fucntion does not work for castling, pawn promotion, and en-passant.
        """
#        if self.board[move.start_row][move.start_col] != "--":
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.active_piece
        self.move_log.append(move)
        # swaps the player's turn
#        if self.white_to_move == True:
#            self.white_to_move = False
#        if self.white_to_move == False:
#            self.white_to_move = True
        self.white_to_move = not self.white_to_move

    def undo_move(self):
        """
        This function undos the move, first checking to see if there is a move to undo.
        """
        if len(self.move_log) != 0: # we need to make sure there is a move to undo
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.active_piece
            self.board[move.end_row][move.end_col] = move.moved_location
            self.white_to_move = not self.white_to_move # switch the turn back to the player that just moved

    def get_valid_moves(self):
        """
        All moves considering checks.
        """
        return self.all_possible_moves()

    def all_possible_moves(self):
        """
        Helper function,which returns all moves not considering checks.
        """
        moves = [Move((6,4),(4,4),self.board)]
        for row in range(len(self.board)): # number of rows
            for col in range(len(self.board[row])): # number of columns in a given row
                turn = self.board[row][col][0] # the first character of chess piece represents the player's team
                if (turn == "W" and self.white_to_move) or (turn == "B" and not self.white_to_move):
                # only check if the piece matches the turn of the player
                    piece = self.board[row][col][1] # identifies the piece
                    if piece == "P":
                        self.pawn_moves(row, col, moves)
                    elif piece == "R":
                        self.rook_moves(row, col, moves)
                    elif piece == "N":
                        self.knight_moves(row, col, moves)
                    elif piece == "B":
                        self.bishop_moves(row, col, moves)
                    elif piece == "Q":
                        self.queen_moves(row, col, moves)
                    elif piece == "K":
                        self.king_moves(row, col, moves)
        return moves

    def pawn_moves(self, row, col, moves):
        """
        gets all moves for the pawn located at the row and column, and then adds it to the move list
        """
        if self.white_to_move: # available moves for white pawn
            if self.board[row - 1][col] == '--': # if the row is empty above it, add the move to the moves list
                moves.append(Move((row, col), (row - 1, col),self.board))
                if row == 6 and self.board[row - 2][col] == '--': # if pawn is at the starting position, then it can move two
                    moves.append(Move((row, col), (row - 2, col),self.board))
            if col >= 1: # Left diagonal captures should only happen for pawns in col 1 or higher
                if self.board[row - 1][col - 1][0] == "B": # Allows pawn to capture left diagonally
                    moves.append(Move((row, col), (row - 1, col - 1), self.board))
            if col <= 6: # Right diagonal captures should only happen for pawns in col 6 or lower
                if self.board[row - 1][col + 1][0] == "B": # Allows pawn to capture right diagonally
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))
        if not self.white_to_move:
            if self.board[row + 1][col] == '--':
                moves.append(Move((row, col), (row + 1, col), self.board))
                if row == 1 and self.board[row + 2][col] == '--':
                    moves.append(Move((row, col), (row + 2, col), self.board))
            if col >= 1: # Left diagonal capture for black pawn
                if self.board[row + 1][col - 1][0] == 'W':
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))
            if col <= 6: # Right diagonal capture for black pawn
                if self.board[row + 1][col + 1][0] == 'W':
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))

    def rook_moves(self, row, col, moves):
        """
        gets all moves for the rook located at the row and column, and then adds it to the move list
        """
        directions = [1, -1]
        for element in directions:
            if self.white_to_move:
                for _ in range(1, 8):
                    end_row = row + element * _ # starting with the up and down directions
                    if 0 <= end_row <= 7: # makes sure the piece is on the board
                        end_piece = self.board[end_row][col]
                        if end_piece == '--': # if the space is empty, that is a valid move
                            moves.append(Move((row, col), (end_row, col), self.board))
                        elif end_piece[0] == 'B':
                            # if the space is an enemy, it is the last valid move in this direction
                            moves.append(Move((row, col), (end_row, col), self.board))
                            break # this breaks out of the for loop and moves to the next direction
                        else: # should break if we see a white piece and move to the next direction
                            break
                for _ in range(1, 8):
                    end_col = col + element * _ # starting with the up and down directions
                    if 0 <= end_col <= 7: # makes sure the piece is on the board
                        end_piece = self.board[row][end_col]
                        if end_piece == '--': # if the space is empty, that is a valid move
                            moves.append(Move((row, col), (row, end_col), self.board))
                        elif end_piece[0] == 'B':
                            # if the space is an enemy, it is the last valid move in this direction
                            moves.append(Move((row, col), (row, end_col), self.board))
                            break # this breaks out of the for loop and moves to the next direction
                        else: # should break if we see a white piece and move to the next direction
                            break
            if not self.white_to_move:
                for _ in range(1, 8):
                    end_row = row + element * _  # starting with the up and down directions
                    if 0 <= end_row <= 7:  # makes sure the piece is on the board
                        end_piece = self.board[end_row][col]
                        if end_piece == '--':  # if the space is empty, that is a valid move
                            moves.append(Move((row, col), (end_row, col), self.board))
                        elif end_piece[0] == 'W':
                            # if the space is an enemy, it is the last valid move in this direction
                            moves.append(Move((row, col), (end_row, col), self.board))
                            break  # this breaks out of the for loop and moves to the next direction
                        else:  # should break if we see a white piece and move to the next direction
                            break
                for _ in range(1, 8):
                    end_col = col + element * _  # starting with the up and down directions
                    if 0 <= end_col <= 7:  # makes sure the piece is on the board
                        end_piece = self.board[row][end_col]
                        if end_piece == '--':  # if the space is empty, that is a valid move
                            moves.append(Move((row, col), (row, end_col), self.board))
                        elif end_piece[0] == 'W':
                            # if there is a white chess piece here, it is the last valid move in this direction
                            moves.append(Move((row, col), (row, end_col), self.board))
                            break  # this breaks out of the for loop and moves to the next direction
                        else:  # should break if we see a white piece and move to the next direction
                            break

    def knight_moves(self, row, col, moves):
        """
        gets all moves for the knight located at the row and column, and then adds it to the move list
        """
        row_col_moves = [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]
        # all the movements for the knight
        for direction in row_col_moves:
            if self.white_to_move:
                if 0 <= row + direction[0] <= 7 and 0 <= col + direction[1] <= 7: # make sure move is on the board
                    possible_tile = self.board[row + direction[0]][col + direction[1]] # possible move for the rook
                    if possible_tile == '--': # if the space is empty, this is a valid move
                        moves.append(Move((row, col), (row + direction[0], col + direction[1]), self.board))
                    elif possible_tile[0] == 'B':
                        # if there is a black chess piece here, it is a valid move
                        moves.append(Move((row, col), (row + direction[0], col + direction[1]), self.board))
            if not self.white_to_move:
                if 0 <= row + direction[0] <= 7 and 0 <= col + direction[1] <= 7: # make sure move is on the board
                    possible_tile = self.board[row + direction[0]][col + direction[1]] # possible move for rook
                    if possible_tile == '--': # if the space is empty, then this is a valid move
                        moves.append(Move((row,col), (row + direction[0], col + direction[1]), self.board))
                    elif possible_tile[0] == 'W':
                        # if there is a white piece then it's a valid move
                        moves.append(Move((row, col), (row + direction[0], col + direction[1]), self.board))


    def bishop_moves(self, row, col, moves):
        """
        gets all moves for the bishop located at the row and column, and then adds it to the move list
        """
        row_col_moves = [(1, 1), (-1, -1), (1, -1), (-1, 1)] # all the possible directions for bishop
        for direction in row_col_moves:
            for i in range(1,8): # maximum number of rows/columns the bishop can move
                if self.white_to_move: # only the moves for white
                    end_row = row + direction[0]*i
                    end_col = col + direction[1]*i
                    if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                        # make sure the move is on the board
                        possible_tile = self.board[end_row][end_col]
                        if possible_tile == '--': # if the tile is empty
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                        elif possible_tile[0] == 'B':
                            # if the space is an enemy, it is the last valid move in this direction
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                            break # this breaks out of the for loop and moves to the next direction
                        else: # should break if we see a white piece and move to the next direction
                            break
                if not self.white_to_move: # only the moves for black piece
                    end_row = row + direction[0]*i
                    end_col = col + direction[1]*i
                    if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                        # make sure the move is on the board
                        possible_tile = self.board[end_row][end_col]
                        if possible_tile == '--': # if the tile is empty
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                        elif possible_tile[0] == 'W':
                            # if the space is an enemy, it is the last valid move in this direction
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                            break # this breaks out of the for loop and moves to the next direction
                        else: # should break if we see a white piece and move to the next direction
                            break

    def queen_moves(self, row, col, moves):
        """
        gets all moves for the queen located at the row and column, and then adds it to the move list
        """
        self.bishop_moves(row, col, moves)
        self.rook_moves(row, col, moves)

    def king_moves(self, row, col, moves):
        """
        gets all moves for the king located at the row and column, and then adds it to the move list
        """
        for row_adder in range(-1, 2):
            for col_adder in range(-1, 2):
                if self.white_to_move: # moves for white king
                    if 0 <= row + row_adder <= 7 and 0 <= col + col_adder <= 7:
                        # checks to see if the move is on the board
                        possible_tile = self.board[row + row_adder][col + col_adder]  # possible move for king
                        if possible_tile == '--': # if the tile is empty then it's a valid move
                            moves.append(Move((row, col), (row + row_adder, col + col_adder), self.board))
                            print(Move((row, col), (row + row_adder, col + col_adder), self.board).move_ID)
                        elif possible_tile[0] == 'B': # if the tile is a black piece, then it's a valid move
                            moves.append(Move((row, col), (row + row_adder, col + col_adder), self.board))
class Move():
    def __init__(self, start_tile, end_tile, board):
        self.start_row = start_tile[0]
        self.start_col = start_tile[1]
        self.end_row = end_tile[0]
        self.end_col = end_tile[1]
        self.active_piece = board[self.start_row][self.start_col]  # represents the start location of the selected piece
        self.moved_location = board[self.end_row][self.end_col]  # represents the end location of the selected piece
        self.move_ID = self.start_row * 1000 + self.start_col * 100 + self.end_row*10 + self.end_col # gives us a unique
            # MoveID where the first two digits represent the start row, column and then latter two represent the end
            # row, col

    row_to_rank = {7: "1", 6: "2", 5: "3", 4: "4", 3: "5", 2: "6", 1: "7", 0: "8"} # assigning rank value to rows
    rank_to_row = {v: k for k, v in row_to_rank.items()} # creates a dictionary whose keys and values are reversed
    col_to_file = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"} # assigning file value to columns
    file_to_col = {v: k for k, v in rank_to_row.items()}

    def __eq__(self, other): # We need this function to actually compare if a move being made is in the valid_moves list
        if isinstance(other, Move):
            return self.move_ID == other.move_ID
        return False

    def get_chess_notation(self):
        """
        :return: the chess notation for the piece. i.e. C3 instead of 5,3.
        """
        return self.get_rank_file(self.start_row, self.start_col) + "=>" + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        """"
        This is a helper function to get the rank and file for the selected chess piece. Chess notation starts with
        the column and ends with the row.
        """
        return self.col_to_file[col] + self.row_to_rank[row]

