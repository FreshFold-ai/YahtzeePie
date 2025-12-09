# Yahtzee Python Implementation - Analysis

Comprehensive analysis framework that profiles the Python OOP implementation across three dimensions:
1. **Performance**: Execution time and memory usage for all 33 methods
2. **Readability**: Lines of code, comments, and cyclomatic complexity
3. **Debugging**: Code quality (pylint) and test coverage

## Overview

This analysis suite evaluates the yahtzee_game implementation by:
- Profiling all methods in Dice (4), Scorecard (4), and Game (25) classes
- **Statistical rigor**: 4 trials × 21 samples = 84 measurements per method
- Measuring execution time with standard deviation (e.g., 0.0027±0.0002ms)
- Measuring memory usage with confidence intervals (e.g., 0.09±0.05KB)
- Analyzing code structure across 4 files (300 total lines: 242 code, 10 comments)
- Generating visual charts with error bars for easy interpretation

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
- Execution time (milliseconds) - Mean ± Std Dev format
- Memory used (kilobytes) - Mean ± Std Dev format
- Peak memory (kilobytes)
- Statistical metadata: num_trials, samples_per_trial

**Statistical Methodology:**
- **4 independent trials** to account for system state variations
- **21 samples per trial** (84 total measurements per method)
- Results reported as Mean ± Standard Deviation
- Example: `0.0027±0.0002ms` means 0.0027ms average with 0.0002ms std dev

**Output:** `data/performance_metrics.json`

**Key Findings:**
- Fastest: Getters/setters (~0.0004-0.0006ms avg)
- Most expensive: `display_scorecard` (~0.23ms avg, ~17KB avg)
- Scoring operations: ~0.006-0.052ms avg range
- Low standard deviations indicate consistent performance

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
Running performance analysis...
Configuration: 5 trials × 50 samples per trial
================================================================================

DICE
--------------------------------------------------------------------------------
  dice_init                      | Time:  0.0058±0.0016ms | Memory:    0.08± 0.02KB
  dice_roll                      | Time:  0.0028±0.0005ms | Memory:    0.00± 0.00KB
  ...

GAME
--------------------------------------------------------------------------------
  game_calculate_score_yahtzee   | Time:  0.0143±0.0009ms | Memory:    0.00± 0.00KB
  game_display_scorecard         | Time:  0.2572±0.0981ms | Memory:   14.28±10.05KB
  ...

Results saved to: data/performance_metrics.json
Statistics: Mean ± Std Dev from 5 trials

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
