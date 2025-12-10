# YahtzeePie Codebase Analysis

## Overview
This repository contains **two parallel implementations** of Yahtzee—one in **Python** (OOP) and one in **Scala** (Functional). Both are accompanied by sophisticated analysis tooling to measure performance, readability, and debugging characteristics.

---

## 1. Python Implementation (`yahtzee_game/`)

### Architecture & Design
**Paradigm:** Object-Oriented Programming (OOP)
**Structure:** Class-based with mutable state

### Core Components

#### `dice.py` - Dice Management
- **Class:** `Dice`
- **Features:**
  - Property-based face value with validation (1-6)
  - Mutable state managed via setters
  - Single die abstraction with roll capability
- **Design Pattern:** Encapsulation with property decorators

#### `scorecard.py` - Score Tracking
- **Class:** `Scorecard`
- **Features:**
  - 2D array structure: `cards[player_idx][slot_idx]`
  - Multi-player support (configurable)
  - 13 scoring slots per player (Yahtzee standard)
  - Index-based access with boundary validation
- **Storage:** Mutable list of lists `[[0]*13 for _ in range(num_players)]`

#### `game.py` - Game Logic Engine
- **Class:** `Game`
- **State Management:**
  - `dice_values` - Current values of all 5 dice
  - `sorted_dice` - Sorted version for pattern matching
  - `frequency` - Count of each die value (1-6)
  - `current_round` - Round tracker
  - `kept_indices` - Set tracking which dice are locked

**Key Methods:**

| Method | Purpose |
|--------|---------|
| `play()` | Main game loop: 13 rounds × N players |
| `roll_dice()` | Rolls all dice and updates state |
| `display_dice()` | Visual ASCII display with kept dice markers |
| `get_reroll_dice_input()` | Interactive prompt for dice selection (1-5) |
| `display_scorecard()` | Rich formatted scorecard with 80-char table |
| `get_scoring_slot_input()` | Slot selection with visual feedback |
| `calculate_score()` | Complete Yahtzee scoring algorithm |

**Game Flow:**
```
FOR each of 13 rounds:
  FOR each player:
    FOR 3 rolls:
      - Roll/reroll dice
      - Display current state
      - Ask which dice to reroll (if not final roll)
    - Display scorecard
    - Choose scoring slot
    - Calculate and record score
```

#### `main.py` - Entry Point
- Player count validation
- Game initialization
- Simple wrapper around `Game.play()`

### Notable Features

#### 1. **Interactive Dice Management**
- User selects dice to **reroll** (not keep)
- Visual indicators: brackets `[3]` show kept dice
- Dice persist their kept state across rolls unless explicitly rerolled
- 1-based indexing for user input (converted internally to 0-based)

#### 2. **Rich Scorecard Display**
```
==============================================================================
Player 1 Scorecard
==============================================================================
Slot  Category                                           Score    Status      
------------------------------------------------------------------------------
0     Ones - Sum of all ones                             -        ✓ OPEN      
1     Twos - Sum of all twos                             6        ✗ USED      
...
```
- Clear available/used indicators
- Descriptive category explanations
- Score display with proper alignment
- Re-displayed on invalid selection

#### 3. **Complete Yahtzee Scoring**
All 13 categories implemented:
- **Upper Section (0-5):** Ones through Sixes (sum matching dice)
- **Three/Four of a Kind (6-7):** Sum all dice if condition met
- **Full House (8):** 25 points fixed
- **Small Straight (9):** 30 points for 4 consecutive
- **Large Straight (10):** 40 points for 5 consecutive
- **Yahtzee (11):** 50 points for all same
- **Chance (12):** Sum all dice (always valid)

#### 4. **Error Handling**
- Input validation with retry loops
- Boundary checking on all indices
- Clear error messages for users
- Prevents reusing filled slots

### Testing
Located in `yahtzee_game/tests/`:
- `test_dice.py` - Dice rolling and validation
- `test_scorecard.py` - Score storage and retrieval
- `test_game.py` - Game logic and scoring rules
- `run_tests.py` - Test runner

---

## 2. Scala Implementation (`yahtzee_scala/`)

### Architecture & Design
**Paradigm:** Functional Programming (FP)
**Structure:** Immutable data structures with pure functions

### Core Components

#### `Dice.scala` - Immutable Dice
- **Type:** Opaque type alias (`opaque type Dice = Int`)
- **Features:**
  - Zero-overhead abstraction (compiles to `Int`)
  - Pure functional random generation with seed threading
  - Linear Congruential Generator (LCG) for determinism
  - Extension methods for value access and rolling
- **Key Innovation:** Returns `(Dice, Long)` tuples to thread RNG seed

```scala
def roll(seed: Long): (Dice, Long) =
  val newSeed = (seed * 0x5DEECE66DL + 0xBL) & 0xFFFFFFFFFFFFL
  val newValue = ((newSeed >>> 16).toInt.abs % 6) + 1
  (Dice(newValue), newSeed)
```

