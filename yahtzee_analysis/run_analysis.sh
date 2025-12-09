#!/bin/bash
cd "$(dirname "$0")"

echo "Installing analysis dependencies..."
pip install -q matplotlib radon pylint coverage 2>/dev/null

echo ""
echo "Running all analyses..."
echo "======================"

echo ""
echo "1. Performance Profiling..."
python performance_profiler.py

echo ""
echo "2. cProfile Analysis..."
python cprofile_analyzer.py

echo ""
echo "3. Readability Analysis..."
python readability_analyzer.py

echo ""
echo "4. Debugging Analysis..."
python debugging_analyzer.py

echo ""
echo "5. Generating Visualizations..."
python visualizer.py

echo ""
echo "======================"
echo "Analysis complete! Check the following:"
echo "  - data/ for raw metrics (JSON)"
echo "  - visualizations/ for charts (PNG)"
echo "  - README.md for documentation"
