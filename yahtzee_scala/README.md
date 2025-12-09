# Yahtzee - Functional Scala 3

Pure functional Yahtzee with immutable data structures.

## Structure
```
yahtzee_scala/
├── src/main/scala/yahtzee/
│   ├── Dice.scala       # Opaque type with pure RNG
│   ├── Scorecard.scala  # Immutable scorecard
│   ├── Game.scala       # Pure scoring functions
│   ├── GameState.scala  # Immutable state
│   └── Main.scala       # IO boundary
├── src/test/scala/yahtzee/
│   ├── DiceSpec.scala
│   ├── ScorecardSpec.scala
│   └── GameSpec.scala
├── run.sh              # Run script
└── README.md
```

## Run the Game

```bash
./run.sh
# or
sbt run
```

## Run Tests

```bash
sbt test
```

## Test Coverage

- **6 tests** - Dice (opaque type)
- **8 tests** - Scorecard (immutable operations)
- **16 tests** - Game logic (all scoring)
- **30 total** - All passing ✓

## Design

- **Immutability** - All values immutable
- **Pure Functions** - No side effects in core logic
- **Opaque Types** - Dice as zero-cost abstraction
- **Pure RNG** - Explicit seed threading (LCG)
- **Either** - Error handling without exceptions
- **IO Isolation** - Side effects only in Main