#### `Scorecard.scala` - Immutable Score Tracking
- **Type:** Case class with `Map[(Int, Int), Int]`
- **Features:**
  - Sparse map storage (only stores non-zero scores)
  - Returns `Either[String, T]` for error handling
  - Completely immutable - every mutation returns new instance
  - Functional error propagation

```scala
def setScore(playerIdx: Int, slotIdx: Int, value: Int): Either[String, Scorecard] =
  if playerIdx < 0 || playerIdx >= numPlayers then Left("Invalid player index")
  else if slotIdx < 0 || slotIdx >= 13 then Left("Invalid slot index")
  else Right(copy(cards = cards + ((playerIdx, slotIdx) -> value)))
```

#### `GameState.scala` - State Monad Pattern
- **Type:** Case class encapsulating entire game state
- **State:**
  - `dice: List[Dice]` - Current dice values
  - `scorecard: Scorecard` - All player scores
  - `currentPlayer: Int` - Active player index
  - `currentRound: Int` - Round counter
  - `rollsLeft: Int` - Rolls remaining in turn
  - `seed: Long` - RNG seed for pure randomness

**Key Methods:**
```scala
def rollDice(indices: Set[Int]): GameState =
  // Returns NEW GameState with updated dice and seed
  
def recordScore(slotIdx: Int): Either[String, GameState] =
  // Records score, advances player/round, returns NEW state
  
def isGameOver: Boolean = currentRound >= 13
```

#### `Game.scala` - Pure Game Logic
- **Object:** Collection of pure functions (no state)
- **Features:**
  - All functions are pure (no side effects)
  - Takes dice as input, returns results
  - Complete separation of logic from I/O
  - Testable without mocking

**Key Functions:**

| Function | Signature | Purpose |
|----------|-----------|---------|
| `rollDice` | `(List[Dice], Long) => (List[Dice], Long)` | Rolls all dice |
| `rollSpecificDice` | `(List[Dice], Set[Int], Long) => (List[Dice], Long)` | Rerolls selected |
| `getDiceValues` | `List[Dice] => List[Int]` | Extracts values |
| `getFrequency` | `List[Dice] => List[Int]` | Counts each value |
| `calculateScore` | `(List[Dice], Int) => Int` | Scoring algorithm |

#### `Main.scala` - I/O Layer
- **Function:** `@main def run(): Unit`
- **Features:**
  - Completely separated from game logic
  - Handles all user interaction
  - Pattern matching for game flow
  - Tail-recursive game loop

### Notable Features

#### 1. **Immutability Everywhere**
Every operation returns a **new** instance:
```scala
val rolled = state.rollDice(Set(0, 1, 2))  // Returns new GameState
val scored = rolled.recordScore(5)          // Returns new GameState
```
Benefits:
- No hidden state mutations
- Easy to reason about
- Thread-safe by default
- Easier debugging (state history preserved)

#### 2. **Functional Error Handling**
Uses `Either[String, T]` instead of exceptions:
```scala
scorecard.setScore(player, slot, score) match
  case Right(newCard) => // Success
  case Left(error) => // Handle error message
```

#### 3. **Pure Random Number Generation**
No `scala.util.Random` - uses LCG with explicit seed threading:
```scala
val (dice1, seed1) = rollDice(initialDice, seed)
val (dice2, seed2) = rollDice(dice1, seed1)  // Explicit seed chaining
```
Benefits:
- Fully deterministic
- Reproducible games
- Testable without mocking
- No hidden global state

#### 4. **Type Safety**
- Opaque types prevent invalid dice values at compile time
- `Either` forces error handling
- Pattern matching ensures exhaustiveness
- No null values (Option/Either instead)

#### 5. **Separation of Concerns**
```
Game.scala        → Pure logic (no I/O)
GameState.scala   → State management (no I/O)
Main.scala        → I/O and user interaction
```

### Testing
Located in `yahtzee_scala/src/test/scala/`:
- `DiceSpec.scala` - Property-based testing of dice
- `ScorecardSpec.scala` - Scorecard operations
- `GameSpec.scala` - Game logic verification
- Uses ScalaTest framework

### Build System
- **Tool:** sbt (Scala Build Tool)
- **Config:** `build.sbt`
- **Scripts:** `run.sh` for convenience
- **Dependencies:** Managed via sbt

---

## 3. Analysis Tools

### Python Analysis (`yahtzee_analysis/`)

#### `performance_profiler.py`
- Uses `cProfile` for function-level profiling
- Measures execution time and call counts
- Identifies bottlenecks in game loop

#### `cprofile_analyzer.py`
- Parses cProfile output
- Generates statistical reports
- Visualizes performance hotspots

#### `readability_analyzer.py`
- McCabe complexity analysis
- Lines of code metrics
- Comment density calculation
- Function length distribution

#### `debugging_analyzer.py`
- Analyzes logging statements
- Exception handling patterns
- Error message quality
- Debugging complexity metrics

#### `visualizer.py`
- Matplotlib-based visualizations
- Performance graphs
- Complexity heatmaps
- Comparison charts

