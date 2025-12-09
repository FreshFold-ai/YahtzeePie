# Yahtzee Game Unit Tests

This directory contains comprehensive unit tests for all classes and methods in the Yahtzee game implementation.

## Test Coverage

### test_dice.py (11 tests)
Tests for the `Dice` class:
- Initialization and face value validation
- Face value getter and setter (valid and invalid values)
- Roll functionality
- Independence of multiple dice instances
- Randomness verification

### test_scorecard.py (21 tests)
Tests for the `Scorecard` class:
- Initialization for single and multiple players
- Getting scores with valid/invalid indices
- Setting scores with valid/invalid indices
- Getting player cards
- Score independence between players and slots
- Error handling for out-of-range indices

### test_game.py (50 tests)
Tests for the `Game` class:
- Game initialization
- Dice rolling and value management
- Score calculation for all 13 categories:
  - Ones through Sixes (slots 0-5)
  - Three of a Kind (slot 6)
  - Four of a Kind (slot 7)
  - Full House (slot 8)
  - Small Straight (slot 9)
  - Large Straight (slot 10)
  - Yahtzee (slot 11)
  - Chance (slot 12)
- Straight detection (small and large)
- User input handling for rerolling dice
- Frequency counting

## Running the Tests

### Run All Tests

```bash
# From the yahtzee_game directory
python -m unittest discover -s tests -p 'test_*.py' -v

# Or using the test runner script
python tests/run_tests.py
```

### Run Specific Test File

```bash
# From the yahtzee_game directory
python -m unittest tests.test_dice -v
python -m unittest tests.test_scorecard -v
python -m unittest tests.test_game -v
```

### Run Individual Test Case

```bash
# From the yahtzee_game directory
python -m unittest tests.test_dice.TestDice.test_roll_returns_valid_value -v
python -m unittest tests.test_game.TestGame.test_calculate_score_yahtzee_valid -v
```

## Test Results

All 82 tests pass successfully:
- ✓ 11 tests for Dice class
- ✓ 21 tests for Scorecard class
- ✓ 50 tests for Game class

## Test Structure

Each test follows the Arrange-Act-Assert pattern:
1. **Arrange**: Set up test conditions
2. **Act**: Execute the method being tested
3. **Assert**: Verify the expected outcome

Tests include:
- Happy path testing (valid inputs and expected behavior)
- Edge case testing (boundary conditions)
- Error handling testing (invalid inputs, exceptions)
- State verification testing (ensuring proper state changes)
- Independence testing (ensuring objects don't interfere with each other)

## Dependencies

Tests use Python's built-in `unittest` framework and `unittest.mock` for mocking user input. No external dependencies required.
