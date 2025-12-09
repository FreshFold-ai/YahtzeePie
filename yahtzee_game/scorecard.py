class Scorecard:
    def __init__(self, num_players):
        
        self.num_players = num_players
        self.cards = [[0] * 13 for _ in range(num_players)]
    
    def get_score(self, player_idx, slot_idx):
        if 0 <= player_idx < self.num_players and 0 <= slot_idx < 13:
            return self.cards[player_idx][slot_idx]
        raise IndexError("Invalid player or slot index")
    
    def set_score(self, player_idx, slot_idx, value):
        if 0 <= player_idx < self.num_players and 0 <= slot_idx < 13:
            self.cards[player_idx][slot_idx] = value
        else:
            raise IndexError("Invalid player or slot index")
    
    def get_player_card(self, player_idx):
        if 0 <= player_idx < self.num_players:
            return self.cards[player_idx]
        raise IndexError("Invalid player index")