### Scala Analysis (`yahtzee_scala_analysis/`)

#### `performance_profiler.scala`
- JVM profiling integration
- Heap usage analysis
- GC pressure measurement
- Pure function performance

#### `readability_analyzer.py`
- Similar to Python version
- Adapted for Scala syntax
- Functional complexity metrics

#### `debugging_analyzer.py`
- Analyzes Either-based error handling
- Pattern match exhaustiveness
- Type safety metrics

#### `visualizer.py`
- Cross-language comparison charts
- Side-by-side performance metrics

### Analysis Output
Both tools generate:
- **Data:** JSON/CSV files in `data/`
- **Visualizations:** PNG charts in `visualizations/`
- **Reports:** Markdown summaries
- **Scripts:** `run_analysis.sh` for automation

---

## Comparison Summary

| Aspect | Python (OOP) | Scala (FP) |
|--------|--------------|------------|
| **Paradigm** | Object-Oriented | Functional |
| **State** | Mutable | Immutable |
| **Error Handling** | Exceptions + validation | Either monad |
| **Randomness** | `random.randint()` | Pure LCG with seed |
| **Testing** | Unit tests | Unit + property tests |
| **Type Safety** | Dynamic (runtime) | Static (compile-time) |
| **Concurrency** | Not thread-safe | Thread-safe by default |
| **Code Style** | Imperative loops | Declarative pipelines |
| **Debugging** | Mutable state inspection | State history tracking |
| **Performance** | Good (interpreted) | Excellent (JVM compiled) |
| **Learning Curve** | Easier for beginners | Steeper (FP concepts) |
| **Predictability** | Side effects possible | Fully deterministic |

## Architecture Patterns

### Python: Classic OOP
```
Game (orchestrator)
 ├─> Dice (5 instances, mutable)
 ├─> Scorecard (nested lists, mutable)
 └─> User I/O (mixed with logic)
```

### Scala: Functional Core, Imperative Shell
```
Main (I/O shell)
 └─> GameState (immutable state container)
      ├─> Dice (pure opaque types)
      ├─> Scorecard (immutable map)
      └─> Game (pure logic functions)
```

## Key Innovations

### Python Implementation
1. **Interactive dice keeping system** - Reroll selection with visual feedback
2. **Rich scorecard display** - 80-character formatted table with status indicators
3. **User-friendly indexing** - 1-based input converted to 0-based internally
4. **Comprehensive testing suite** - Full coverage of game logic

### Scala Implementation
1. **Opaque types** - Zero-cost abstraction for dice (compiles to Int)
2. **Pure RNG** - Deterministic random generation with explicit seed threading
3. **Either-based errors** - Functional error handling without exceptions
4. **Complete immutability** - All state transitions explicit and traceable
5. **Separation of I/O from logic** - Pure core, imperative shell pattern

## Use Cases

**Choose Python when:**
- Rapid prototyping needed
- Team familiar with OOP
- Interactive debugging preferred
- Simple deployment required

**Choose Scala when:**
- Type safety critical
- Concurrency needed
- Pure functions desired
- JVM ecosystem required
- Deterministic behavior essential

---

## File Structure Summary

```
YahtzeePie/
├── yahtzee_game/               # Python OOP implementation
│   ├── dice.py                 # Mutable Dice class
│   ├── scorecard.py            # Mutable Scorecard class
│   ├── game.py                 # Game orchestrator (234 lines)
│   ├── main.py                 # Entry point
│   └── tests/                  # Unit tests
│
├── yahtzee_scala/              # Scala FP implementation
│   ├── build.sbt               # SBT build config
│   ├── src/main/scala/yahtzee/
│   │   ├── Dice.scala         # Opaque type with pure RNG
│   │   ├── Scorecard.scala    # Immutable case class
│   │   ├── GameState.scala    # State monad
│   │   ├── Game.scala         # Pure logic functions
│   │   └── Main.scala         # I/O layer (110 lines)
│   └── src/test/scala/        # ScalaTest specs
│
├── yahtzee_analysis/           # Python analysis tools
│   ├── performance_profiler.py
│   ├── readability_analyzer.py
│   ├── debugging_analyzer.py
│   └── visualizer.py
│
└── yahtzee_scala_analysis/     # Scala analysis tools
    ├── performance_profiler.scala
    ├── readability_analyzer.py
    ├── debugging_analyzer.py
    └── visualizer.py
```

## Conclusion

This repository demonstrates **two philosophically different approaches** to the same problem:

- **Python:** Pragmatic, imperative, mutable state, familiar OOP patterns
- **Scala:** Principled, declarative, immutable data, functional purity

Both are **fully functional Yahtzee implementations** with complete game logic, user interaction, and comprehensive testing. The analysis tools provide empirical data to compare readability, performance, and debugging characteristics of each paradigm.

The project serves as an excellent **educational resource** for understanding the trade-offs between OOP and FP, and demonstrates that both approaches can produce high-quality, maintainable code when applied thoughtfully.
