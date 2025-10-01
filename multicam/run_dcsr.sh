#!/bin/bash
# run_dcsr.sh
# Wrapper script to run DCSR (Dual-Camera Super-Resolution) inference
# This script clones and sets up the DCSR repository if not already present

set -e

# Configuration
DCSR_REPO="https://github.com/Tengfei-Wang/DCSR.git"
DCSR_DIR="../thirdparty/DCSR"
VENV_DIR="dcsr_venv"
INPUT_WIDE="$1"
INPUT_TELE="$2"
OUTPUT_DIR="$3"
CHECKPOINT_URL="https://github.com/Tengfei-Wang/DCSR/releases/download/v1.0/dcsr_model.pth"

# Check if inputs are provided
if [ $# -lt 3 ]; then
    echo "Usage: $0 <wide_image> <tele_image> <output_dir>"
    echo "Example: $0 samples/wide.jpg samples/tele.jpg results/dcsr"
    exit 1
fi

echo "Setting up DCSR for Dual-Camera Super-Resolution..."

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Clone DCSR repository if not exists
if [ ! -d "$DCSR_DIR" ]; then
    echo "Cloning DCSR repository..."
    git clone "$DCSR_REPO" "$DCSR_DIR"
else
    echo "DCSR repository already exists, updating..."
    cd "$DCSR_DIR"
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
pip install -r "$DCSR_DIR/requirements.txt" || {
    echo "Installing basic dependencies..."
    pip install torch torchvision opencv-python numpy pillow scikit-image
}

# Download checkpoint if not exists
CHECKPOINT_PATH="$DCSR_DIR/checkpoints/dcsr_model.pth"
if [ ! -f "$CHECKPOINT_PATH" ]; then
    echo "Downloading DCSR checkpoint..."
    mkdir -p "$DCSR_DIR/checkpoints"
    wget -O "$CHECKPOINT_PATH" "$CHECKPOINT_URL" || {
        echo "Warning: Could not download checkpoint. Please download manually from:"
        echo "$CHECKPOINT_URL"
        echo "And place it at: $CHECKPOINT_PATH"
    }
fi

# Run DCSR inference
echo "Running DCSR inference..."
cd "$DCSR_DIR"

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
else
    echo "Error: Could not find test.py or inference.py in DCSR repository"
    echo "Please check the repository structure and update this script accordingly"
    exit 1
fi

cd - > /dev/null

echo "DCSR inference completed!"
echo "Results saved to: $OUTPUT_DIR"

# Deactivate virtual environment
deactivate



