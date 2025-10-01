# Quick Usage Guide - Multi-Camera Fusion

This guide provides the essential commands to run all experiments.

---

## 🚀 Quick Start (3 Commands)

```bash
# 1. Setup (one-time)
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# 2. Run quick test
./run_quick_test.sh

# 3. View results
open results/quick_test/composite.png
```

---

## 📋 Complete Workflow Scripts

### Option 1: Run Everything (Automated)

```bash
# Activate environment
source venv/bin/activate

# Run complete pipeline
./run_all.sh
```

**What it does**:
1. ✅ Creates 3 sample dual-camera pairs
2. ✅ Runs classical fusion method
3. ✅ Evaluates with all metrics
4. ✅ Generates comparison visualizations
5. ✅ Prints summary with key results

**Time**: ~5-10 seconds  
**Output**: `results/classical_method/`

---

### Option 2: Step-by-Step (Manual)

#### Step 1: Setup Environment

```bash
# Create virtual environment (one-time)
python3 -m venv venv

# Activate environment (every session)
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies (one-time)
pip install --upgrade pip
pip install -r requirements.txt

# Verify installation
python -c "import cv2, numpy, torch, lpips; print('✅ All dependencies ready!')"
```

#### Step 2: Create Sample Data

```bash
# Generate synthetic dual-camera image pairs
python multicam/create_sample_data.py \
    --num_samples 3 \
    --output samples

# Output: samples/sample_01/, sample_02/, sample_03/
# Each contains: wide.jpg, tele.jpg, scene.jpg, composite.jpg
```

#### Step 3: Run Classical Fusion

```bash
# Basic usage
python multicam/align_and_fuse.py \
    --wide samples/sample_01/wide.jpg \
    --tele samples/sample_01/tele.jpg \
    --out results/experiment_01

# With visualization and custom parameters
python multicam/align_and_fuse.py \
    --wide samples/sample_01/wide.jpg \
    --tele samples/sample_01/tele.jpg \
    --out results/experiment_01 \
    --visualize \
    --alpha 1.0
```

**Parameters**:
- `--wide`: Path to wide-angle image
- `--tele`: Path to telephoto image
- `--out`: Output directory
- `--visualize`: Save feature matching visualization
- `--alpha`: Fusion strength (default: 1.0, range: 0.5-2.0)

**Outputs**:
```
results/experiment_01/
├── fused.png              # Main fusion result
├── digital_zoom.png       # Baseline comparison
├── wide.png              # Processed wide input
├── tele_warp.png         # Aligned telephoto
├── confidence_mask.png    # Fusion confidence map
└── composite.png          # 4-way comparison
```

#### Step 4: Evaluate Results

```bash
python multicam/eval_multicam.py \
    --fused results/experiment_01/fused.png \
    --wide results/experiment_01/wide.png \
    --tele_warp results/experiment_01/tele_warp.png \
    --digital_zoom results/experiment_01/digital_zoom.png \
    --confidence_mask results/experiment_01/confidence_mask.png \
    --output results/experiment_01/evaluation.json \
    --csv results/experiment_01/metrics.csv
```

**Outputs**:
- `evaluation.json`: Complete metrics in JSON format
- `metrics.csv`: Spreadsheet-friendly CSV format

**Metrics Computed**:
- PSNR, SSIM, LPIPS (standard)
- Detail Transfer Score, Ghost Score, Alignment Quality (custom)

#### Step 5: View Results

```bash
# View composite image
open results/experiment_01/composite.png  # macOS
# OR
xdg-open results/experiment_01/composite.png  # Linux
# OR
start results/experiment_01/composite.png  # Windows

# Check metrics
cat results/experiment_01/evaluation.json

# CSV for spreadsheet
open results/experiment_01/metrics.csv
```

---

## 🔄 Running Multiple Methods

### Method 1: Teaching Method (Classical)

```bash
source venv/bin/activate

python multicam/align_and_fuse.py \
    --wide samples/sample_01/wide.jpg \
    --tele samples/sample_01/tele.jpg \
    --out results/teaching \
    --visualize
```

**Time**: ~1 second  
**Quality**: PSNR 28-32 dB  
**GPU**: Not required

---

### Method 2: DCSR (Deep Learning)

```bash
source venv/bin/activate

bash multicam/run_dcsr.sh \
    samples/sample_01/wide.jpg \
    samples/sample_01/tele.jpg \
    results/dcsr
```

**What it does**:
1. Clones DCSR repository to `thirdparty/DCSR`
2. Creates separate virtual environment for DCSR
3. Downloads pre-trained model (~200MB)
4. Runs inference
5. Saves results to `results/dcsr/`

