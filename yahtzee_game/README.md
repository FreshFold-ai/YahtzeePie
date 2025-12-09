# YahtzeePie
Yahtzee implementation in OOP with Python

## Overview
A fully object-oriented implementation of the classic Yahtzee dice game with support for multiple players, complete scoring system, and comprehensive unit tests.

## Project Structure
```
yahtzee_game/
├── dice.py         # Dice class for individual die management
├── scorecard.py    # Scorecard class for tracking player scores
├── game.py         # Game class containing main game logic
├── main.py         # Entry point for running the game
├── tests/          # Comprehensive unit test suite
│   ├── test_dice.py
│   ├── test_scorecard.py
│   ├── test_game.py
│   ├── run_tests.py
│   └── README.md
└── README.md       # This file
```

## How to Play
Run the game from the yahtzee_game directory:
```bash
python main.py
```

Follow the prompts to:
1. Enter the number of players
2. Roll dice up to 3 times per turn
3. Choose which dice to keep/reroll between rolls
4. Select a scoring category after your final roll
5. Complete 13 rounds to finish the game

## Running Tests

### Run All Tests (82 tests total)
```bash
# From the yahtzee_game directory
python -m unittest discover -s tests -p 'test_*.py' -v

# Or using the test runner script
python tests/run_tests.py
```

### Run Specific Test File
```bash
python -m unittest tests.test_dice -v        # 11 tests for Dice class
python -m unittest tests.test_scorecard -v   # 21 tests for Scorecard class
python -m unittest tests.test_game -v        # 50 tests for Game class
```

### Run Individual Test Case
```bash
python -m unittest tests.test_dice.TestDice.test_roll_returns_valid_value -v
python -m unittest tests.test_game.TestGame.test_calculate_score_yahtzee_valid -v
```

## Test Coverage
- **Dice class (11 tests)**: Initialization, face value validation, rolling, randomness
- **Scorecard class (21 tests)**: Player management, score tracking, error handling
- **Game class (50 tests)**: All 13 scoring categories, straight detection, game logic

All 82 tests pass successfully! ✓

## Game Features
- 1-6 player support
- All standard Yahtzee scoring categories:
  - Upper section: Ones, Twos, Threes, Fours, Fives, Sixes
  - Lower section: 3 of a Kind, 4 of a Kind, Full House, Small Straight, Large Straight, Yahtzee, Chance
- Interactive dice rolling with keep/reroll functionality
- Visual scorecard display with used/open slots
- Complete input validation and error handling
