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
            print_board(board)
            print(" ".join(str(coords) for coords in self.coordinates))
            raise IndexError("A ship already occupies that space.")
        else:
            self.fillBoard()

    def filled(self):
        for coords in self.coordinates:
            if board[coords['row']][coords['col']] == 1:
                return True
        return False
  
    def fillBoard(self):
        for coords in self.coordinates:
            board[coords['row']][coords['col']] = 1


# to avoid errors (size of the board):
num_cols = 10
num_rows = 10
board = [[0] * num_rows for x in range(num_cols)]