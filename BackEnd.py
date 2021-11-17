from typing import Dict


class Chess():
    """
    Defines the current game state of
    """

    def __init__(self):
        # Create an 8x8 2D list with each element of the list representing a piece. The first character is
        # the team of the piece. The second character is the piece.
        self.board = [
            ["BR", "BKn", "BB", "BQ", "BK", "BB", "BKn", "BR"],
            ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
            ["WR", "WKn", "WB", "WQ", "WK", "WB", "WKn", "WR"]]
        self.white_to_move = True
        self.move_log = []  # We want to store the moves so that we can undo moves later on

    def make_move(self, move):
        """
        This function moves the chess piece by leaving behind an empty piece and updating the board with the
        new location. We also log the move in the move_log list created before. Finally, we switch the turn of the
        player.
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

class Move():
    def __init__(self, start_tile, end_tile, board):
        self.start_row = start_tile[0]
        self.start_col = start_tile[1]
        self.end_row = end_tile[0]
        self.end_col = end_tile[1]
        self.active_piece = board[self.start_row][self.start_col]  # represents the start location of the selected piece
        self.moved_location = board[self.end_row][self.end_col]  # represents the end location of the selected piece

    row_to_rank = {7: "1", 6: "2", 5: "3", 4: "4", 3: "5", 2: "6", 1: "7", 0: "8"} # assigning rank value to rows
    rank_to_row = {v: k for k, v in row_to_rank.items()} # creates a dictionary whose keys and values are reversed
    col_to_file = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"} # assigning file value to columns
    file_to_col = {v: k for k, v in rank_to_row.items()}

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

