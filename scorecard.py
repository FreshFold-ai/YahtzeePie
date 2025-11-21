class Scorecard:
    def __init__(self, num_players):
        """
        Initialize scorecards for all players.
        Each player has 13 slots: 6 for top table, 7 for bottom table.
        Args:
            num_players (int): Number of players in the game
        """
        self.num_players = num_players
        self.cards = [[0] * 13 for _ in range(num_players)]
    
    def get_score(self, player_idx, slot_idx):
        """
        Retrieve a score from a specific player's scorecard.
        
        Args:
            player_idx (int): Player index (0-based)
            slot_idx (int): Slot index (0-12)
        
        Returns:
            int: Score value at the specified slot
        """
        if 0 <= player_idx < self.num_players and 0 <= slot_idx < 13:
            return self.cards[player_idx][slot_idx]
        raise IndexError("Invalid player or slot index")
    
    def set_score(self, player_idx, slot_idx, value):
        """
        Update a score in a specific player's scorecard.
        
        Args:
            player_idx (int): Player index (0-based)
            slot_idx (int): Slot index (0-12)
            value (int): Score value to set
        """
        if 0 <= player_idx < self.num_players and 0 <= slot_idx < 13:
            self.cards[player_idx][slot_idx] = value
        else:
            raise IndexError("Invalid player or slot index")
    
    def get_player_card(self, player_idx):
        """
        Retrieve an entire player's scorecard.
        
        Args:
            player_idx (int): Player index (0-based)
        
        Returns:
            list: List of 13 scores for the player
        """
        if 0 <= player_idx < self.num_players:
            return self.cards[player_idx]
        raise IndexError("Invalid player index")