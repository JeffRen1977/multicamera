#!/bin/bash
# run_all.sh
# Complete workflow script to run all multi-camera fusion experiments
# This script runs: sample generation → classical fusion → evaluation → comparison

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   Multi-Camera Fusion - Complete Experimental Pipeline    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
SAMPLE_DIR="samples"
RESULTS_DIR="results"
NUM_SAMPLES=3

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not activated${NC}"
    echo "Activating virtual environment from parent directory..."
    if [ -f "../venv/bin/activate" ]; then
        source ../venv/bin/activate
    elif [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    else
        echo -e "${RED}❌ Virtual environment not found. Please run in parent directory:${NC}"
        echo "   cd .."
        echo "   python3 -m venv venv"
        echo "   source venv/bin/activate"
        echo "   pip install -r MultiCamera/requirements.txt"
        exit 1
    fi
fi

echo -e "${GREEN}✅ Virtual environment active${NC}"
echo ""

# Step 1: Generate sample data
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}Step 1: Generating Sample Data${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ ! -d "$SAMPLE_DIR/sample_01" ]; then
    python chapter15/01_setup/create_sample_data.py \
        --num_samples $NUM_SAMPLES \
        --output $SAMPLE_DIR
    echo -e "${GREEN}✅ Sample data created${NC}"
else
    echo -e "${YELLOW}⚠️  Sample data already exists, skipping...${NC}"
fi

echo ""

# Step 2: Run classical fusion method
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}Step 2: Running Classical Fusion Method${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

python chapter15/02_classical_method/align_and_fuse.py \
    --wide $SAMPLE_DIR/sample_01/wide.jpg \
    --tele $SAMPLE_DIR/sample_01/tele.jpg \
    --out $RESULTS_DIR/classical_method \
    --visualize \
    --alpha 1.0

echo -e "${GREEN}✅ Classical fusion completed${NC}"
echo ""

# Step 3: Evaluate results
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}Step 3: Evaluating Fusion Quality${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

python chapter15/05_evaluation/eval_multicam.py \
    --fused $RESULTS_DIR/classical_method/fused.png \
    --wide $RESULTS_DIR/classical_method/wide.png \
    --tele_warp $RESULTS_DIR/classical_method/tele_warp.png \
    --digital_zoom $RESULTS_DIR/classical_method/digital_zoom.png \
    --confidence_mask $RESULTS_DIR/classical_method/confidence_mask.png \
    --output $RESULTS_DIR/classical_method/evaluation.json \
    --csv $RESULTS_DIR/classical_method/evaluation.csv

echo -e "${GREEN}✅ Evaluation completed${NC}"
echo ""

# Step 4: Show results summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}Step 4: Results Summary${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "📁 Generated Files:"
echo "   Input samples: $SAMPLE_DIR/sample_01/"
echo "   Fusion results: $RESULTS_DIR/classical_method/"
echo ""
echo "📊 Key Results:"
if [ -f "$RESULTS_DIR/classical_method/evaluation.json" ]; then
    python -c "
import json
with open('$RESULTS_DIR/classical_method/evaluation.json', 'r') as f:
    data = json.load(f)
    metrics = data.get('image_quality_metrics', {})
    custom = data.get('custom_metrics', {})
    print(f'   PSNR: {metrics.get(\"psnr_fused_vs_wide\", 0):.2f} dB')
    print(f'   SSIM: {metrics.get(\"ssim_fused_vs_wide\", 0):.4f}')
    print(f'   LPIPS: {metrics.get(\"lpips_fused_vs_wide\", 0):.4f}')
    print(f'   Detail Transfer: {custom.get(\"detail_transfer_score\", 0):.4f}')
    print(f'   Ghost Score: {custom.get(\"ghost_score\", 0):.4f}')
"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}🎉 All experiments completed successfully!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📌 Next Steps:"
echo "   1. View results: open $RESULTS_DIR/classical_method/composite.png"
echo "   2. Check metrics: cat $RESULTS_DIR/classical_method/evaluation.json"
    echo "   3. Run with your images: python chapter15/02_classical_method/align_and_fuse.py --wide YOUR_WIDE.jpg --tele YOUR_TELE.jpg"
    echo "   4. Compare methods: python chapter15/05_evaluation/compare_all_methods.py --wide W.jpg --tele T.jpg"
    echo "   5. Run DCSR: bash chapter15/03_dcsr_method/run_dcsr.sh W.jpg T.jpg results/dcsr"
    echo "   6. Run ZoomGS: bash chapter15/04_zoomgs_method/run_zoomgs.sh W.jpg T.jpg results/zoomgs"
echo ""

