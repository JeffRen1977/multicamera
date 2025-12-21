# Experimental Guide - Step-by-Step Instructions

This guide provides detailed experimental protocols for reproducing all results from the book chapter.

> **Note**: All code is organized in the `chapter15/` directory. All commands assume you're in the `MultiCamera/` root directory with the virtual environment activated.

---

## 🔬 Experiment 1: Basic Dual-Camera Fusion

**Objective**: Understand the classical fusion pipeline and obtain baseline results

### Setup

```bash
cd MultiCamera
source venv/bin/activate
```

### Steps

**1. Create test data**:
```bash
python chapter15/01_setup/create_sample_data.py --num_samples 1 --output samples
```

**Expected output**:
```
Creating 1 sample dual-camera image pairs...
Sample dataset created in: samples
```

**2. Run fusion algorithm**:
```bash
python chapter15/02_classical_method/align_and_fuse.py \
    --wide samples/sample_01/wide.jpg \
    --tele samples/sample_01/tele.jpg \
    --out results/exp1_basic \
    --visualize
```

**Expected output**:
```
Loading images...
Computing homography...
Found 252 matches, saved visualization to match_vis.jpg
Warping telephoto image...
Fusing images...
Creating digital zoom baseline...
Saved outputs to results/exp1_basic
```

**3. Evaluate results**:
```bash
python chapter15/05_evaluation/eval_multicam.py \
    --fused results/exp1_basic/fused.png \
    --wide results/exp1_basic/wide.png \
    --tele_warp results/exp1_basic/tele_warp.png \
    --digital_zoom results/exp1_basic/digital_zoom.png \
    --output results/exp1_basic/metrics.json
```

**Expected metrics**:
- PSNR: ~34 dB
- SSIM: ~0.90
- LPIPS: ~0.11
- Detail Transfer: ~0.63

### Deliverables

- [ ] Feature matching visualization (`match_vis.jpg`)
- [ ] Fused result (`results/exp1_basic/fused.png`)
- [ ] Composite comparison (`results/exp1_basic/composite.png`)
- [ ] Evaluation metrics (`results/exp1_basic/metrics.json`)

**Analysis Questions**:
1. How many feature matches were found?
2. What is the PSNR improvement over digital zoom?
3. Where does the confidence map show high/low confidence?

---

## 🔬 Experiment 2: Parameter Sensitivity Analysis

**Objective**: Understand how fusion strength (α) affects quality and artifacts

### Protocol

```bash
# Test alpha values: 0.5, 0.7, 1.0, 1.3, 1.5
for alpha in 0.5 0.7 1.0 1.3 1.5; do
    echo "Testing alpha=$alpha..."
    
    python chapter15/02_classical_method/align_and_fuse.py \
        --wide samples/sample_01/wide.jpg \
        --tele samples/sample_01/tele.jpg \
        --out results/exp2_alpha_$alpha \
        --alpha $alpha
    
    python chapter15/05_evaluation/eval_multicam.py \
        --fused results/exp2_alpha_$alpha/fused.png \
        --wide results/exp2_alpha_$alpha/wide.png \
        --tele_warp results/exp2_alpha_$alpha/tele_warp.png \
        --digital_zoom results/exp2_alpha_$alpha/digital_zoom.png \
        --output results/exp2_alpha_$alpha/metrics.json
done
```

### Data Collection

Create a comparison table:

| Alpha | PSNR | SSIM | LPIPS | Detail Transfer | Ghost Score |
|-------|------|------|-------|----------------|-------------|
| 0.5 | ? | ? | ? | ? | ? |
| 0.7 | ? | ? | ? | ? | ? |
| 1.0 | 34.18 | 0.906 | 0.112 | 0.631 | 0.010 |
| 1.3 | ? | ? | ? | ? | ? |
| 1.5 | ? | ? | ? | ? | ? |

**Extract data**:
```bash
for alpha in 0.5 0.7 1.0 1.3 1.5; do
    echo "Alpha=$alpha:"
    python -c "
import json
with open('results/exp2_alpha_$alpha/metrics.json', 'r') as f:
    d = json.load(f)
    m = d.get('image_quality_metrics', {})
    c = d.get('custom_metrics', {})
    print(f'  PSNR: {m.get(\"psnr_fused_vs_wide\", 0):.2f}')
    print(f'  Detail: {c.get(\"detail_transfer_score\", 0):.3f}')
    print(f'  Ghost: {c.get(\"ghost_score\", 0):.3f}')
"
done
```

### Analysis

