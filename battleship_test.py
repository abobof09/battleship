import unittest
from battleship import Game, Scoreboard

class TestMethods(unittest.TestCase):
    def setUp(self):
        """
        Sets a fresh board up for each individual test.
        """
        self.num_rows = 9
        self.num_cols = 9
        self.board = [[0 for _ in range(self.num_rows)] for _ in range(self.num_cols)]
        self.board_display = [["O" for _ in range(self.num_rows)] for _ in range(self.num_cols)]

    def test_horizontal_ship_creation(self):
        ship = Game(3, 'horizontal', {'row': 2, 'col': 1})
        expected_coords = [
            {'row': 2, 'col': 1},
            {'row': 2, 'col': 2},
            {'row': 2, 'col': 3}
        ]
        self.assertEqual(ship.coords, expected_coords)

    def test_vertical_ship_creation(self):
        ship = Game(2, 'vertical', {'row': 1, 'col': 4})
        expected_coords = [
            {'row': 1, 'col': 4},
            {'row': 2, 'col': 4}
        ]
        self.assertEqual(ship.coords, expected_coords)

    def test_filled_returns_true(self):
        ship = Game(2, 'horizontal', {'row': 4, 'col': 5})
        self.assertTrue(ship.filled())
    
    def test_invalid_ship_creation(self):
        with self.assertRaises(IndexError):
            Game(10, 'horizontal', {'row': 1, 'col': 8})
    
    def test_destroyed_returns_false(self):
        ship = Game(2, 'vertical', {'row': 2, 'col': 2})
        self.assertFalse(ship.destroyed())

if __name__ == "__main__":
    unittest.main()