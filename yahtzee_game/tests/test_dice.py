import unittest
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dice import Dice


class TestDice(unittest.TestCase):
    """Test suite for the Dice class."""
    
    def test_init_creates_valid_face_value(self):
        """Test that __init__ creates a die with a valid face value (1-6)."""
        die = Dice()
        self.assertIn(die.face_value, range(1, 7))
    
    def test_face_value_getter(self):
        """Test the face_value property getter."""
        die = Dice()
        value = die.face_value
        self.assertIsInstance(value, int)
        self.assertGreaterEqual(value, 1)
        self.assertLessEqual(value, 6)
    
    def test_face_value_setter_valid_values(self):
        """Test setting face_value with valid values (1-6)."""
        die = Dice()
        for value in range(1, 7):
            die.face_value = value
            self.assertEqual(die.face_value, value)
    
    def test_face_value_setter_invalid_low_value(self):
        """Test that setting face_value to 0 raises ValueError."""
        die = Dice()
        with self.assertRaises(ValueError) as context:
            die.face_value = 0
        self.assertIn("Face value must be between 1 and 6", str(context.exception))
    
    def test_face_value_setter_invalid_high_value(self):
        """Test that setting face_value to 7 raises ValueError."""
        die = Dice()
        with self.assertRaises(ValueError) as context:
            die.face_value = 7
        self.assertIn("Face value must be between 1 and 6", str(context.exception))
    
    def test_face_value_setter_negative_value(self):
        """Test that setting face_value to negative value raises ValueError."""
        die = Dice()
        with self.assertRaises(ValueError):
            die.face_value = -1
    
    def test_roll_returns_valid_value(self):
        """Test that roll() returns a valid face value (1-6)."""
        die = Dice()
        for _ in range(100):  # Test multiple rolls
            value = die.roll()
            self.assertIn(value, range(1, 7))
    
    def test_roll_updates_face_value(self):
        """Test that roll() updates the face_value property."""
        die = Dice()
        die.face_value = 3  # Set to a known value
        die.roll()
        # After rolling, face_value should still be valid (may or may not be 3)
        self.assertIn(die.face_value, range(1, 7))
    
    def test_roll_returns_face_value(self):
        """Test that roll() returns the same value as face_value."""
        die = Dice()
        rolled_value = die.roll()
        self.assertEqual(rolled_value, die.face_value)
    
    def test_multiple_dice_independent(self):
        """Test that multiple Dice instances are independent."""
        die1 = Dice()
        die2 = Dice()
        die1.face_value = 1
        die2.face_value = 6
        self.assertEqual(die1.face_value, 1)
        self.assertEqual(die2.face_value, 6)
    
    def test_roll_produces_different_values(self):
        """Test that rolling multiple times produces at least some different values."""
        die = Dice()
        values = set()
        for _ in range(100):
            values.add(die.roll())
        # With 100 rolls, we should see more than one unique value
        self.assertGreater(len(values), 1)


if __name__ == '__main__':
    unittest.main()