**Questions to Answer**:
1. At what α does quality peak?
2. When do artifacts (ghost score) start appearing?
3. What's the optimal α for detail vs. artifact tradeoff?
4. Does PSNR always correlate with visual quality?

---

## 🔬 Experiment 3: Method Comparison

**Objective**: Compare classical, DCSR, and ZoomGS on the same data

### Protocol

**1. Run all methods on same input**:
```bash
WIDE="samples/sample_01/wide.jpg"
TELE="samples/sample_01/tele.jpg"

# Classical
python chapter15/02_classical_method/align_and_fuse.py \
    --wide $WIDE --tele $TELE --out results/exp3_classical

# DCSR (if GPU available)
bash chapter15/03_dcsr_method/run_dcsr.sh $WIDE $TELE results/exp3_dcsr

# ZoomGS (if GPU available)
bash chapter15/04_zoomgs_method/run_zoomgs.sh $WIDE $TELE results/exp3_zoomgs
```

**2. Evaluate all methods**:
```bash
for method in classical dcsr zoomgs; do
    if [ -f "results/exp3_$method/fused.png" ]; then
        python chapter15/05_evaluation/eval_multicam.py \
            --fused results/exp3_$method/fused.png \
            --wide $WIDE \
            --tele_warp results/exp3_$method/tele_warp.png \
            --digital_zoom results/exp3_$method/digital_zoom.png \
            --output results/exp3_$method/metrics.json
    fi
done
```

**3. Create comparison table**:
```bash
echo "Method Comparison Results:"
echo "=========================="
for method in classical dcsr zoomgs; do
    if [ -f "results/exp3_$method/metrics.json" ]; then
        echo ""
        echo "$method:"
        python -c "
import json
with open('results/exp3_$method/metrics.json', 'r') as f:
    d = json.load(f)
    m = d.get('image_quality_metrics', {})
    print(f'  PSNR: {m.get(\"psnr_fused_vs_wide\", 0):.2f} dB')
    print(f'  SSIM: {m.get(\"ssim_fused_vs_wide\", 0):.4f}')
    print(f'  LPIPS: {m.get(\"lpips_fused_vs_wide\", 0):.4f}')
"
    fi
done
```

### Expected Results

| Method | PSNR (dB) | SSIM | LPIPS | Processing Time |
|--------|-----------|------|-------|----------------|
| Classical | 28-32 | 0.88-0.92 | 0.12-0.20 | ~1 sec |
| DCSR | 30-35 | 0.90-0.95 | 0.08-0.15 | ~5 sec |
| ZoomGS | 32-38 | 0.92-0.96 | 0.06-0.12 | ~8 sec |

### Analysis

**Questions**:
1. Is the quality improvement worth the computational cost?
2. For which scenes does classical method suffice?
3. When is ZoomGS's complexity justified?

---

## 🔬 Experiment 4: Real-World Image Testing

**Objective**: Test on real dual-camera smartphone photos

### Capturing Images

**Requirements**:
- Smartphone with dual cameras (wide + tele)
- Tripod or stable surface
- Good lighting

**Capture Protocol**:
1. Mount phone on tripod
2. Frame subject at 3-5 meters distance
3. Capture wide angle photo
4. **Without moving camera**, switch to telephoto
5. Capture telephoto photo (within 1 second)
6. Transfer both images to computer

**Metadata to Record**:
- Camera model
- Focal lengths (wide and tele)
- Exposure settings (ISO, shutter, aperture)
- Capture timestamp
- Scene description

### Processing

```bash
# Transfer photos to samples/real/
mkdir -p samples/real
cp /path/to/wide.jpg samples/real/
cp /path/to/tele.jpg samples/real/

# Run fusion
python chapter15/02_classical_method/align_and_fuse.py \
    --wide samples/real/wide.jpg \
    --tele samples/real/tele.jpg \
    --out results/exp4_real \
    --visualize

# Evaluate
python chapter15/05_evaluation/eval_multicam.py \
    --fused results/exp4_real/fused.png \
    --wide results/exp4_real/wide.png \
    --tele_warp results/exp4_real/tele_warp.png \
    --digital_zoom results/exp4_real/digital_zoom.png \
    --output results/exp4_real/metrics.json
```

### Analysis

**Examine**:
1. `match_vis.jpg`: Are features well distributed?
2. `confidence_mask.png`: Where is fusion most confident?
3. `composite.png`: Visual quality comparison
4. `metrics.json`: Quantitative performance

