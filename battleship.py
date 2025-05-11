from random import randint # Will allow randomized ship placements
import os
import json

class ShipLogic:
    def __init__(self, game, size, direction, location):
        """
        Initialize the Game class with logic attributes.
        Args:
            size: the size of the ship(s)
            direction: the direction the ship(s) are facing
            location: the starting coordinate of the ship(s)
        """
        self.game = game
        self.size = size
        if direction.lower() == "horizontal" or direction.lower() == "vertical":
            self.direction = direction
        else:
            raise ValueError("Value should be either horizontal or vertical.")
        
        # Properly orient the ships based on the parameters
        if direction.lower() == "horizontal":
            if location['row'] in range(self.game.num_cols):
                self.coords = []
                for x in range(size):
                    if location['col'] + x in range(self.game.num_rows):
                        self.coords.append({'row': location['row'], 'col': location['col'] + x})
                    else:
                        raise IndexError("The column does not exist.")
            else:
                raise IndexError("The row does not exist.")
        elif direction.lower() == "vertical":
            if location['col'] in range(self.game.num_rows):
                self.coords = []
                for x in range(size):
                    if location['row'] + x in range(self.game.num_cols):
                        self.coords.append({'row': location['row'] + x, 'col': location['col']})
                    else:
                        raise IndexError("Column does not exist.")
            else:
                raise IndexError("Row does not exist.")
        if self.filled():
            self.game.print_board(self.game.board)
            print(" ".join(str(coords) for coords in self.coords))
            raise IndexError("A ship already occupies that space.")
        else:
            self.fill_board()

    def filled(self):
        """
        A method to check if the board has been properly filled.
        """
        for coords in self.coords:
            if self.game.board[coords['row']][coords['col']] != 0:
                return True
        return False
  
    def fill_board(self):
        """
        A method to generate a fresh board.
        """
        for coords in self.coords:
            self.game.board[coords['row']][coords['col']] = 1
        
    def does_contain(self, location):
        """
        A method to check coords on the board.
        Args:
            location: the specified location
        Returns:
            true or false
        """
        for coords in self.coords:
            if coords == location:
                return True
        return False
  
    def destroyed(self):
        for coords in self.coords:
            if self.game.board_display[coords['row']][coords['col']] == 'O':
                return False
            elif self.game.board_display[coords['row']][coords['col']] == '*':
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

class Battleship:
    def __init__(self, num_cols=9, num_rows=9, num_ships=4, max_ship_size=5, min_ship_size=2, num_turns=40):
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.num_ships = num_ships
        self.max_ship_size = max_ship_size
        self.min_ship_size = min_ship_size
        self.num_turns = num_turns
        
        self.board = [[0] * num_rows for _ in range(num_cols)]
        self.board_display = [["O"] * num_rows for _ in range(num_cols)]
        self.ship_list = []
        self.scoreboard = Scoreboard()

    def print_board(self, board):
        """
        Prints the game board to the terminal.
        Args:
            board: the game board to be printed
        Returns:
            the board printed to the terminal.
        """
        print("\n  " + " ".join(str(x) for x in range(1, self.num_rows + 1)))
        for r in range(self.num_cols):
            print(str(r + 1) + " " + " ".join(str(c) for c in board[r]))
        print()
    
    def search_coords(self, size, direction):
        """
        A function that looks for valid spots for a ship to be placed.
        Args:
            size: the size of the ship (seen in the Game class)
            direction: the direction the ship is facing (seen in the Game class)
        Returns:
            None: if there is no valid location
            locations: a list containing the coords of the viable locations
        """
        locations = []

        if direction != 'horizontal' and direction != 'vertical':
            raise ValueError("Orientation must have a value of 'horizontal' or 'vertical'.")

        if direction == 'horizontal':
            if size <= self.num_rows:
                for r in range(self.num_cols):
                    for c in range(self.num_rows - size + 1):
                        if 1 not in self.board[r][c:c+size]:
                            locations.append({'row': r, 'col': c})
        elif direction == 'vertical':
            if size <= self.num_cols:
                for c in range(self.num_rows):
                    for r in range(self.num_cols - size + 1):
                        if 1 not in [self.board[i][c] for i in range(r, r+size)]:
                            locations.append({'row': r, 'col': c})

        return locations if locations else None
    
    def random_location(self):
        """
        Gets a random valid location on the board.
        """
        size = randint(self.min_ship_size, self.max_ship_size)
        orientation = 'horizontal' if randint(0, 1) == 0 else 'vertical'
        locations = self.search_coords(size, orientation)
        if locations == None:
            return 'None'
        else:
            return {'location': locations[randint(0, len(locations) - 1)], 'size': size,
                    'orientation': orientation}
        
    def place_ships(self):
        """
        Places ships on the board.
        """
        count = 0
        while count < self.num_ships:
            ship_info = self.random_location()
            if ship_info:
                self.ship_list.append(Game(self, ship_info['size'], ship_info['orientation'], ship_info['location']))
                count += 1

    def get_row(self):
        """
        A method to get a specific row on the board.
        """
        while True:
            try:
                guess = int(input("Row: "))
                if guess in range(1, self.num_cols + 1):
                    return guess - 1
                else:
                    print("Row does not exist.")
            except ValueError:
                print("Please enter a number.")

    def get_col(self):
        """
        A method to get a specific column on the board.
        """
        while True:
            try:
                guess = int(input("Column: "))
                if guess in range(1, self.num_rows + 1):
                    return guess - 1
                else:
                    print("Column does not exist")
            except ValueError:
                print("Please enter a number.")

    def play_turn(self, turn):
        """
        Handles a single turn.
        Args: 
            turn: the current turn
        """
        print(f"Turn: {turn + 1} of {self.num_turns}")
        print(f"Ships left: {len(self.ship_list)}\n")
        
        coords = {}
        while True:
            coords['row'] = self.get_row()
            coords['col'] = self.get_col()
            if self.board_display[coords['row']][coords['col']] in ('X', '*'):
                print("You've already tried that space!")
            else:
                break

        os.system('clear')
        ship_hit = False
        for ship in self.ship_list:
            if ship.does_contain(coords):
                print("Hit!")
                ship_hit = True
                self.board_display[coords['row']][coords['col']] = 'X'
                if ship.destroyed():
                    print("Ship was destroyed!")
                    self.ship_list.remove(ship)
                break
        
        if not ship_hit:
            self.board_display[coords['row']][coords['col']] = '*'
            print("You missed!")
        
        self.print_board(self.board_display)

    def run_game(self):
        """
        Runs the Battleship game loop.
        """
        self.place_ships()
        os.system('clear')
        self.print_board(self.board_display)

        for turn in range(self.num_turns):
            if not self.ship_list:
                break
            self.play_turn(turn)

        self.end_game(turn)

    def end_game(self, turns):
        """
        Handles end-of-game logic.
        Args:
            turn: the current turn.
        """
        if self.ship_list:
            print("You lose...")
        else:
            print("You sunk all the ships! You win!")
            initials = input("Enter your initials (3 characters): ").strip().upper()[:3]
            self.scoreboard.add_score(initials, turns + 1)
            self.scoreboard.display()

if __name__ == "__main__":
    game = Battleship()
    game.run_game()