#!/bin/bash
# run_quick_test.sh
# Quick test script - runs a single fusion experiment in under 5 seconds

echo "🚀 Quick Multi-Camera Fusion Test"
echo "=================================="
echo ""

# Activate virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        echo "✅ Virtual environment activated"
    else
        echo "❌ Virtual environment not found"
        echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
        exit 1
    fi
fi

# Check if sample data exists
if [ ! -f "samples/sample_01/wide.jpg" ]; then
    echo "📸 Creating sample data..."
    python multicam/create_sample_data.py --num_samples 1 --output samples
fi

# Run fusion
echo ""
echo "🔬 Running fusion..."
python multicam/align_and_fuse.py \
    --wide samples/sample_01/wide.jpg \
    --tele samples/sample_01/tele.jpg \
    --out results/quick_test

echo ""
echo "✅ Quick test completed!"
echo ""
echo "📁 Results saved to: results/quick_test/"
echo "   - fused.png (main result)"
echo "   - composite.png (side-by-side comparison)"
echo "   - digital_zoom.png (baseline)"
echo ""
echo "View results: open results/quick_test/composite.png"