**Common Issues with Real Photos**:
- Motion between captures → Low alignment quality
- Exposure mismatch → Artifacts in fusion
- Strong parallax (close subjects) → Ghosting
- Low texture (sky) → Few features found

---

## 🔬 Experiment 5: Failure Case Analysis

**Objective**: Understand when and why methods fail

### Test Cases

**Case 1: Strong Parallax (Near Field)**
```bash
# Create sample with close subject
# Or use real photo with subject <1 meter

python chapter15/02_classical_method/align_and_fuse.py \
    --wide samples/close_subject/wide.jpg \
    --tele samples/close_subject/tele.jpg \
    --out results/exp5_parallax
```

**Expected**: High ghost score, poor alignment quality

**Case 2: Low Texture (Uniform Regions)**
```bash
# Test on image with sky, blank walls
# Expected: "Not enough matches" error
```

**Case 3: Motion Blur**
```bash
# Test with camera shake or moving subject
# Expected: Poor alignment, artifacts
```

**Case 4: Exposure Mismatch**
```bash
# Test with different exposures
# Expected: Color artifacts, low confidence
```

### Recording Failures

Create failure mode table:

| Failure Type | Symptom | Metric Indicator | Solution |
|--------------|---------|------------------|----------|
| Strong parallax | Ghosting | Ghost score >0.3 | Use DCSR/ZoomGS |
| Low texture | Few matches | Error or align <0.3 | Add texture |
| Motion | Blur/double image | Align <0.4 | Re-capture |
| Exposure | Color mismatch | Confidence low | Color correction |

---

## 📊 Experiment 6: Quantitative Benchmarking

**Objective**: Build comprehensive performance database

### Benchmark Protocol

```bash
# Create benchmark suite
for sample in {01..03}; do
    for alpha in 0.7 1.0 1.3; do
        echo "Benchmark: sample_$sample, alpha=$alpha"
        
        python chapter15/02_classical_method/align_and_fuse.py \
            --wide samples/sample_$sample/wide.jpg \
            --tele samples/sample_$sample/tele.jpg \
            --out results/benchmark/s${sample}_a${alpha} \
            --alpha $alpha
        
        python chapter15/05_evaluation/eval_multicam.py \
            --fused results/benchmark/s${sample}_a${alpha}/fused.png \
            --wide results/benchmark/s${sample}_a${alpha}/wide.png \
            --tele_warp results/benchmark/s${sample}_a${alpha}/tele_warp.png \
            --digital_zoom results/benchmark/s${sample}_a${alpha}/digital_zoom.png \
            --output results/benchmark/s${sample}_a${alpha}/metrics.json
    done
done
```

### Aggregate Results

```bash
# Collect all metrics into CSV
echo "Sample,Alpha,PSNR,SSIM,LPIPS,Detail,Ghost,Align" > benchmark_results.csv

for sample in {01..03}; do
    for alpha in 0.7 1.0 1.3; do
        python -c "
import json
with open('results/benchmark/s${sample}_a${alpha}/metrics.json', 'r') as f:
    d = json.load(f)
    m = d.get('image_quality_metrics', {})
    c = d.get('custom_metrics', {})
    print(f'${sample},${alpha},' +
          f'{m.get(\"psnr_fused_vs_wide\", 0):.2f},' +
          f'{m.get(\"ssim_fused_vs_wide\", 0):.4f},' +
          f'{m.get(\"lpips_fused_vs_wide\", 0):.4f},' +
          f'{c.get(\"detail_transfer_score\", 0):.4f},' +
          f'{c.get(\"ghost_score\", 0):.4f},' +
          f'{c.get(\"alignment_quality\", 0):.4f}')
" >> benchmark_results.csv
    done
done

cat benchmark_results.csv
```

### Analysis

Import `benchmark_results.csv` into spreadsheet software for:
- Statistical analysis (mean, std, min, max)
- Parameter sensitivity plots
- Method comparison charts

---

## 🎯 Experiment 7: All-Method Comparison

**Objective**: Compare classical, DCSR, and ZoomGS on same input

### Full Comparison Pipeline

```bash
source venv/bin/activate

# Use automated comparison
python chapter15/compare_all_methods.py \
    --wide samples/sample_01/wide.jpg \
    --tele samples/sample_01/tele.jpg \
    --output results/exp7_comparison
```

**OR manual comparison**:

