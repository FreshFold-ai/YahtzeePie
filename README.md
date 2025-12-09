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
- Performance metrics (33 methods profiled: 0.002-0.6ms range)
- Readability analysis (300 lines: 242 code, 10 comments)
- Debugging metrics (pylint & coverage)
- Visual charts & graphs
- See [yahtzee_analysis/README.md](yahtzee_analysis/README.md)

### Scala Implementation Analysis
```bash
cd yahtzee_scala_analysis
./run_analysis.sh
```
- Performance metrics (30 methods profiled: 0.0003-0.02ms range)
- Readability analysis (263 lines: 212 code, 0 comments)
- Functional patterns (100% immutability, pure functions)
- Test coverage (30 tests, 100% pass rate)
- Visual charts & graphs
- See [yahtzee_scala_analysis/README.md](yahtzee_scala_analysis/README.md)

### Comparison
Both analysis frameworks provide:
- Execution time and memory profiling
- Code structure metrics
- Quality and testing statistics
- Beautiful PNG visualizations

Compare OOP vs Functional approaches across multiple dimensions!

## Testing

```bash
# Python tests
cd yahtzee_game && python -m unittest discover -s tests -v

# Scala tests
cd yahtzee_scala && sbt test
```