**Time**: ~5 seconds (GPU) / ~30 seconds (CPU)  
**Quality**: PSNR 30-35 dB  
**GPU**: Recommended

**Note**: First run takes longer (downloads model and dependencies)

---

### Method 3: ZoomGS (3D Gaussian Splatting)

```bash
source venv/bin/activate

bash multicam/run_zoomgs.sh \
    samples/sample_01/wide.jpg \
    samples/sample_01/tele.jpg \
    results/zoomgs
```

**What it does**:
1. Clones ZoomGS repository to `thirdparty/ZoomGS`
2. Builds CUDA extensions for Gaussian splatting
3. Downloads pre-trained models
4. Runs full pipeline (SfM + optimization + rendering)
5. Saves results to `results/zoomgs/`

**Time**: ~8 seconds (high-end GPU)  
**Quality**: PSNR 32-38 dB  
**GPU**: Required (CUDA support)

**Requirements**:
- NVIDIA GPU with CUDA
- 4GB+ GPU memory
- CUDA 11.0+

---

### Compare All Three Methods

```bash
source venv/bin/activate

python multicam/compare_all_methods.py \
    --wide samples/sample_01/wide.jpg \
    --tele samples/sample_01/tele.jpg \
    --output results/comparison
```

**What it does**:
1. Runs all three methods sequentially
2. Evaluates each with same metrics
3. Creates comparison report
4. Generates side-by-side visualizations

**Output**:
```
results/comparison/
├── teaching_output/
├── dcsr_output/
├── zoomgs_output/
├── comparison_report.json
└── visual_summary.txt
```

**Time**: ~15 seconds (if all methods run successfully)

---

## 🧪 Testing Your Own Images

### Using Real Dual-Camera Photos

```bash
source venv/bin/activate

# Replace with your image paths
WIDE_IMAGE="/path/to/your/wide_photo.jpg"
TELE_IMAGE="/path/to/your/tele_photo.jpg"

# Run fusion
python multicam/align_and_fuse.py \
    --wide "$WIDE_IMAGE" \
    --tele "$TELE_IMAGE" \
    --out results/my_photos \
    --visualize \
    --alpha 1.0
```

**Tips for Best Results**:
1. ✅ Capture both images within 1 second (minimize motion)
2. ✅ Keep camera steady (use tripod or rest on surface)
3. ✅ Ensure good lighting (avoid extreme shadows)
4. ✅ Subject distance: 2-10 meters (moderate parallax)
5. ✅ Similar exposure (manual mode if possible)
6. ✅ Avoid moving subjects

---

## 📊 Batch Processing Multiple Samples

```bash
source venv/bin/activate

# Process all samples
for i in {01..03}; do
    echo "Processing sample_$i..."
    
    python multicam/align_and_fuse.py \
        --wide samples/sample_$i/wide.jpg \
        --tele samples/sample_$i/tele.jpg \
        --out results/batch/sample_$i \
        --alpha 1.0
    
    echo "Sample $i completed!"
done

echo "Batch processing completed!"
```

---

## 🎯 Parameter Tuning Examples

### Experiment with Fusion Strength

```bash
source venv/bin/activate

# Test different alpha values
for alpha in 0.5 0.7 1.0 1.3 1.5; do
    python multicam/align_and_fuse.py \
        --wide samples/sample_01/wide.jpg \
        --tele samples/sample_01/tele.jpg \
        --out results/alpha_$alpha \
        --alpha $alpha
done

# Compare results visually
open results/alpha_*/composite.png
```

**Expected Effects**:
- α=0.5: Subtle enhancement, very safe
- α=0.7: Conservative, minimal artifacts
- α=1.0: Balanced (default)
- α=1.3: Aggressive, more detail
- α=1.5: Very aggressive, may show artifacts

---

## 🐛 Troubleshooting

### Script Fails: "command not found: python"

```bash
# Use python3 instead
python3 -m venv venv
source venv/bin/activate
python3 multicam/align_and_fuse.py ...
```

### Script Fails: "No module named cv2"

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Script Fails: "Not enough matches"

```
RuntimeError: Not enough matches: 5
```

**Solution**: Image pair has insufficient features
```bash
# Try different sample
python multicam/align_and_fuse.py \
    --wide samples/sample_02/wide.jpg \
    --tele samples/sample_02/tele.jpg \
    --out results/test
```

### DCSR/ZoomGS Fails: "Repository not found"

