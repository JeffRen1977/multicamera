# Scripts Reference Guide

Complete reference for all runnable scripts in this project.

---

## 📜 Available Scripts

### 🚀 Main Execution Scripts

| Script | Purpose | Time | Prerequisites |
|--------|---------|------|---------------|
| `run_quick_test.sh` | Minimal working demo | 30 sec | venv setup |
| `run_all.sh` | Complete pipeline | 2 min | venv setup |
| `demo.py` | Python-based demo | 2 min | venv setup |

### 🔬 Method-Specific Scripts

| Script | Method | Time | GPU Required |
|--------|--------|------|--------------|
| `multicam/align_and_fuse.py` | Classical (teaching) | 1 sec | No |
| `multicam/run_dcsr.sh` | DCSR (deep learning) | 5 sec | Recommended |
| `multicam/run_zoomgs.sh` | ZoomGS (3D gaussian) | 8 sec | Yes |

### 🛠️ Utility Scripts

| Script | Purpose |
|--------|---------|
| `multicam/create_sample_data.py` | Generate synthetic test data |
| `multicam/eval_multicam.py` | Evaluate fusion quality |
| `multicam/compare_all_methods.py` | Compare all three methods |

---

## 📋 Script Details

### `run_quick_test.sh`

**Purpose**: Fastest way to see results

**Usage**:
```bash
./run_quick_test.sh
```

**What it does**:
1. Activates virtual environment
2. Creates 1 sample pair (if not exists)
3. Runs classical fusion
4. Shows where results are saved

**Output**: `results/quick_test/`

**Time**: ~30 seconds

---

### `run_all.sh`

**Purpose**: Complete experimental pipeline

**Usage**:
```bash
source venv/bin/activate
./run_all.sh
```

**What it does**:
1. ✅ Generates 3 sample pairs
2. ✅ Runs classical fusion
3. ✅ Evaluates with all metrics
4. ✅ Prints summary with key results

**Output**: `results/classical_method/`

**Time**: ~2 minutes

**Displays**:
- PSNR, SSIM, LPIPS
- Detail Transfer Score
- Ghost Score
- Processing time

---

### `demo.py`

**Purpose**: Python-based comprehensive demo

**Usage**:
```bash
python demo.py
```

**What it does**:
1. Creates 3 sample pairs
2. Runs classical fusion
3. Evaluates results
4. Shows detailed progress
5. Parses and displays metrics

**Output**: `results/demo_teaching/`

**Time**: ~2 minutes

---

### `multicam/align_and_fuse.py`

**Purpose**: Main classical fusion algorithm

**Usage**:
```bash
python multicam/align_and_fuse.py \
    --wide WIDE.jpg \
    --tele TELE.jpg \
    --out OUTPUT_DIR \
    [--visualize] \
    [--alpha 1.0]
```

**Parameters**:
- `--wide`: Wide-angle input image (required)
- `--tele`: Telephoto input image (required)
- `--out`: Output directory (required)
- `--visualize`: Save feature matching visualization (optional)
- `--alpha`: Fusion strength, 0.5-2.0 (optional, default: 1.0)

**Outputs**:
```
OUTPUT_DIR/
├── fused.png
├── digital_zoom.png
├── wide.png
├── tele_warp.png
├── confidence_mask.png
└── composite.png
```

**Example**:
```bash
python multicam/align_and_fuse.py \
    --wide samples/sample_01/wide.jpg \
    --tele samples/sample_01/tele.jpg \
    --out results/test1 \
    --visualize \
    --alpha 1.2
```

---

### `multicam/eval_multicam.py`

**Purpose**: Comprehensive quality evaluation

**Usage**:
```bash
python multicam/eval_multicam.py \
    --fused FUSED.png \
    --wide WIDE.png \
    --tele_warp TELE_WARPED.png \
    --digital_zoom DIGITAL_ZOOM.png \
    [--confidence_mask MASK.png] \
    [--gt GROUND_TRUTH.png] \
    --output REPORT.json \
    [--csv METRICS.csv]
```

