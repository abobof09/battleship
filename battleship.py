from random import randint # Will allow randomized ship placements
import os

class Game:
    def __init__(self, size, direction, location):
        """
        Initialize the Game class with logic attributes.
        Args:
            size: the size of the ship(s)
            direction: the direction the ship(s) are facing
            location: the starting coordinate of the ship(s)
        """
        self.size = size
        if direction.lower() == "horizontal" or direction.lower() == "vertical":
            self.direction = direction
        else:
            raise ValueError("Value should be either horizontal or vertical.")
        
        # Properly orient the ships based on the parameters
        if direction.lower() == "horizontal":
            if location['row'] in range(num_cols):
                # List to store the coordinates?
                self.coords = []
                for x in range(size):
                    if location['col'] + x in range(num_rows):
                        self.coords.append({'row': location['row'], 'col': location['col'] + x})
                    else:
                        raise IndexError("The column does not exist.")
                else:
                    raise IndexError("The row does not exist.")
        elif direction.lower() == "vertical":
            if location['col'] in num_rows:
                self.coords = []
                for x in range(size):
                    if location['row'] + x in range(num_cols):
                        self.coords.append({'row': location['row'] + x, 'col': location['col']})
                    else:
                        raise IndexError("Column does not exist.")
                else:
                    raise IndexError("Row does not exist.")
        if self.filled():
            # there will eventually be a print_board method
            print_board(board)
            print(" ".join(str(coords) for coords in self.coordinates))
            raise IndexError("A ship already occupies that space.")
        else:
            self.fill_board()

    def filled(self):
        """
        A method to check if the board has been properly filled.
        """
        for coords in self.coordinates:
            if board[coords['row']][coords['col']] == 1:
                return True
        return False
  
    def fill_board(self):
        """
        A method to generate a fresh board.
        """
        for coords in self.coordinates:
            board[coords['row']][coords['col']] = 1
        
    def does_contain(self, location):
        """
        A method to check coordinates on the board.
        Args:
            location: the specified location
        Returns:
            true or false
        """
        for coords in self.coordinates:
            if coords == location:
                return True
        return False
  
    def destroyed(self):
        for coords in self.coordinates:
            if board_display[coords['row']][coords['col']] == 'O':
                return False
            elif board_display[coords['row']][coords['col']] == '*':
                raise RuntimeError("Board display inaccurate")
        return True


# Game Settings
num_cols = 9
num_rows = 9
num_ships = 4
max_ship_size = 5
min_ship_size = 2
num_turns = 40

#Create lists
ship_list = []

# board will be stored as a list for easy adjustments to the indices
board = [[0] * num_rows for x in range(num_cols)]

board_display = [["O"] * num_rows for x in range(num_cols)]


def print_board(board):
    """
    Prints the game board to the terminal.
    Args:
        board: the game board to be printed
    Returns:
        the board printed to the terminal.
    """
    print("\n  " + " ".join(str(x) for x in range(1, num_rows + 1)))
    for r in range(num_cols):
        print(str(r + 1) + " " + " ".join(str(c) for c in board[r]))
    print()