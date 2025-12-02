import random
from dice import Dice
from scorecard import Scorecard

class Game:
    current_round = 0 
    dice_values = [0] * 5
    sorted_dice = [0] * 5
    frequency = [0] * 6  
    players = Scorecard(2)  
    die = [Dice() for _ in range(5)]

    def __init__(self, players):
        self.players = Scorecard(players)
        self.die = [Dice() for _ in range(5)]
        self.roll_dice()
        self.set_dice_values()
        self.set_sorted_dice()
        self.set_frequency()
    
    def roll_dice(self):
        for dice in self.die:
            dice.roll()
        self.set_dice_values()
    
    def get_dice_values(self):
        return [dice.face_value for dice in self.die]
    
    def get_sorted_dice(self):
        return sorted(self.get_dice_values())
    
    def get_frequency(self):
        return self.frequency
    
    def set_dice_values(self):
        for i in range(5):
            self.dice_values[i] = self.die[i].face_value

    def set_sorted_dice(self):
        self.sorted_dice = sorted(self.dice_values)
    
    def set_frequency(self):
        self.frequency = [0] * 6
        for value in self.dice_values:
            self.frequency[value - 1] += 1

    def play(self):
        """
        Main game loop: 13 rounds, each player takes a turn per round.
        Each turn consists of 3 dice rolls with the ability to keep dice between rolls.
        """
        for round_num in range(1, 14):  # 13 rounds total
            print(f"\n{'='*60}")
            print(f"ROUND {round_num}")
            print(f"{'='*60}")
            for player_idx in range(self.players.num_players):
                print(f"\n--- Player {player_idx + 1}'s Turn (Round {round_num}) ---")
                kept_indices = set()  # Reset kept dice for new turn
                for roll_num in range(1, 4):
                    print(f"\nRoll {roll_num}/3:")
                    if roll_num == 1:
                        self.roll_dice()
                    self.display_dice(kept_indices)
                    if roll_num < 3:
                        reroll_indices = self.get_reroll_dice_input()
                        # Update kept indices: unkeep rerolled dice
                        for idx in reroll_indices:
                            kept_indices.discard(idx)
                        # Roll the reroll dice
                        for idx in reroll_indices:
                            self.die[idx].roll()
                        self.set_dice_values()
                        self.set_sorted_dice()
                        self.set_frequency()
                print(f"\nFinal dice: {self.get_dice_values()}")
                slot_idx = self.get_scoring_slot_input(player_idx)
                score = self.calculate_score(slot_idx)
                self.players.set_score(player_idx, slot_idx, score)
                print(f"Player {player_idx + 1} scored {score} points in slot {slot_idx + 1}!")
    

    def display_dice(self, kept_indices):
        """Display current dice values with indices aligned below."""
        values = self.get_dice_values()
        values_line = ""
        indices_line = ""
        
        for i, value in enumerate(values):
            if i in kept_indices:
                values_line += f"[{value}] "
                indices_line += f"[{i+1}] "
            else:
                values_line += f" {value}  "
                indices_line += f" {i+1}  "
        
        print("Values: " + values_line)
        print("Dice#:  " + indices_line)
        if kept_indices:
            print(f"(Kept: {sorted([i+1 for i in kept_indices])})")
    
    def get_reroll_dice_input(self):
        """
        Ask player which dice to reroll (1-5 for user, internally 0-4).
        Returns set of indices (0-4) of dice to reroll.
        Pressing Enter with no input keeps all dice (rerolls none).
        """
        while True:
            try:
                user_input = input(
                    "Enter dice numbers to reroll (1-5, space-separated), or press Enter to keep all: "
                ).strip()
                if not user_input:
                    return set()  # Keep all dice
                indices = [int(x) - 1 for x in user_input.split()]
                if all(0 <= idx < 5 for idx in indices):
                    return set(indices)
                else:
                    print("Invalid numbers. Please enter numbers 1-5.")
            except ValueError:
                print("Invalid input. Please enter space-separated numbers (e.g., 1 3 5).")

    def display_scorecard(self, player_idx):
        """Display the current scorecard for a player."""
        player_card = self.players.get_player_card(player_idx)
        categories = [
            "Ones", "Twos", "Threes", "Fours", "Fives", "Sixes",
            "3 of a Kind", "4 of a Kind", "Full House", "Small Straight",
            "Large Straight", "Yahtzee", "Chance"
        ]
        
        print(f"\n--- Player {player_idx + 1} Scorecard ---")
        print(f"{'Slot':<3} {'Category':<18} {'Score':<8} {'Available'}")
        print("-" * 50)
        for i, category in enumerate(categories):
            score = player_card[i]
            available = "✓ OPEN" if score == 0 else "✗ USED"
            score_display = str(score) if score != 0 else "-"
            print(f"{i:<3} {category:<18} {score_display:<8} {available}")
    
    def get_scoring_slot_input(self, player_idx):
        """
        Ask player which scoring category/slot to use (0-12).
        Displays the scorecard first.
        """
        player_card = self.players.get_player_card(player_idx)
        self.display_scorecard(player_idx)
        
        while True:
            try:
                slot = int(input(
                    f"\nChoose an open scoring slot (0-12) for Player {player_idx + 1}: "
                ))
                
                if 0 <= slot < 13:
                    if player_card[slot] != 0:
                        print(f"❌ Slot {slot} already used! Choose an open slot.")
                        self.display_scorecard(player_idx)
                        continue
                    return slot
                else:
                    print("Invalid slot. Please enter 0-12.")
            except ValueError:
                print("Invalid input. Please enter a number between 0 and 12.")
    
    def calculate_score(self, slot_idx):
        """
        Calculate the score for a given category/slot.
        Slots 0-5: Ones through Sixes (sum of dice with that value)
        Slots 6-12: Various Yahtzee categories
        """
        values = self.get_dice_values()
        sorted_values = self.get_sorted_dice()
        freq = self.get_frequency()
        
        # Slots 0-5: Number categories (Ones, Twos, Threes, etc.)
        if slot_idx < 6:
            return sum(v for v in values if v == slot_idx + 1)
        
        # Slot 6: Three of a Kind
        elif slot_idx == 6:
            if any(f >= 3 for f in freq):
                return sum(values)
            return 0
        
        # Slot 7: Four of a Kind
        elif slot_idx == 7:
            if any(f >= 4 for f in freq):
                return sum(values)
            return 0
        
        # Slot 8: Full House
        elif slot_idx == 8:
            if sorted(freq).count(0) == 4 and (3 in freq and 2 in freq):
                return 25
            return 0
        
        # Slot 9: Small Straight (4 consecutive numbers)
        elif slot_idx == 9:
            if self.is_small_straight(sorted_values):
                return 30
            return 0
        
        # Slot 10: Large Straight (5 consecutive numbers)
        elif slot_idx == 10:
            if self.is_large_straight(sorted_values):
                return 40
            return 0
        
        # Slot 11: Yahtzee (all 5 dice the same)
        elif slot_idx == 11:
            if max(freq) == 5:
                return 50
            return 0
        
        # Slot 12: Chance (sum of all dice)
        elif slot_idx == 12:
            return sum(values)
        
        return 0
    
    def is_small_straight(self, sorted_values):
        """Check if dice contain a small straight (4 consecutive)."""
        straights = [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]]
        for straight in straights:
            if all(num in sorted_values for num in straight):
                return True
        return False
    
    def is_large_straight(self, sorted_values):
        """Check if dice contain a large straight (5 consecutive)."""
        return sorted_values == [1, 2, 3, 4, 5] or sorted_values == [2, 3, 4, 5, 6]