class Game:
    """Manages the logic of playing Yahtzee."""
    
    ROUNDS = 13
    ROLLS_PER_TURN = 3
    
    def __init__(self, players):
        """Initialize a new game with the given players.
        
        Args:
            players: List of Player objects
        """
        self.players = players
        self.current_round = 0
        self.current_player_index = 0
        self.current_turn_rolls = 0
    
    def is_game_over(self):
        """Check if the game has completed all rounds."""
        return self.current_round >= self.ROUNDS
    
    def next_turn(self):
        """Move to the next player's turn."""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        if self.current_player_index == 0:
            self.current_round += 1
        self.current_turn_rolls = 0
    
    def roll_dice(self):
        """Execute a roll for the current player.
        
        Returns:
            List of dice values rolled
        """
        if self.current_turn_rolls >= self.ROLLS_PER_TURN:
            raise ValueError("No more rolls available this turn")
        
        self.current_turn_rolls += 1
        return self.players[self.current_player_index].roll()
    
    def get_current_player(self):
        """Get the player whose turn it is."""
        return self.players[self.current_player_index]