```bash
# Run each method
python chapter15/02_classical_method/align_and_fuse.py \
    --wide samples/sample_01/wide.jpg \
    --tele samples/sample_01/tele.jpg \
    --out results/exp7_classical

bash chapter15/03_dcsr_method/run_dcsr.sh \
    samples/sample_01/wide.jpg \
    samples/sample_01/tele.jpg \
    results/exp7_dcsr

bash chapter15/04_zoomgs_method/run_zoomgs.sh \
    samples/sample_01/wide.jpg \
    samples/sample_01/tele.jpg \
    results/exp7_zoomgs

# Evaluate all
for method in classical dcsr zoomgs; do
    python chapter15/05_evaluation/eval_multicam.py \
        --fused results/exp7_$method/fused.png \
        --wide samples/sample_01/wide.jpg \
        --tele_warp results/exp7_$method/tele_warp.png \
        --digital_zoom results/exp7_$method/digital_zoom.png \
        --output results/exp7_$method/metrics.json
done
```

### Results Table

| Metric | Classical | DCSR | ZoomGS | Best |
|--------|-----------|------|--------|------|
| PSNR | ? | ? | ? | ? |
| SSIM | ? | ? | ? | ? |
| LPIPS | ? | ? | ? | ? |
| Detail Transfer | ? | ? | ? | ? |
| Ghost Score | ? | ? | ? | ? |
| Processing Time | ? | ? | ? | ? |

**Fill from**:
```bash
cat results/exp7_*/metrics.json
```

---

## 🎓 Reproducibility Checklist

Use this checklist to ensure experiments are reproducible:

### Environment
- [ ] Python version recorded: `python --version`
- [ ] Package versions: `pip freeze > requirements_frozen.txt`
- [ ] Hardware specs documented (CPU, GPU, RAM)
- [ ] OS version recorded: `uname -a`

### Data
- [ ] Sample data parameters recorded (num_samples, seed)
- [ ] Input image specifications (resolution, format)
- [ ] Metadata preserved (EXIF, camera info)

### Code
- [ ] Git commit hash: `git rev-parse HEAD`
- [ ] No uncommitted changes: `git status`
- [ ] Parameters explicitly specified (no defaults assumed)

### Results
- [ ] All outputs saved with timestamps
- [ ] Metrics exported to JSON and CSV
- [ ] Visualizations saved with labels
- [ ] Log files captured

### Documentation
- [ ] Experimental protocol written
- [ ] Parameters documented
- [ ] Observations recorded
- [ ] Analysis notes included

---

## 📝 Lab Notebook Template

Use this template for recording experiments:

```markdown
## Experiment: [Title]
Date: YYYY-MM-DD
Researcher: [Name]

### Objective
[What you're testing]

### Hypothesis
[Expected outcome]

### Setup
- Environment: [venv info]
- Hardware: [specs]
- Input data: [description]

### Protocol
1. [Step 1]
2. [Step 2]
...

### Parameters
- alpha: [value]
- sigma: [value]
- threshold: [value]

### Results
- PSNR: [value]
- SSIM: [value]
- Processing time: [value]

### Observations
[What you noticed]

### Analysis
[Interpretation]

### Conclusions
[What you learned]

### Next Steps
[Follow-up experiments]
```

---

## ⏱️ Time Estimates

| Experiment | Time Required | Difficulty |
|------------|---------------|------------|
| Exp 1: Basic Fusion | 5 minutes | Easy |
| Exp 2: Parameter Sweep | 15 minutes | Easy |
| Exp 3: Method Comparison | 30 minutes | Medium |
| Exp 4: Real Photos | 20 minutes | Medium |
| Exp 5: Failure Analysis | 15 minutes | Medium |
| Exp 6: Benchmarking | 45 minutes | Hard |
| Exp 7: Full Comparison | 60 minutes | Hard |

**Total for all experiments**: ~3 hours

---

## 🎯 Success Criteria

**Minimum Success** (Experiment 1):
- ✅ Code runs without errors
- ✅ PSNR > 30 dB
- ✅ Ghost score < 0.1
- ✅ Visual results look better than digital zoom

**Full Success** (All Experiments):
- ✅ All experiments completed
- ✅ Results match expected ranges
- ✅ Method comparison shows expected hierarchy
- ✅ Parameter sensitivity understood
- ✅ Real photos processed successfully

---

## 📞 Support

**If experiments fail**:
1. Check `USAGE.md` for basic troubleshooting
2. Verify virtual environment setup
3. Test with provided samples first
4. Review error messages carefully
5. Try `run_quick_test.sh` as sanity check

**Report issues**:
- Include error messages
- Specify which experiment failed
- Provide system info (`python --version`, `pip list`)
- Attach log files if available

---

*Good luck with your experiments!*

