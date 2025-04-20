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
            if location['row'] in range(row_size):
                # List to store the coordinates?
                self.coordinate = []
                for x in range(size):
                    if location['col'] + x in range(col_size):
                        self.coordinate.append({'row': location['row'], 'col': location['col'] + x})
                    else:
                        raise IndexError("The column does not exist.")
