# YahtzeePie - Python OOP Implementation

Object-oriented Yahtzee with comprehensive unit tests.

## Structure
```
yahtzee_game/
├── dice.py         # Dice class
├── scorecard.py    # Scorecard class
├── game.py         # Game logic
├── main.py         # Entry point
├── run.sh          # Run script
├── tests/          # Unit test suite (82 tests)
└── README.md
```

## Run the Game

```bash
./run.sh
# or
python main.py
```

## Run Tests

```bash
# All tests
python -m unittest discover -s tests -p 'test_*.py' -v

# Specific test file
python -m unittest tests.test_dice -v
python -m unittest tests.test_scorecard -v
python -m unittest tests.test_game -v
```

## Test Coverage

- **11 tests** - Dice class
- **21 tests** - Scorecard class  
- **50 tests** - Game logic (all scoring categories)
- **82 total** - All passing ✓

## Features

- 1+ player support
- All standard Yahtzee scoring
- Interactive rolling with keep/reroll
- Input validation
