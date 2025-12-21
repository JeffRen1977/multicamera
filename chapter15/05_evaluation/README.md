# Section 5: Evaluation and Comparison

This section covers comprehensive evaluation of all fusion methods using standard and custom metrics.

## 📋 What This Section Covers

- Standard metrics (PSNR, SSIM, LPIPS)
- Custom multi-camera metrics
- Method comparison
- Quantitative analysis
- Visual quality assessment

## 🚀 Quick Start

### Evaluate Single Method

```bash
# From chapter15/ directory
cd 05_evaluation

# Evaluate classical method
python eval_multicam.py \
    --fused ../results/classical/fused.png \
    --wide ../results/classical/wide.png \
    --tele_warp ../results/classical/tele_warp.png \
    --digital_zoom ../results/classical/digital_zoom.png \
    --output ../results/classical/metrics.json \
    --csv ../results/classical/metrics.csv
```

### Compare All Methods

```bash
python compare_all_methods.py \
    --wide ../data/sample_01/wide.jpg \
    --tele ../data/sample_01/tele.jpg \
    --output ../results/comparison
```

## 📊 Evaluation Metrics

### Standard Metrics

**PSNR (Peak Signal-to-Noise Ratio)**
- Measures: Pixel-level reconstruction quality
- Range: 20-40 dB (higher is better)
- Excellent: >30 dB
- Formula: `PSNR = 10 × log₁₀(MAX² / MSE)`

**SSIM (Structural Similarity Index)**
- Measures: Structural similarity
- Range: 0-1 (higher is better)
- Excellent: >0.9
- Accounts for: Luminance, contrast, structure

**LPIPS (Learned Perceptual Image Patch Similarity)**
- Measures: Perceptual similarity using deep features
- Range: 0-1 (lower is better)
- Excellent: <0.1
- Better correlates with human perception

### Custom Multi-Camera Metrics

**Detail Transfer Score**
- Measures: How much telephoto detail is preserved
- Range: 0-1 (higher is better)
- Excellent: >0.8
- Formula: `Energy(fused_high_freq) / Energy(tele_high_freq)`

**Ghost Score**
- Measures: Artifacts from incorrect detail transfer
- Range: 0-1 (lower is better)
- Excellent: <0.1
- Detects: Ghosting, double images, misalignment artifacts

**Alignment Quality**
- Measures: Registration accuracy
- Range: 0-1 (higher is better)
- Excellent: >0.8
- Uses: Optical flow consistency

## 📈 Expected Results

### Classical Method
- PSNR: 28-34 dB
- SSIM: 0.88-0.92
- LPIPS: 0.12-0.20
- Detail Transfer: 0.60-0.80
- Ghost Score: 0.08-0.15

### DCSR Method
- PSNR: 30-35 dB
- SSIM: 0.90-0.95
- LPIPS: 0.08-0.15
- Detail Transfer: 0.70-0.90
- Ghost Score: 0.05-0.12

### ZoomGS Method
- PSNR: 32-38 dB
- SSIM: 0.92-0.96
- LPIPS: 0.06-0.12
- Detail Transfer: 0.80-0.95
- Ghost Score: 0.03-0.08

## 🔍 Understanding the Output

### JSON Report

```json
{
  "summary": {
    "method": "Multi-Camera Fusion Evaluation",
    "metrics_computed": 9
  },
  "image_quality_metrics": {
    "psnr_fused_vs_wide": 34.18,
    "ssim_fused_vs_wide": 0.906,
    "lpips_fused_vs_wide": 0.112
  },
  "custom_metrics": {
    "detail_transfer_score": 0.631,
    "ghost_score": 0.010,
    "alignment_quality": 0.501
  }
}
```

### CSV Export

For spreadsheet analysis:
```csv
Metric,Value
psnr_fused_vs_wide,34.18
ssim_fused_vs_wide,0.906
lpips_fused_vs_wide,0.112
detail_transfer_score,0.631
ghost_score,0.010
alignment_quality,0.501
```

## 🎓 Learning Exercises

### Exercise 1: Compare Methods

```bash
# Run all methods
cd ../02_classical_method && python align_and_fuse.py ...
cd ../03_dcsr_method && bash run_dcsr.sh ...
cd ../04_zoomgs_method && bash run_zoomgs.sh ...

# Evaluate all
cd ../05_evaluation
for method in classical dcsr zoomgs; do
    python eval_multicam.py \
        --fused ../results/$method/fused.png \
        --wide ../data/sample_01/wide.jpg \
        --tele_warp ../results/$method/tele_warp.png \
        --digital_zoom ../results/$method/digital_zoom.png \
        --output ../results/$method/metrics.json
done

# Compare
cat ../results/*/metrics.json
```

### Exercise 2: Parameter Sensitivity

```bash
# Test different alpha values
for alpha in 0.5 0.7 1.0 1.3 1.5; do
    cd ../02_classical_method
    python align_and_fuse.py \
        --wide ../data/sample_01/wide.jpg \
        --tele ../data/sample_01/tele.jpg \
        --out ../results/alpha_$alpha \
        --alpha $alpha
    
    cd ../05_evaluation
    python eval_multicam.py \
        --fused ../results/alpha_$alpha/fused.png \
        --wide ../results/alpha_$alpha/wide.png \
        --tele_warp ../results/alpha_$alpha/tele_warp.png \
        --digital_zoom ../results/alpha_$alpha/digital_zoom.png \
        --output ../results/alpha_$alpha/metrics.json
done

# Analyze: Which alpha gives best quality/artifact tradeoff?
```

## 📊 Interpreting Results

### Quality Indicators

**High PSNR but low Detail Transfer**:
- Image is smooth but lacks sharp details
- Solution: Increase fusion strength (alpha)

**High Detail Transfer but high Ghost Score**:
- Details transferred but with artifacts
- Solution: Improve alignment or reduce alpha

**Low Alignment Quality**:
- Registration failed or poor
- Solution: Check feature matching, try different images

### Method Selection Guide

| Scenario | Recommended Method | Reason |
|----------|-------------------|--------|
| Fast CPU-only | Classical | ~1 second, no GPU needed |
| Good quality/speed balance | DCSR | ~5 seconds, better quality |
| Maximum quality | ZoomGS | Best results, continuous zoom |
| Planar scenes | Classical | Sufficient, faster |
| Complex parallax | ZoomGS | Only method that handles it |

## 🔗 Related Content

- **Main README**: Part V, Sections 17-19
- **EXPERIMENTS.md**: Detailed experimental protocols
- **USAGE.md**: Command reference

## ➡️ Summary

After completing all sections, you should:
- ✅ Understand all three fusion methods
- ✅ Know how to evaluate results
- ✅ Be able to choose the right method
- ✅ Interpret metrics correctly

---

**Congratulations!** You've completed Chapter 15 on Multi-Camera Fusion Implementation! 🎉

