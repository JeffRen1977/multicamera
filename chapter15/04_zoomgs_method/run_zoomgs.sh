#!/bin/bash
# run_zoomgs.sh
# Wrapper script to run ZoomGS (Dual-Camera Smooth Zoom) inference
# This script clones and sets up the ZoomGS repository if not already present

set -e

# Configuration
ZOOMGS_REPO="https://github.com/ZcsrenlongZ/ZoomGS.git"
ZOOMGS_DIR="../thirdparty/ZoomGS"
VENV_DIR="zoomgs_venv"
INPUT_WIDE="$1"
INPUT_TELE="$2"
OUTPUT_DIR="$3"
CHECKPOINT_URL="https://github.com/ZcsrenlongZ/ZoomGS/releases/download/v1.0/zoomgs_model.pth"

# Check if inputs are provided
if [ $# -lt 3 ]; then
    echo "Usage: $0 <wide_image> <tele_image> <output_dir>"
    echo "Example: $0 samples/wide.jpg samples/tele.jpg results/zoomgs"
    exit 1
fi

echo "Setting up ZoomGS for Dual-Camera Smooth Zoom..."

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Clone ZoomGS repository if not exists
if [ ! -d "$ZOOMGS_DIR" ]; then
    echo "Cloning ZoomGS repository..."
    git clone "$ZOOMGS_REPO" "$ZOOMGS_DIR"
else
    echo "ZoomGS repository already exists, updating..."
    cd "$ZOOMGS_DIR"
    git pull
    cd - > /dev/null
fi

# Create virtual environment if not exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python -m venv "$VENV_DIR"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Install dependencies
echo "Installing dependencies..."
pip install -r "$ZOOMGS_DIR/requirements.txt" || {
    echo "Installing basic dependencies..."
    pip install torch torchvision opencv-python numpy pillow scikit-image
}

# Download checkpoint if not exists
CHECKPOINT_PATH="$ZOOMGS_DIR/checkpoints/zoomgs_model.pth"
if [ ! -f "$CHECKPOINT_PATH" ]; then
    echo "Downloading ZoomGS checkpoint..."
    mkdir -p "$ZOOMGS_DIR/checkpoints"
    wget -O "$CHECKPOINT_PATH" "$CHECKPOINT_URL" || {
        echo "Warning: Could not download checkpoint. Please download manually from:"
        echo "$CHECKPOINT_URL"
        echo "And place it at: $CHECKPOINT_PATH"
    }
fi

# Run ZoomGS inference
echo "Running ZoomGS inference..."
cd "$ZOOMGS_DIR"

# Check if test script exists and run it
if [ -f "test.py" ]; then
    python test.py \
        --input_w "$INPUT_WIDE" \
        --input_t "$INPUT_TELE" \
        --checkpoint "$CHECKPOINT_PATH" \
        --out "$OUTPUT_DIR"
elif [ -f "inference.py" ]; then
    python inference.py \
        --wide "$INPUT_WIDE" \
        --tele "$INPUT_TELE" \
        --checkpoint "$CHECKPOINT_PATH" \
        --output "$OUTPUT_DIR"
elif [ -f "demo.py" ]; then
    python demo.py \
        --wide "$INPUT_WIDE" \
        --tele "$INPUT_TELE" \
        --checkpoint "$CHECKPOINT_PATH" \
        --output "$OUTPUT_DIR"
else
    echo "Error: Could not find test.py, inference.py, or demo.py in ZoomGS repository"
    echo "Please check the repository structure and update this script accordingly"
    exit 1
fi

cd - > /dev/null

echo "ZoomGS inference completed!"
echo "Results saved to: $OUTPUT_DIR"

# Deactivate virtual environment
deactivate