**Parameters**:
- `--fused`: Fused result image (required)
- `--wide`: Wide camera image (required)
- `--tele_warp`: Warped telephoto image (required)
- `--digital_zoom`: Digital zoom baseline (required)
- `--confidence_mask`: Confidence map (optional)
- `--gt`: Ground truth high-res image (optional)
- `--output`: JSON report path (required)
- `--csv`: CSV export path (optional)

**Computed Metrics**:
- PSNR, SSIM, LPIPS (standard)
- Detail Transfer Score
- Ghost Score
- Alignment Quality

**Example**:
```bash
python multicam/eval_multicam.py \
    --fused results/test1/fused.png \
    --wide results/test1/wide.png \
    --tele_warp results/test1/tele_warp.png \
    --digital_zoom results/test1/digital_zoom.png \
    --confidence_mask results/test1/confidence_mask.png \
    --output results/test1/eval.json \
    --csv results/test1/eval.csv
```

---

### `multicam/create_sample_data.py`

**Purpose**: Generate synthetic dual-camera test data

**Usage**:
```bash
python multicam/create_sample_data.py \
    [--num_samples 5] \
    [--output samples] \
    [--realistic]
```

**Parameters**:
- `--num_samples`: Number of sample pairs to generate (default: 5)
- `--output`: Output directory (default: samples)
- `--realistic`: Use real image instead of synthetic (optional)

**Output**:
```
samples/
├── sample_01/
│   ├── wide.jpg      # 800×1200 wide-angle simulation
│   ├── tele.jpg      # 800×1200 telephoto simulation
│   ├── scene.jpg     # Original synthetic scene
│   └── composite.jpg # Side-by-side input comparison
├── sample_02/
└── ...
```

**Examples**:
```bash
# Create 3 synthetic samples
python multicam/create_sample_data.py --num_samples 3

# Create realistic sample
python multicam/create_sample_data.py --realistic
```

---

### `multicam/run_dcsr.sh`

**Purpose**: Run DCSR (Dual-Camera Super-Resolution)

**Usage**:
```bash
bash multicam/run_dcsr.sh WIDE.jpg TELE.jpg OUTPUT_DIR
```

**Parameters**:
- `$1`: Wide-angle image path
- `$2`: Telephoto image path
- `$3`: Output directory

**What it does**:
1. Clones https://github.com/Tengfei-Wang/DCSR.git
2. Creates isolated venv: `dcsr_venv`
3. Downloads pretrained model (~200MB)
4. Runs DCSR inference
5. Saves results

**Example**:
```bash
bash multicam/run_dcsr.sh \
    samples/sample_01/wide.jpg \
    samples/sample_01/tele.jpg \
    results/dcsr_output
```

**First run**: ~5 minutes (downloads repo + model)  
**Subsequent runs**: ~5 seconds

**Requirements**:
- Internet connection (first run)
- GPU recommended (works on CPU but slower)
- ~2GB disk space

---

### `multicam/run_zoomgs.sh`

**Purpose**: Run ZoomGS (Dual-Camera Smooth Zoom)

**Usage**:
```bash
bash multicam/run_zoomgs.sh WIDE.jpg TELE.jpg OUTPUT_DIR
```

**Parameters**:
- `$1`: Wide-angle image path
- `$2`: Telephoto image path
- `$3`: Output directory

**What it does**:
1. Clones https://github.com/ZcsrenlongZ/ZoomGS.git
2. Creates isolated venv: `zoomgs_venv`
3. Builds CUDA extensions
4. Downloads pretrained models
5. Runs ZoomGS pipeline
6. Saves results

**Example**:
```bash
bash multicam/run_zoomgs.sh \
    samples/sample_01/wide.jpg \
    samples/sample_01/tele.jpg \
    results/zoomgs_output
```

**First run**: ~10 minutes (downloads repo + builds CUDA)  
**Subsequent runs**: ~8 seconds

**Requirements**:
- NVIDIA GPU with CUDA support
- 4GB+ GPU memory
- ~5GB disk space
- CUDA 11.0+

---

### `multicam/compare_all_methods.py`

**Purpose**: Run and compare all three methods

**Usage**:
```bash
python multicam/compare_all_methods.py \
    --wide WIDE.jpg \
    --tele TELE.jpg \
    --output COMPARISON_DIR \
    [--gt GROUND_TRUTH.jpg]
```

