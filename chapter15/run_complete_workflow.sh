#!/bin/bash
# run_complete_workflow.sh
# Complete workflow for Chapter 15: Multi-Camera Fusion
# Runs all sections in order: Setup → Classical → Evaluation

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate virtual environment (check parent directory first)
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -f "../../venv/bin/activate" ]; then
        source ../../venv/bin/activate
        echo "✅ Virtual environment activated from parent directory"
    elif [ -f "../venv/bin/activate" ]; then
        source ../venv/bin/activate
        echo "✅ Virtual environment activated"
    else
        echo "❌ Virtual environment not found"
        echo "Please run in parent directory:"
        echo "  cd ../.."
        echo "  python3 -m venv venv"
        echo "  source venv/bin/activate"
        echo "  pip install -r MultiCamera/requirements.txt"
        exit 1
    fi
fi

# Verify we're using the correct Python
if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ Virtual environment not activated"
    exit 1
fi

# Use Python from virtual environment explicitly
PYTHON_CMD="$VIRTUAL_ENV/bin/python"
if [ ! -f "$PYTHON_CMD" ]; then
    PYTHON_CMD="python"
fi

echo "Using Python: $PYTHON_CMD"
echo "Python version: $($PYTHON_CMD --version)"

# Verify required packages are installed
echo "Checking required packages..."
if ! $PYTHON_CMD -c "import cv2, numpy, skimage, lpips" 2>/dev/null; then
    echo "❌ Missing required packages. Installing..."
    $PYTHON_CMD -m pip install --upgrade pip
    
    # Find requirements.txt (from chapter15/, it's one level up in MultiCamera root)
    REQ_FILE="../requirements.txt"
    if [ ! -f "$REQ_FILE" ]; then
        echo "❌ Could not find requirements.txt at $REQ_FILE"
        echo "Current directory: $(pwd)"
        echo "Please install packages manually:"
        echo "   pip install scikit-image opencv-python numpy"
        exit 1
    fi
    
    $PYTHON_CMD -m pip install -r "$REQ_FILE"
    if ! $PYTHON_CMD -c "import cv2, numpy, skimage" 2>/dev/null; then
        echo "❌ Failed to install packages. Please run manually:"
        echo "   pip install scikit-image opencv-python numpy"
        exit 1
    fi
    echo "✅ Packages installed"
fi
echo ""

echo "=========================================="
echo "Chapter 15: Complete Workflow"
echo "=========================================="
echo ""

# Step 1: Setup - Generate sample data
echo "[1/3] Setting up sample data..."
cd 01_setup
$PYTHON_CMD create_sample_data.py --num_samples 1 --output ../data
cd ..
echo "✓ Sample data created"
echo ""

# Step 2: Classical Method - Run fusion
echo "[2/3] Running classical fusion method..."
cd 02_classical_method
$PYTHON_CMD align_and_fuse.py \
    --wide ../data/sample_01/wide.jpg \
    --tele ../data/sample_01/tele.jpg \
    --out ../results/classical \
    --visualize
cd ..
echo "✓ Classical fusion completed"
echo ""

# Step 3: Evaluation - Compute metrics
echo "[3/3] Evaluating results..."
cd 05_evaluation
$PYTHON_CMD eval_multicam.py \
    --fused ../results/classical/fused.png \
    --wide ../results/classical/wide.png \
    --tele_warp ../results/classical/tele_warp.png \
    --digital_zoom ../results/classical/digital_zoom.png \
    --output ../results/classical/metrics.json \
    --csv ../results/classical/metrics.csv
cd ..
echo "✓ Evaluation completed"
echo ""

echo "=========================================="
echo "Workflow completed successfully!"
echo "=========================================="
echo ""
echo "Results saved to:"
echo "  - Images: chapter15/results/classical/"
echo "  - Metrics: chapter15/results/classical/metrics.json"
echo ""
echo "To view results:"
echo "  open chapter15/results/classical/composite.png"
echo "  cat chapter15/results/classical/metrics.json"
echo ""

