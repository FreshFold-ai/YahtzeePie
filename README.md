# YahtzeePie

Yahtzee implementations in Python (OOP) and Scala (Functional).

## Implementations

### Python - Object-Oriented
```bash
cd yahtzee_game
./run.sh
```
- 82 unit tests
- Mutable state with classes
- See [yahtzee_game/README.md](yahtzee_game/README.md)

### Scala - Functional
```bash
cd yahtzee_scala
./run.sh
```
- 30 unit tests
- Pure functions, immutable data
- See [yahtzee_scala/README.md](yahtzee_scala/README.md)

## Analysis

### Python Implementation Analysis
```bash
cd yahtzee_analysis
./run_analysis.sh
```
- Performance metrics (time & memory)
- Readability analysis (LOC & complexity)
- Debugging metrics (pylint & coverage)
- Visual charts & graphs
- See [yahtzee_analysis/README.md](yahtzee_analysis/README.md)

## Testing

```bash
# Python tests
cd yahtzee_game && python -m unittest discover -s tests -v

# Scala tests
cd yahtzee_scala && sbt test
```
