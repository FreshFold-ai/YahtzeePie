from dice import Dice
from scorecard import Scorecard
from game import Game

class YahtzeeGame:
    def __init__(self):
        pass


if __name__ == "__main__":
    while True:
        try:
            players = int(input("How many players will be playing? ").strip())
            if players >= 1:
                break
            print("Please enter an integer value of at least 1.")
        except ValueError:
            print("Invalid input — enter a single integer value.")
    g = Game(players)
    print(f"Starting a game of Yahtzee with {players} players!")
    g.play()
    


