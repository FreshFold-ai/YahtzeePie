import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game import Game
from dice import Dice


class TestGame(unittest.TestCase):
    """Test suite for the Game class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.game = Game(2)
    
    def test_init_creates_scorecard(self):
        """Test that __init__ creates a Scorecard with correct number of players."""
        game = Game(3)
        self.assertEqual(game.players.num_players, 3)
    
    def test_init_creates_five_dice(self):
        """Test that __init__ creates exactly 5 Dice objects."""
        game = Game(2)
        self.assertEqual(len(game.die), 5)
        for die in game.die:
            self.assertIsInstance(die, Dice)
    
    def test_init_rolls_dice_initially(self):
        """Test that __init__ rolls all dice and sets initial values."""
        game = Game(2)
        for value in game.dice_values:
            self.assertIn(value, range(1, 7))
    
    def test_roll_dice_updates_all_dice(self):
        """Test that roll_dice() rolls all 5 dice."""
        self.game.roll_dice()
        for die in self.game.die:
            self.assertIn(die.face_value, range(1, 7))
    
    def test_roll_dice_updates_dice_values(self):
        """Test that roll_dice() updates the dice_values array."""
        self.game.roll_dice()
        for i in range(5):
            self.assertEqual(self.game.dice_values[i], self.game.die[i].face_value)
    
    def test_get_dice_values_returns_list_of_five(self):
        """Test that get_dice_values() returns a list of 5 values."""
        values = self.game.get_dice_values()
        self.assertEqual(len(values), 5)
    
    def test_get_dice_values_returns_valid_values(self):
        """Test that get_dice_values() returns valid dice values (1-6)."""
        values = self.game.get_dice_values()
        for value in values:
            self.assertIn(value, range(1, 7))
    
    def test_get_dice_values_matches_die_face_values(self):
        """Test that get_dice_values() matches the actual die face values."""
        values = self.game.get_dice_values()
        for i, value in enumerate(values):
            self.assertEqual(value, self.game.die[i].face_value)
    
    def test_get_sorted_dice_returns_sorted_list(self):
        """Test that get_sorted_dice() returns a sorted list."""
        # Set known values
        for i, die in enumerate(self.game.die):
            die.face_value = [5, 2, 6, 1, 3][i]
        self.game.set_dice_values()
        
        sorted_dice = self.game.get_sorted_dice()
        self.assertEqual(sorted_dice, [1, 2, 3, 5, 6])
    
    def test_get_frequency_returns_list_of_six(self):
        """Test that get_frequency() returns a list of 6 frequency counts."""
        freq = self.game.get_frequency()
        self.assertEqual(len(freq), 6)
    
    def test_set_dice_values_updates_array(self):
        """Test that set_dice_values() correctly updates dice_values array."""
        for i, die in enumerate(self.game.die):
            die.face_value = i + 1
        
        self.game.set_dice_values()
        self.assertEqual(self.game.dice_values, [1, 2, 3, 4, 5])
    
    def test_set_sorted_dice_sorts_correctly(self):
        """Test that set_sorted_dice() correctly sorts the dice values."""
        self.game.dice_values = [5, 2, 6, 1, 3]
        self.game.set_sorted_dice()
        self.assertEqual(self.game.sorted_dice, [1, 2, 3, 5, 6])
    
    def test_set_frequency_counts_correctly(self):
        """Test that set_frequency() correctly counts dice frequencies."""
        # Set dice to [1, 1, 3, 3, 3]
        for i, die in enumerate(self.game.die):
            die.face_value = [1, 1, 3, 3, 3][i]
        self.game.set_dice_values()
        self.game.set_frequency()
        
        # Expected frequency: [2, 0, 3, 0, 0, 0]
        self.assertEqual(self.game.frequency[0], 2)  # Two 1s
        self.assertEqual(self.game.frequency[1], 0)  # No 2s
        self.assertEqual(self.game.frequency[2], 3)  # Three 3s
        self.assertEqual(self.game.frequency[3], 0)  # No 4s
        self.assertEqual(self.game.frequency[4], 0)  # No 5s
        self.assertEqual(self.game.frequency[5], 0)  # No 6s
    
    def test_set_frequency_all_different(self):
        """Test frequency counting when all dice show different values."""
        for i, die in enumerate(self.game.die):
            die.face_value = i + 1
        self.game.set_dice_values()
        self.game.set_frequency()
        
        # Expected: [1, 1, 1, 1, 1, 0]
        for i in range(5):
            self.assertEqual(self.game.frequency[i], 1)
        self.assertEqual(self.game.frequency[5], 0)
    
    def test_set_frequency_all_same(self):
        """Test frequency counting when all dice show the same value."""
        for die in self.game.die:
            die.face_value = 4
        self.game.set_dice_values()
        self.game.set_frequency()
        
        # Expected: [0, 0, 0, 5, 0, 0]
        for i in range(6):
            if i == 3:  # Index 3 represents value 4
                self.assertEqual(self.game.frequency[i], 5)
            else:
                self.assertEqual(self.game.frequency[i], 0)
    
    def test_calculate_score_ones(self):
        """Test calculating score for ones (slot 0)."""
        for i, die in enumerate(self.game.die):
            die.face_value = [1, 1, 3, 4, 1][i]
        self.game.set_dice_values()
        
        score = self.game.calculate_score(0)
        self.assertEqual(score, 3)  # Three 1s = 3
    
    def test_calculate_score_twos(self):
        """Test calculating score for twos (slot 1)."""
        for i, die in enumerate(self.game.die):
            die.face_value = [2, 2, 2, 4, 5][i]
        self.game.set_dice_values()
        
        score = self.game.calculate_score(1)
        self.assertEqual(score, 6)  # Three 2s = 6
    
    def test_calculate_score_threes(self):
        """Test calculating score for threes (slot 2)."""
        for i, die in enumerate(self.game.die):
            die.face_value = [3, 1, 3, 4, 5][i]
        self.game.set_dice_values()
        
        score = self.game.calculate_score(2)
        self.assertEqual(score, 6)  # Two 3s = 6
    
    def test_calculate_score_fours(self):
        """Test calculating score for fours (slot 3)."""
        for i, die in enumerate(self.game.die):
            die.face_value = [4, 4, 4, 4, 5][i]
        self.game.set_dice_values()
        
        score = self.game.calculate_score(3)
        self.assertEqual(score, 16)  # Four 4s = 16
    
    def test_calculate_score_fives(self):
        """Test calculating score for fives (slot 4)."""
        for i, die in enumerate(self.game.die):
            die.face_value = [5, 1, 2, 3, 5][i]
        self.game.set_dice_values()
        
        score = self.game.calculate_score(4)
        self.assertEqual(score, 10)  # Two 5s = 10
    
    def test_calculate_score_sixes(self):
        """Test calculating score for sixes (slot 5)."""
        for i, die in enumerate(self.game.die):
            die.face_value = [6, 6, 6, 3, 4][i]
        self.game.set_dice_values()
        
        score = self.game.calculate_score(5)
        self.assertEqual(score, 18)  # Three 6s = 18
    
    def test_calculate_score_three_of_kind_valid(self):
        """Test calculating score for three of a kind (valid)."""
        for i, die in enumerate(self.game.die):
            die.face_value = [3, 3, 3, 4, 5][i]
        self.game.set_dice_values()
        self.game.set_frequency()
        
        score = self.game.calculate_score(6)
        self.assertEqual(score, 18)  # Sum of all dice
    
    def test_calculate_score_three_of_kind_invalid(self):
        """Test calculating score for three of a kind (invalid)."""
        for i, die in enumerate(self.game.die):
            die.face_value = [1, 2, 3, 4, 5][i]
        self.game.set_dice_values()
        self.game.set_frequency()
        
        score = self.game.calculate_score(6)
        self.assertEqual(score, 0)
    
    def test_calculate_score_four_of_kind_valid(self):
        """Test calculating score for four of a kind (valid)."""
        for i, die in enumerate(self.game.die):
            die.face_value = [5, 5, 5, 5, 2][i]
        self.game.set_dice_values()
        self.game.set_frequency()
        
        score = self.game.calculate_score(7)
        self.assertEqual(score, 22)  # Sum of all dice
    
    def test_calculate_score_four_of_kind_invalid(self):
        """Test calculating score for four of a kind (invalid)."""
        for i, die in enumerate(self.game.die):
            die.face_value = [5, 5, 5, 2, 3][i]
        self.game.set_dice_values()
        self.game.set_frequency()
        
        score = self.game.calculate_score(7)
        self.assertEqual(score, 0)
    
    def test_calculate_score_full_house_valid(self):
        """Test calculating score for full house (valid)."""
        for i, die in enumerate(self.game.die):
            die.face_value = [2, 2, 2, 5, 5][i]
        self.game.set_dice_values()
        self.game.set_frequency()
        
        score = self.game.calculate_score(8)
        self.assertEqual(score, 25)
    
    def test_calculate_score_full_house_invalid(self):
        """Test calculating score for full house (invalid)."""
        for i, die in enumerate(self.game.die):
            die.face_value = [2, 2, 3, 4, 5][i]
        self.game.set_dice_values()
        self.game.set_frequency()
        
        score = self.game.calculate_score(8)
        self.assertEqual(score, 0)
    
    def test_calculate_score_small_straight_valid_1234(self):
        """Test calculating score for small straight (1-2-3-4)."""
        for i, die in enumerate(self.game.die):
            die.face_value = [1, 2, 3, 4, 6][i]
        self.game.set_dice_values()
        self.game.set_sorted_dice()
        
        score = self.game.calculate_score(9)
        self.assertEqual(score, 30)
    
    def test_calculate_score_small_straight_valid_2345(self):
        """Test calculating score for small straight (2-3-4-5)."""
        for i, die in enumerate(self.game.die):
            die.face_value = [2, 3, 4, 5, 6][i]
        self.game.set_dice_values()
        self.game.set_sorted_dice()
        
        score = self.game.calculate_score(9)
        self.assertEqual(score, 30)
    
    def test_calculate_score_small_straight_valid_3456(self):
        """Test calculating score for small straight (3-4-5-6)."""
        for i, die in enumerate(self.game.die):
            die.face_value = [3, 4, 5, 6, 1][i]
        self.game.set_dice_values()
        self.game.set_sorted_dice()
        
        score = self.game.calculate_score(9)
        self.assertEqual(score, 30)
    
    def test_calculate_score_small_straight_invalid(self):
        """Test calculating score for small straight (invalid)."""
        for i, die in enumerate(self.game.die):
            die.face_value = [1, 2, 4, 5, 6][i]
        self.game.set_dice_values()
        self.game.set_sorted_dice()
        
        score = self.game.calculate_score(9)
        self.assertEqual(score, 0)
    
    def test_calculate_score_large_straight_valid_12345(self):
        """Test calculating score for large straight (1-2-3-4-5)."""
        for i, die in enumerate(self.game.die):
            die.face_value = [1, 2, 3, 4, 5][i]
        self.game.set_dice_values()
        self.game.set_sorted_dice()
        
        score = self.game.calculate_score(10)
        self.assertEqual(score, 40)
    
    def test_calculate_score_large_straight_valid_23456(self):
        """Test calculating score for large straight (2-3-4-5-6)."""
        for i, die in enumerate(self.game.die):
            die.face_value = [2, 3, 4, 5, 6][i]
        self.game.set_dice_values()
        self.game.set_sorted_dice()
        
        score = self.game.calculate_score(10)
        self.assertEqual(score, 40)
    
    def test_calculate_score_large_straight_invalid(self):
        """Test calculating score for large straight (invalid)."""
        for i, die in enumerate(self.game.die):
            die.face_value = [1, 2, 3, 4, 6][i]
        self.game.set_dice_values()
        self.game.set_sorted_dice()
        
        score = self.game.calculate_score(10)
        self.assertEqual(score, 0)
    
    def test_calculate_score_yahtzee_valid(self):
        """Test calculating score for Yahtzee (all 5 dice same)."""
        for die in self.game.die:
            die.face_value = 4
        self.game.set_dice_values()
        self.game.set_frequency()
        
        score = self.game.calculate_score(11)
        self.assertEqual(score, 50)
    
    def test_calculate_score_yahtzee_invalid(self):
        """Test calculating score for Yahtzee (invalid)."""
        for i, die in enumerate(self.game.die):
            die.face_value = [4, 4, 4, 4, 5][i]
        self.game.set_dice_values()
        self.game.set_frequency()
        
        score = self.game.calculate_score(11)
        self.assertEqual(score, 0)
    
    def test_calculate_score_chance(self):
        """Test calculating score for chance (sum of all dice)."""
        for i, die in enumerate(self.game.die):
            die.face_value = [1, 2, 3, 4, 5][i]
        self.game.set_dice_values()
        
        score = self.game.calculate_score(12)
        self.assertEqual(score, 15)
    
    def test_is_small_straight_with_1234(self):
        """Test is_small_straight() with 1-2-3-4."""
        result = self.game.is_small_straight([1, 2, 3, 4, 6])
        self.assertTrue(result)
    
    def test_is_small_straight_with_2345(self):
        """Test is_small_straight() with 2-3-4-5."""
        result = self.game.is_small_straight([2, 3, 4, 5, 6])
        self.assertTrue(result)
    
    def test_is_small_straight_with_3456(self):
        """Test is_small_straight() with 3-4-5-6."""
        result = self.game.is_small_straight([1, 3, 4, 5, 6])
        self.assertTrue(result)
    
    def test_is_small_straight_with_duplicates(self):
        """Test is_small_straight() with duplicate values that still form a straight."""
        result = self.game.is_small_straight([1, 2, 2, 3, 4])
        self.assertTrue(result)
    
    def test_is_small_straight_invalid(self):
        """Test is_small_straight() with invalid pattern."""
        result = self.game.is_small_straight([1, 2, 4, 5, 6])
        self.assertFalse(result)
    
    def test_is_large_straight_with_12345(self):
        """Test is_large_straight() with 1-2-3-4-5."""
        result = self.game.is_large_straight([1, 2, 3, 4, 5])
        self.assertTrue(result)
    
    def test_is_large_straight_with_23456(self):
        """Test is_large_straight() with 2-3-4-5-6."""
        result = self.game.is_large_straight([2, 3, 4, 5, 6])
        self.assertTrue(result)
    
    def test_is_large_straight_invalid(self):
        """Test is_large_straight() with invalid pattern."""
        result = self.game.is_large_straight([1, 2, 3, 4, 6])
        self.assertFalse(result)
    
    def test_is_large_straight_with_duplicates(self):
        """Test is_large_straight() with duplicates (should fail)."""
        result = self.game.is_large_straight([1, 2, 2, 3, 4])
        self.assertFalse(result)
    
    @patch('builtins.input', return_value='1 3 5')
    def test_get_reroll_dice_input_valid(self, mock_input):
        """Test get_reroll_dice_input() with valid input."""
        result = self.game.get_reroll_dice_input()
        self.assertEqual(result, {0, 2, 4})
    
    @patch('builtins.input', return_value='')
    def test_get_reroll_dice_input_empty(self, mock_input):
        """Test get_reroll_dice_input() with empty input (keep all)."""
        result = self.game.get_reroll_dice_input()
        self.assertEqual(result, set())
    
    @patch('builtins.input', side_effect=['invalid', '1 2'])
    @patch('builtins.print')
    def test_get_reroll_dice_input_invalid_then_valid(self, mock_print, mock_input):
        """Test get_reroll_dice_input() with invalid input followed by valid input."""
        result = self.game.get_reroll_dice_input()
        self.assertEqual(result, {0, 1})
    
    @patch('builtins.input', side_effect=['6', '1'])
    @patch('builtins.print')
    def test_get_reroll_dice_input_out_of_range(self, mock_print, mock_input):
        """Test get_reroll_dice_input() with out-of-range value."""
        result = self.game.get_reroll_dice_input()
        self.assertEqual(result, {0})


if __name__ == '__main__':
    unittest.main()