**Parameters**:
- `--wide`: Wide-angle image
- `--tele`: Telephoto image
- `--output`: Output directory for comparison
- `--gt`: Optional ground truth for reference

**What it does**:
1. Runs classical method
2. Attempts to run DCSR (if available)
3. Attempts to run ZoomGS (if available)
4. Evaluates all results
5. Creates comparison report

**Output**:
```
COMPARISON_DIR/
├── teaching_output/
├── dcsr_output/
├── zoomgs_output/
├── comparison_report.json
└── visual_summary.txt
```

**Example**:
```bash
python multicam/compare_all_methods.py \
    --wide samples/sample_01/wide.jpg \
    --tele samples/sample_01/tele.jpg \
    --output results/full_comparison
```

---

## 🎯 Common Workflows

### Workflow 1: Quick Test

```bash
./run_quick_test.sh
open results/quick_test/composite.png
```

### Workflow 2: Full Pipeline

```bash
source venv/bin/activate
./run_all.sh
cat results/classical_method/evaluation.json
```

### Workflow 3: Your Own Images

```bash
source venv/bin/activate

python multicam/align_and_fuse.py \
    --wide YOUR_WIDE.jpg \
    --tele YOUR_TELE.jpg \
    --out results/mine \
    --visualize

python multicam/eval_multicam.py \
    --fused results/mine/fused.png \
    --wide results/mine/wide.png \
    --tele_warp results/mine/tele_warp.png \
    --digital_zoom results/mine/digital_zoom.png \
    --output results/mine/metrics.json
```

### Workflow 4: Compare Methods

```bash
source venv/bin/activate

python multicam/compare_all_methods.py \
    --wide samples/sample_01/wide.jpg \
    --tele samples/sample_01/tele.jpg \
    --output results/comparison

cat results/comparison/comparison_report.json
```

### Workflow 5: Parameter Tuning

```bash
source venv/bin/activate

# Test different alpha values
for alpha in 0.5 0.7 1.0 1.3 1.5; do
    python multicam/align_and_fuse.py \
        --wide samples/sample_01/wide.jpg \
        --tele samples/sample_01/tele.jpg \
        --out results/tune_alpha_$alpha \
        --alpha $alpha
done

# Compare results
open results/tune_alpha_*/composite.png
```

---

## ⚙️ Script Execution Order

**For learning (sequential)**:
```
1. run_quick_test.sh           (understand basics)
2. align_and_fuse.py          (manual control)
3. eval_multicam.py           (understand metrics)
4. run_all.sh                 (complete pipeline)
5. compare_all_methods.py     (method comparison)
6. run_dcsr.sh / run_zoomgs.sh (SOTA methods)
```

**For production (direct)**:
```
1. align_and_fuse.py          (if classical sufficient)
   OR
   run_dcsr.sh                (if need better quality)
   OR
   run_zoomgs.sh              (if need best quality)

2. eval_multicam.py           (quality assurance)
```

---

## 🐞 Debugging Commands

```bash
# Check environment
which python
python --version
pip list | grep opencv

# Test imports
python -c "import cv2, numpy, torch, lpips; print('OK')"

# Check file paths
ls -lh samples/sample_01/
ls -lh multicam/

# Clean start
rm -rf results/* samples/*
./run_quick_test.sh
```

---

## 📈 Performance Summary

| Script | Input | Output | Time | GPU |
|--------|-------|--------|------|-----|
| `create_sample_data.py` | None | 3 samples | 3s | No |
| `align_and_fuse.py` | 2 images | Fusion + baseline | 1s | No |
| `eval_multicam.py` | 4 images | Metrics JSON/CSV | 2s | Optional |
| `run_dcsr.sh` | 2 images | DCSR fusion | 5s | Yes |
| `run_zoomgs.sh` | 2 images | ZoomGS fusion | 8s | Yes |
| `compare_all_methods.py` | 2 images | 3-method comparison | 15s | Optional |
| `run_all.sh` | None | Complete pipeline | 120s | No |
| `run_quick_test.sh` | None | Quick test | 30s | No |

---

**Pro Tip**: Start with `run_quick_test.sh`, then progress to more complex scripts as needed!