**Solution**: Check internet connection and retry
```bash
# DCSR will clone from: https://github.com/Tengfei-Wang/DCSR.git
# ZoomGS will clone from: https://github.com/ZcsrenlongZ/ZoomGS.git
```

### GPU Out of Memory

**Solution**: Reduce image size or use CPU
```bash
# Resize images before processing
mogrify -resize 50% samples/sample_01/*.jpg

# Or process with CPU (slower)
CUDA_VISIBLE_DEVICES="" python multicam/eval_multicam.py ...
```

---

## 📁 Directory Structure After Running

```
MultiCamera/
├── venv/                          # Virtual environment
├── samples/                       # Generated test data
│   ├── sample_01/
│   │   ├── wide.jpg              # Wide camera (800×1200)
│   │   ├── tele.jpg              # Telephoto (800×1200)
│   │   ├── scene.jpg             # Original scene
│   │   └── composite.jpg         # Input comparison
│   ├── sample_02/
│   └── sample_03/
├── results/                       # All experimental results
│   ├── classical_method/         # From run_all.sh
│   │   ├── fused.png
│   │   ├── composite.png
│   │   ├── evaluation.json
│   │   └── evaluation.csv
│   ├── quick_test/               # From run_quick_test.sh
│   ├── dcsr/                     # From run_dcsr.sh
│   ├── zoomgs/                   # From run_zoomgs.sh
│   └── comparison/               # From compare_all_methods.py
├── thirdparty/                    # External repos (auto-created)
│   ├── DCSR/
│   └── ZoomGS/
└── match_vis.jpg                 # Feature matching visualization
```

---

## ⚡ Performance Expectations

| Operation | Time | Hardware |
|-----------|------|----------|
| Create samples (3) | ~3 sec | CPU |
| Classical fusion | ~1 sec | CPU |
| Evaluation | ~2 sec | CPU (LPIPS on CPU) |
| DCSR fusion | ~5 sec | GPU (RTX 3090) |
| ZoomGS fusion | ~8 sec | GPU (RTX 3090) |
| Compare all methods | ~15 sec | Mixed CPU/GPU |

**Total for complete workflow**: ~10 seconds (classical only) or ~25 seconds (all methods)

---

## 🎓 Learning Exercises

### Exercise 1: Understand the Pipeline

```bash
# Run with visualization
python multicam/align_and_fuse.py \
    --wide samples/sample_01/wide.jpg \
    --tele samples/sample_01/tele.jpg \
    --out results/exercise1 \
    --visualize

# Examine outputs:
# 1. match_vis.jpg - See how features are matched
# 2. confidence_mask.png - See where fusion trusts tele camera
# 3. composite.png - Compare all results side-by-side
```

### Exercise 2: Parameter Sensitivity

```bash
# Test alpha values: 0.5, 1.0, 1.5
for alpha in 0.5 1.0 1.5; do
    python multicam/align_and_fuse.py \
        --wide samples/sample_01/wide.jpg \
        --tele samples/sample_01/tele.jpg \
        --out results/alpha_test_$alpha \
        --alpha $alpha
done

# Compare: Which alpha gives best quality/artifact tradeoff?
```

### Exercise 3: Method Comparison

```bash
# Run all three methods
./run_all.sh                                    # Classical
bash multicam/run_dcsr.sh W.jpg T.jpg res/dcsr # DCSR
bash multicam/run_zoomgs.sh W.jpg T.jpg res/zg  # ZoomGS

# Compare metrics
cat results/*/evaluation.json

# Question: When does classical method match DCSR?
```

---

## 📞 Getting Help

**If scripts don't work**:
1. Check virtual environment is activated: `echo $VIRTUAL_ENV`
2. Verify Python version: `python --version` (should be 3.9+)
3. Check dependencies: `pip list | grep opencv`
4. Try quick test first: `./run_quick_test.sh`

**Common Commands**:
```bash
# Reactivate environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Clean and restart
rm -rf results/* samples/*
./run_quick_test.sh
```

---

## 🎯 Summary

**Quickest way to see results**:
```bash
source venv/bin/activate && ./run_quick_test.sh
```

**Best way to learn**:
```bash
source venv/bin/activate && ./run_all.sh
```

**For your own images**:
```bash
source venv/bin/activate
python multicam/align_and_fuse.py --wide YOUR_WIDE.jpg --tele YOUR_TELE.jpg --out results/mine
```

**To compare methods**:
```bash
source venv/bin/activate
python multicam/compare_all_methods.py --wide W.jpg --tele T.jpg --output results/comp
```

---

*All commands assume you're in the MultiCamera/ directory*

