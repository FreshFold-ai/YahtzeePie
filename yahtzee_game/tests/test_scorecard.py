import unittest
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scorecard import Scorecard

class TestScorecard(unittest.TestCase):
    
    def test_init_single_player(self):
        """Test initializing a scorecard for a single player."""
        scorecard = Scorecard(1)
        self.assertEqual(scorecard.num_players, 1)
        self.assertEqual(len(scorecard.cards), 1)
        self.assertEqual(len(scorecard.cards[0]), 13)
    
    def test_init_multiple_players(self):
        """Test initializing a scorecard for multiple players."""
        scorecard = Scorecard(4)
        self.assertEqual(scorecard.num_players, 4)
        self.assertEqual(len(scorecard.cards), 4)
        for card in scorecard.cards:
            self.assertEqual(len(card), 13)
    
    def test_init_all_scores_zero(self):
        """Test that all scores are initialized to 0."""
        scorecard = Scorecard(2)
        for player_idx in range(2):
            for slot_idx in range(13):
                self.assertEqual(scorecard.get_score(player_idx, slot_idx), 0)
    
    def test_get_score_valid_indices(self):
        """Test getting scores with valid player and slot indices."""
        scorecard = Scorecard(2)
        score = scorecard.get_score(0, 0)
        self.assertEqual(score, 0)
        
        score = scorecard.get_score(1, 12)
        self.assertEqual(score, 0)
    
    def test_get_score_invalid_player_index_negative(self):
        """Test that get_score raises IndexError for negative player index."""
        scorecard = Scorecard(2)
        with self.assertRaises(IndexError) as context:
            scorecard.get_score(-1, 0)
        self.assertIn("Invalid player or slot index", str(context.exception))
    
    def test_get_score_invalid_player_index_too_high(self):
        """Test that get_score raises IndexError for player index >= num_players."""
        scorecard = Scorecard(2)
        with self.assertRaises(IndexError) as context:
            scorecard.get_score(2, 0)
        self.assertIn("Invalid player or slot index", str(context.exception))
    
    def test_get_score_invalid_slot_index_negative(self):
        """Test that get_score raises IndexError for negative slot index."""
        scorecard = Scorecard(2)
        with self.assertRaises(IndexError) as context:
            scorecard.get_score(0, -1)
        self.assertIn("Invalid player or slot index", str(context.exception))
    
    def test_get_score_invalid_slot_index_too_high(self):
        """Test that get_score raises IndexError for slot index >= 13."""
        scorecard = Scorecard(2)
        with self.assertRaises(IndexError) as context:
            scorecard.get_score(0, 13)
        self.assertIn("Invalid player or slot index", str(context.exception))
    
    def test_set_score_valid_indices(self):
        """Test setting scores with valid player and slot indices."""
        scorecard = Scorecard(2)
        scorecard.set_score(0, 0, 3)
        self.assertEqual(scorecard.get_score(0, 0), 3)
        
        scorecard.set_score(1, 12, 25)
        self.assertEqual(scorecard.get_score(1, 12), 25)
    
    def test_set_score_updates_correct_slot(self):
        """Test that set_score updates only the specified slot."""
        scorecard = Scorecard(1)
        scorecard.set_score(0, 5, 30)
        
        # Check that only slot 5 is updated
        for slot_idx in range(13):
            if slot_idx == 5:
                self.assertEqual(scorecard.get_score(0, slot_idx), 30)
            else:
                self.assertEqual(scorecard.get_score(0, slot_idx), 0)
    
    def test_set_score_invalid_player_index_negative(self):
        """Test that set_score raises IndexError for negative player index."""
        scorecard = Scorecard(2)
        with self.assertRaises(IndexError) as context:
            scorecard.set_score(-1, 0, 10)
        self.assertIn("Invalid player or slot index", str(context.exception))
    
    def test_set_score_invalid_player_index_too_high(self):
        """Test that set_score raises IndexError for player index >= num_players."""
        scorecard = Scorecard(2)
        with self.assertRaises(IndexError) as context:
            scorecard.set_score(2, 0, 10)
        self.assertIn("Invalid player or slot index", str(context.exception))
    
    def test_set_score_invalid_slot_index_negative(self):
        """Test that set_score raises IndexError for negative slot index."""
        scorecard = Scorecard(2)
        with self.assertRaises(IndexError) as context:
            scorecard.set_score(0, -1, 10)
        self.assertIn("Invalid player or slot index", str(context.exception))
    
    def test_set_score_invalid_slot_index_too_high(self):
        """Test that set_score raises IndexError for slot index >= 13."""
        scorecard = Scorecard(2)
        with self.assertRaises(IndexError) as context:
            scorecard.set_score(0, 13, 10)
        self.assertIn("Invalid player or slot index", str(context.exception))
    
    def test_set_score_overwrite_existing(self):
        """Test that set_score can overwrite an existing score."""
        scorecard = Scorecard(1)
        scorecard.set_score(0, 0, 5)
        self.assertEqual(scorecard.get_score(0, 0), 5)
        
        scorecard.set_score(0, 0, 10)
        self.assertEqual(scorecard.get_score(0, 0), 10)
    
    def test_get_player_card_valid_index(self):
        """Test getting a player's card with valid index."""
        scorecard = Scorecard(2)
        scorecard.set_score(0, 0, 3)
        scorecard.set_score(0, 5, 15)
        
        player_card = scorecard.get_player_card(0)
        self.assertEqual(len(player_card), 13)
        self.assertEqual(player_card[0], 3)
        self.assertEqual(player_card[5], 15)
    
    def test_get_player_card_invalid_index_negative(self):
        """Test that get_player_card raises IndexError for negative player index."""
        scorecard = Scorecard(2)
        with self.assertRaises(IndexError) as context:
            scorecard.get_player_card(-1)
        self.assertIn("Invalid player index", str(context.exception))
    
    def test_get_player_card_invalid_index_too_high(self):
        """Test that get_player_card raises IndexError for player index >= num_players."""
        scorecard = Scorecard(2)
        with self.assertRaises(IndexError) as context:
            scorecard.get_player_card(2)
        self.assertIn("Invalid player index", str(context.exception))
    
    def test_get_player_card_returns_list_reference(self):
        """Test that get_player_card returns a reference to the actual card."""
        scorecard = Scorecard(1)
        player_card = scorecard.get_player_card(0)
        player_card[0] = 100
        
        # Verify the change is reflected in the scorecard
        self.assertEqual(scorecard.get_score(0, 0), 100)
    
    def test_multiple_players_independent(self):
        """Test that scores for different players are independent."""
        scorecard = Scorecard(3)
        scorecard.set_score(0, 0, 10)
        scorecard.set_score(1, 0, 20)
        scorecard.set_score(2, 0, 30)
        
        self.assertEqual(scorecard.get_score(0, 0), 10)
        self.assertEqual(scorecard.get_score(1, 0), 20)
        self.assertEqual(scorecard.get_score(2, 0), 30)
    
    def test_all_slots_independent(self):
        """Test that all 13 slots are independent for each player."""
        scorecard = Scorecard(1)
        for slot_idx in range(13):
            scorecard.set_score(0, slot_idx, slot_idx * 5)
        
        for slot_idx in range(13):
            self.assertEqual(scorecard.get_score(0, slot_idx), slot_idx * 5)

if __name__ == '__main__':
    unittest.main()
