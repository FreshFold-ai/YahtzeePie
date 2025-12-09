#!/bin/bash
cd "$(dirname "$0")"

echo "Scala Functional Implementation Analysis"
echo "========================================="
echo ""

# Check if SBT is available
if ! command -v sbt &> /dev/null; then
    echo "⚠️  SBT not found. Please install SBT to run performance profiler."
    echo "   You can run the Python analyzers independently."
    echo ""
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -q matplotlib 2>/dev/null || echo "⚠️  Warning: matplotlib installation failed"

echo ""
echo "Running Scala analysis suite..."
echo "================================="

# 1. Performance profiling (Scala)
echo ""
echo "1️⃣  Performance Profiling (Scala)..."
echo "   Compiling and running Scala profiler..."
if command -v sbt &> /dev/null; then
    # Compile the profiler with the main yahtzee code
    cd ../yahtzee_scala
    
    # Copy profiler to src/main/scala/analysis
    mkdir -p src/main/scala/analysis
    cp ../yahtzee_scala_analysis/performance_profiler.scala src/main/scala/analysis/
    
    # Compile and run
    sbt "runMain analysis.PerformanceProfiler" 2>&1 | grep -v "^\[" | tail -50
    
    # Move output to analysis folder
    if [ -f "data/performance_metrics.json" ]; then
        mv data/performance_metrics.json ../yahtzee_scala_analysis/data/
        echo "   ✓ Performance metrics saved"
    fi
    
    # Clean up
    rm -rf src/main/scala/analysis
    
    cd ../yahtzee_scala_analysis
else
    echo "   ⚠️  Skipped (SBT not available)"
fi

# 2. Readability analysis
echo ""
echo "2️⃣  Readability Analysis..."
python3 readability_analyzer.py 2>&1 | tail -30

# 3. Debugging analysis
echo ""
echo "3️⃣  Debugging Analysis..."
python3 debugging_analyzer.py 2>&1 | tail -30

# 4. Generate visualizations
echo ""
echo "4️⃣  Generating Visualizations..."
python3 visualizer.py 2>&1 | grep -E "(saved|generated|Generating)"

echo ""
echo "================================="
echo "Analysis complete! 📊"
echo ""
echo "📁 Results location:"
echo "   - data/              Raw metrics (JSON)"
echo "   - visualizations/    Charts (PNG)"
echo "   - README.md          Documentation"
echo ""
echo "💡 View the visualizations:"
echo "   - performance_metrics.png"
echo "   - readability_metrics.png"
echo "   - debugging_metrics.png"
echo "   - summary.png"
