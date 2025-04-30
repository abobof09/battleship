from random import randint # Will allow randomized ship placements
import os
import json

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
                raise RuntimeError("Board display inaccurate.")
        return True

class Scoreboard:
    def __init__(self, filename='scoreboard.json'):
        self.filename = filename
        self.scores = self.load_scores()
    
    def load_scores(self):
        """
        A method that loads the file into a json.
        Returns:

        """
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return []
    
    def add_score(self, initials, score):
        self.scores.append({'initials': initials.upper(), 'score': score})
        for i in range(len(self.scores)):
            for j in range(0, len(self.scores) - i - 1):
                if self.scores[j]['score'] > self.scores[j + 1]['score']:
                    self.scores[j], self.scores[j + 1] = self.scores[j + 1], self.scores[j]
        self.save_scores()

    def save_scores(self):
        with open(self.filename, 'w') as file:
            json.dump(self.scores, file, indent=2)

    def display(self):
        print("==== Scoreboard =====")
        for i in self.scores[:10]:
            print(f"{i['initials']} - {i['score']} turns")

# Game Settings
scoreboard = Scoreboard()

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

def search_coordinates(size, direction):
    """
    A function that looks for valid spots for a ship to be placed.
    Args:
        size: the size of the ship (seen in the Game class)
        direction: the direction the ship is facing (seen in the Game class)
    Returns:
        None: if there is no valid location
        locations: a list containing the coordinates of the viable locations
    """
    locations = []

    if direction != 'horizontal' and direction != 'vertical':
        raise ValueError("Orientation must have a value of 'horizontal' or 'vertical'.")

    if direction == 'horizontal':
        if size <= num_rows:
            for r in range(num_cols):
                for c in range(num_rows - size + 1):
                    if 1 not in board[r][c:c+size]:
                        locations.append({'row': r, 'col': c})
    elif direction == 'vertical':
        if size <= num_cols:
            for c in range(num_rows):
                for r in range(num_cols - size + 1):
                    if 1 not in [board[i][c] for i in range(r, r+size)]:
                        locations.append({'row': r, 'col': c})
    if not locations:
        return 'None'
    else:
        return locations

def random_location():
    size = randint(min_ship_size, max_ship_size)
    orientation = 'horizontal' if randint(0, 1) == 0 else 'vertical'
    locations = s(size, orientation)
    if locations == 'None':
        return 'None'
    else:
        return {'location': locations[randint(0, len(locations) - 1)], 'size': size,\
                'orientation': orientation}
    
def get_row():
    while True:
        try:
            guess = int(input("Row: "))
            if guess in range(1, num_cols + 1):
                return guess - 1
            else:
                print("Row does not exist.")
        except ValueError:
            print("Please enter a number.")

def get_col():
    while True:
        try:
            guess = int(input("Column: "))
            if guess in range(1, num_rows + 1):
                return guess - 1
            else:
                print("Column does not exist")
        except ValueError:
            print("Please enter a number.")

# Place the ships on the board
count = 0
while count < num_ships:
    ship_info = random_location()
    if ship_info == 'None':
        continue
    else:
        ship_list.append(Game(ship_info['size'], ship_info['orientation'], ship_info['location']))
        count += 1
del count

# Play the Game
os.system('clear')
print_board(board_display)

for i in range(num_turns):
    print("Turn:", i + 1, "of", num_turns)
    print("Ships left:", len(ship_list))
    print()

    coordinates = {}
    while True:
        coordinates['row'] = get_row()
        coordinates['col'] = get_col() 
        if board_display[coordinates['row']][coordinates['col']] == 'X':
            print("You already missed at that space!")
        elif board_display[coordinates['row']][coordinates['col']] == '*':
            print("You already hit that space!")
        else:
            break
    os.system('clear')
    ship_hit = False
    for s in ship_list:
        if s.contains(coordinates):
            print("Hit!")
            ship_hit = True
            board_display[coordinates['row']][coordinates['col']] = 'X'
            if s.destroyed():
                print("Ship was destroyed!")
                ship_list.remove(s)
            break
        if not ship_hit:
            board_display[coordinates['row']][coordinates['col']] = '*'
            print("You missed!")
        print_board(board_display)
        if not ship_list:
            break

# End the Game
if ship_list:
    print("You lose...")
else:
    print("You sunk all the ships! You win!")
    initials = input("Enter your initials (3 characters): ").strip().upper()[:3]
    scoreboard.add_score(initials, i + 1)
    scoreboard.display()