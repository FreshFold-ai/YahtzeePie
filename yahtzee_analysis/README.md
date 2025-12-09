# Yahtzee Python Implementation - Analysis

Comprehensive analysis framework that profiles the Python OOP implementation across three dimensions:
1. **Performance**: Execution time and memory usage for all 33 methods
2. **Readability**: Lines of code, comments, and cyclomatic complexity
3. **Debugging**: Code quality (pylint) and test coverage

## Overview

This analysis suite evaluates the yahtzee_game implementation by:
- Profiling all methods in Dice (4), Scorecard (4), and Game (25) classes
- Measuring execution time (0.002-0.6ms range) and memory usage (0-3.21KB range)
- Analyzing code structure across 4 files (300 total lines: 242 code, 10 comments)
- Generating visual charts for easy interpretation

## Quick Start

Run all analyses and generate visualizations with a single command:

```bash
./run_analysis.sh
```

This will:
1. Profile all 33 methods for performance metrics
2. Analyze code readability and complexity
3. Check code quality with pylint
4. Measure test coverage
5. Generate PNG charts in `visualizations/`
6. Save all metrics to JSON files in `data/`

## Structure

```
yahtzee_analysis/
├── performance_profiler.py    # Execution time & memory profiling
├── cprofile_analyzer.py        # Detailed call profiling
├── readability_analyzer.py     # LOC & complexity metrics
├── debugging_analyzer.py       # Pylint & test coverage
├── visualizer.py               # Generate charts
├── run_analysis.sh             # Run all analyses
├── data/                       # JSON metrics output
└── visualizations/             # PNG charts
```

## Running the Complete Analysis

### Single Command (Recommended)

```bash
./run_analysis.sh
```

This automated script:
- Runs all 4 analysis tools sequentially
- Generates comprehensive metrics in `data/`
- Creates visual charts in `visualizations/`
- Takes approximately 10-30 seconds to complete

### Expected Output

After running `./run_analysis.sh`, you'll have:

**Data Files:**
- `data/performance_metrics.json` - All 33 methods profiled
- `data/readability_metrics.json` - LOC and complexity for 4 files
- `data/pylint_metrics.json` - Code quality issues
- `data/coverage.json` - Test coverage percentage

**Visualizations:**
- `visualizations/performance_metrics.png` - Execution time & memory charts
- `visualizations/readability_metrics.png` - Code structure breakdown
- `visualizations/debugging_metrics.png` - Pylint issue distribution
- `visualizations/summary.png` - Combined overview

## Individual Analyses

### Performance Analysis

Measures execution time and memory usage for all 33 methods across Dice, Scorecard, and Game classes.

```bash
python performance_profiler.py
```

**Covers:**
- Dice: 4 methods (init, roll, face_value getter/setter)
- Scorecard: 4 methods (init, get_score, set_score, get_player_card)
- Game: 25 methods (dice ops, scoring for all 13 categories, straights, display)

**Metrics:**
- Execution time (milliseconds) - Range: 0.002ms to 0.6ms
- Memory used (kilobytes) - Range: 0KB to 3.21KB
- Peak memory (kilobytes)

**Output:** `data/performance_metrics.json`

**Key Findings:**
- Fastest: Getters/setters (~0.002-0.005ms)
- Most expensive: `display_scorecard` (0.6ms, 3.21KB)
- Scoring operations: ~0.01-0.04ms range

### cProfile Analysis

Detailed profiling with call counts and cumulative time.

```bash
python cprofile_analyzer.py
```

**Output:** `data/cprofile_output.txt`

### Readability Analysis

Lines of code and complexity metrics using radon.

```bash
python readability_analyzer.py
```

**Metrics:**
- Total lines, code lines, comment lines, blank lines
- Cyclomatic complexity (radon)
- Maintainability index (radon)

**Output:** `data/readability_metrics.json`

### Debugging Analysis

Code quality and test coverage.

```bash
python debugging_analyzer.py
```

**Tools:**
- pylint - Code quality issues
- coverage - Test coverage percentage

**Output:** 
- `data/pylint_metrics.json`
- `data/coverage.json`

### Visualizations

Generate charts from all metrics.

```bash
python visualizer.py
```

**Charts:**
- `visualizations/performance_metrics.png` - Execution time & memory
- `visualizations/readability_metrics.png` - LOC distribution
- `visualizations/debugging_metrics.png` - Pylint issues
- `visualizations/summary.png` - Overall summary

## Dependencies

```bash
pip install matplotlib radon pylint coverage
```

## Data Storage

All metrics are stored as JSON in `data/`:
- `performance_metrics.json` - Method timing & memory
- `cprofile_output.txt` - Profiler output
- `readability_metrics.json` - LOC & complexity
- `pylint_metrics.json` - Code quality issues
- `coverage.json` - Test coverage data

## Interpreting Results

### Performance
- Lower execution time = faster methods
- Lower memory usage = more efficient

### Readability
- Higher comment ratio = better documentation
- Lower cyclomatic complexity = easier to maintain
- Maintainability index: A (high) to F (low)

### Debugging
- Fewer pylint issues = better code quality
- Higher coverage % = better tested
- Issue types: convention, refactor, warning, error

## Sample Output

When you run `./run_analysis.sh`, you'll see output like:

```
Running all analyses...
======================

1. Performance Profiling...
DICE
----------------------------------------------------------------------
  dice_init                      | Time:   0.0095ms | Memory:     0.26KB
  dice_roll                      | Time:   0.0046ms | Memory:     0.00KB
  ...

GAME
----------------------------------------------------------------------
  game_calculate_score_yahtzee   | Time:   0.0129ms | Memory:     0.06KB
  game_display_scorecard         | Time:   0.6043ms | Memory:     3.21KB
  ...

2. cProfile Analysis...
3. Readability Analysis...
4. Debugging Analysis...
5. Generating Visualizations...

======================
Analysis complete! Check the following:
  - data/ for raw metrics (JSON)
  - visualizations/ for charts (PNG)
  - README.md for documentation
```

All results are saved to files for further analysis or comparison over time.

## Troubleshooting

**Missing dependencies:**
```bash
pip install matplotlib radon pylint coverage
```

**Permission denied:**
```bash
chmod +x run_analysis.sh
```

**Import errors:**
Ensure you're running from the `yahtzee_analysis/` directory or that the parent `yahtzee_game/` folder exists.
