# Section 2: Classical Computer Vision Method

This section implements the **teaching-level classical approach** to multi-camera fusion using SIFT features, RANSAC alignment, and frequency-domain fusion.

## 📋 What This Section Covers

- SIFT feature detection and matching
- RANSAC homography estimation
- Image warping and alignment
- Multi-scale frequency decomposition
- Confidence-based fusion
- Complete working implementation

## 🚀 Quick Start

```bash
# From chapter15/ directory
cd 02_classical_method

# Run fusion algorithm
python align_and_fuse.py \
    --wide ../data/sample_01/wide.jpg \
    --tele ../data/sample_01/tele.jpg \
    --out ../results/classical \
    --visualize

# View results
open ../results/classical/composite.png
```

## 📊 Algorithm Pipeline

```
Input: Wide + Tele Images
  ↓
[1] SIFT Feature Detection
    → Detects keypoints in both images
    → Extracts 128-D descriptors
  ↓
[2] Feature Matching
    → Brute-force matching
    → Lowe's ratio test (0.75 threshold)
  ↓
[3] Homography Estimation
    → RANSAC robust estimation
    → 3×3 transformation matrix H
  ↓
[4] Image Warping
    → Warp telephoto to wide coordinates
    → Perspective transformation
  ↓
[5] Frequency Decomposition
    → Low-freq: GaussianBlur(I, σ=5)
    → High-freq: I - Low-freq
  ↓
[6] Confidence Computation
    → Photometric similarity check
    → Generate confidence mask
  ↓
[7] Fusion
    → Combine frequencies with confidence
    → Fused = Low_wide + Conf×High_tele + (1-Conf)×High_wide
  ↓
Output: High-Quality Fused Image
```

## 📁 Code Files

- **`align_and_fuse.py`**: Complete fusion pipeline
- **`example_step_by_step.py`**: Step-by-step tutorial (see below)

## 🔬 Step-by-Step Tutorial

For detailed understanding, use the step-by-step example:

```bash
python example_step_by_step.py \
    --wide ../data/sample_01/wide.jpg \
    --tele ../data/sample_01/tele.jpg \
    --out ../results/tutorial
```

This saves intermediate results at each step:
- `step1_features.png` - Feature keypoints
- `step2_matches.png` - Feature matches
- `step3_homography.png` - Alignment visualization
- `step4_warped.png` - Warped telephoto
- `step5_frequencies.png` - Frequency decomposition
- `step6_confidence.png` - Confidence map
- `step7_fused.png` - Final result

## 🎯 Key Concepts

### 1. Feature Detection (SIFT)

**Why SIFT?**
- Scale-invariant: Works at different zoom levels
- Rotation-invariant: Handles camera orientation
- Robust: Works with lighting changes

**What to observe**:
- Number of keypoints detected
- Distribution across image
- Quality of descriptors

### 2. Homography Estimation (RANSAC)

**Why RANSAC?**
- Robust to outliers (moving objects, mismatches)
- Handles up to 50% outliers
- Finds best model despite noise

**What to observe**:
- Inlier ratio (should be >50%)
- Reprojection error
- Quality of alignment

### 3. Frequency Decomposition

**Why separate frequencies?**
- Wide camera: Good for low-frequency (structure, color)
- Tele camera: Good for high-frequency (details, sharpness)
- Fusion: Combine strengths of both

**What to observe**:
- Low-frequency: Smooth, structural information
- High-frequency: Sharp edges, fine details

### 4. Confidence-Based Fusion

**Why confidence mask?**
- Not all regions align perfectly
- Some areas have parallax or motion
- Confidence tells us where to trust tele details

**What to observe**:
- High confidence: Well-aligned regions
- Low confidence: Misaligned or occluded regions

## 📊 Expected Results

**Quantitative Metrics** (typical):
- PSNR: 28-34 dB (excellent if >30 dB)
- SSIM: 0.88-0.92 (excellent if >0.9)
- LPIPS: 0.12-0.20 (good if <0.2)
- Processing time: ~1 second (CPU)

**Visual Quality**:
- Fused image should be sharper than digital zoom
- Should preserve wide camera's field of view
- Should add telephoto's fine details
- Minimal artifacts (ghosting, blurring)

## 🎓 Learning Exercises

### Exercise 1: Understand Feature Matching

```bash
# Run with visualization
python align_and_fuse.py \
    --wide ../data/sample_01/wide.jpg \
    --tele ../data/sample_01/tele.jpg \
    --out ../results/ex1 \
    --visualize

# Examine match_vis.jpg
# Count: How many matches? Are they well distributed?
```

### Exercise 2: Test Different Parameters

```bash
# Test fusion strength
for alpha in 0.5 0.7 1.0 1.3 1.5; do
    python align_and_fuse.py \
        --wide ../data/sample_01/wide.jpg \
        --tele ../data/sample_01/tele.jpg \
        --out ../results/alpha_$alpha \
        --alpha $alpha
done

# Compare: Which alpha gives best quality?
open ../results/alpha_*/composite.png
```

### Exercise 3: Use Your Own Images

```bash
# Replace with your dual-camera photos
python align_and_fuse.py \
    --wide /path/to/your/wide.jpg \
    --tele /path/to/your/tele.jpg \
    --out ../results/my_photos \
    --visualize
```

## 🔍 Understanding the Code

**Main Functions**:

1. `detect_and_match_features()`: SIFT detection + matching
2. `estimate_homography()`: RANSAC homography estimation
3. `warp_telephoto_image()`: Perspective transformation
4. `decompose_frequency()`: Gaussian blur separation
5. `compute_confidence_mask()`: Photometric consistency
6. `fuse_images()`: Multi-scale frequency fusion

**Key Parameters**:
- `--alpha`: Fusion strength (0.5-2.0, default: 1.0)
- `--visualize`: Save intermediate visualizations

## ⚠️ Common Issues

**"Not enough matches"**:
- Images may have insufficient texture
- Try different sample or add more texture

**Poor alignment**:
- Strong parallax (subject too close)
- Camera motion between captures
- Solution: Use subjects farther away

**Artifacts in fusion**:
- Misalignment
- Exposure mismatch
- Solution: Reduce `--alpha` or improve alignment

## ➡️ Next Steps

1. **Understand the algorithm**: Read code comments
2. **Experiment with parameters**: Try different `--alpha` values
3. **Compare with baselines**: See digital zoom output
4. **Proceed to Section 3**: Learn deep learning approach (DCSR)

---

**Related README Sections**: Main README Part II, Sections 5-10

