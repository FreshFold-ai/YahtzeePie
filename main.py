from dice import Dice
from scorecard import Scorecard

class YahtzeeGame:
    def __init__(self):
        pass


if __name__ == "__main__":
    d = Dice()
    print(f"Initial roll: {d.face_value}")

    s = Scorecard(2)
    s.set_score(0, 2, 25)
    s.set_score(1, 5, 30)
    s.set_score(0, 1, 15)
    s.set_score(1, 12, 20)
    print(f"Player 0: {s.get_player_card(0)}")
    print(f"Player 1: {s.get_player_card(1)}")

