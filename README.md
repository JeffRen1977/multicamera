# Dual-Camera Smooth Zoom (ZoomGS) Implementation

This repository provides a comprehensive implementation of dual-camera fusion techniques for achieving smooth zoom effects, including both teaching-level implementations and integration with state-of-the-art methods.

## Overview

The project implements multiple approaches to dual-camera fusion:

1. **Teaching-level Implementation**: OpenCV-based registration and fusion for educational purposes
2. **DCSR Integration**: Dual-Camera Super-Resolution method
3. **ZoomGS Integration**: Dual-Camera Smooth Zoom method
4. **Comprehensive Evaluation**: Custom metrics for multi-camera fusion assessment

## Project Structure

```
MultiCamera/
├── experiments/
│   └── multicam/
│       ├── align_and_fuse.py          # Teaching-level fusion implementation
│       ├── eval_multicam.py           # Comprehensive evaluation script
│       ├── compare_all_methods.py     # Compare all fusion methods
│       ├── create_sample_data.py      # Generate sample test data
│       ├── run_dcsr.sh               # DCSR integration script
│       └── run_zoomgs.sh             # ZoomGS integration script
├── samples/                           # Sample test images
├── results/                          # Output results
├── thirdparty/                       # External repositories
└── requirements.txt                  # Python dependencies
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd MultiCamera
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create sample data** (optional):
   ```bash
   python experiments/multicam/create_sample_data.py --num_samples 5
   ```

## Quick Start

### 1. Teaching-Level Fusion

Run the basic OpenCV-based fusion method:

```bash
python experiments/multicam/align_and_fuse.py \
    --wide samples/sample_01/wide.jpg \
    --tele samples/sample_01/tele.jpg \
    --out results/teaching \
    --visualize
```

This will create:
- `fused.png`: Multi-camera fusion result
- `digital_zoom.png`: Digital zoom baseline
- `composite.png`: Side-by-side comparison
- `confidence_mask.png`: Fusion confidence map

### 2. Comprehensive Evaluation

Evaluate fusion results with multiple metrics:

```bash
python experiments/multicam/eval_multicam.py \
    --fused results/teaching/fused.png \
    --wide samples/sample_01/wide.jpg \
    --tele_warp results/teaching/tele_warp.png \
    --digital_zoom results/teaching/digital_zoom.png \
    --output results/evaluation_report.json
```

### 3. Compare All Methods

Run all available fusion methods and compare results:

```bash
python experiments/multicam/compare_all_methods.py \
    --wide samples/sample_01/wide.jpg \
    --tele samples/sample_01/tele.jpg \
    --output results/comparison
```

## Detailed Usage

### Teaching-Level Implementation (`align_and_fuse.py`)

The teaching-level implementation demonstrates the core concepts of dual-camera fusion:

**Key Features**:
- SIFT-based feature matching for image registration
- RANSAC-based homography estimation
- Multi-scale high-frequency detail transfer
- Confidence-based fusion with artifact reduction

**Parameters**:
- `--wide`: Path to wide angle image
- `--tele`: Path to telephoto image
- `--out`: Output directory
- `--visualize`: Save intermediate visualizations
- `--alpha`: Fusion strength parameter (default: 1.0)

**Algorithm Steps**:
1. **Feature Detection**: Extract SIFT features from both images
2. **Feature Matching**: Match features using BF matcher with Lowe's ratio test
3. **Homography Estimation**: Compute homography using RANSAC
4. **Image Warping**: Warp telephoto image to wide angle coordinate system
5. **Detail Extraction**: Extract high-frequency components using Gaussian blur
6. **Confidence Computation**: Compute fusion confidence based on photometric similarity
7. **Multi-scale Fusion**: Combine low-frequency (wide) and high-frequency (tele) components

### Evaluation Metrics (`eval_multicam.py`)

The evaluation script provides comprehensive assessment of fusion quality:

**Standard Metrics**:
- **PSNR**: Peak Signal-to-Noise Ratio
- **SSIM**: Structural Similarity Index
- **LPIPS**: Learned Perceptual Image Patch Similarity

**Custom Metrics**:
- **Detail Transfer Score**: Ratio of high-frequency energy preserved from telephoto
- **Ghost Score**: Measure of artifacts introduced by telephoto details
- **Alignment Quality**: Feature matching consistency assessment

### SOTA Integration

#### DCSR (Dual-Camera Super-Resolution)

```bash
bash experiments/multicam/run_dcsr.sh \
    samples/sample_01/wide.jpg \
    samples/sample_01/tele.jpg \
    results/dcsr
```

#### ZoomGS (Dual-Camera Smooth Zoom)

```bash
bash experiments/multicam/run_zoomgs.sh \
    samples/sample_01/wide.jpg \
    samples/sample_01/tele.jpg \
    results/zoomgs
```

## Sample Data

The repository includes tools to generate synthetic dual-camera data:

```bash
# Create synthetic samples
python experiments/multicam/create_sample_data.py --num_samples 5

# Create realistic sample using real image
python experiments/multicam/create_sample_data.py --realistic
```

**Sample Structure**:
```
samples/
├── sample_01/
│   ├── wide.jpg      # Wide angle simulation
│   ├── tele.jpg      # Telephoto simulation
│   ├── scene.jpg     # Original scene
│   └── composite.jpg # Side-by-side comparison
└── realistic/
    ├── wide.jpg      # Realistic wide angle
    └── tele.jpg      # Realistic telephoto
```

## Evaluation Results Interpretation

### Metrics Guide

**PSNR (Higher is Better)**:
- > 30 dB: Excellent quality
- 25-30 dB: Good quality
- 20-25 dB: Moderate quality
- < 20 dB: Poor quality

**SSIM (Higher is Better)**:
- > 0.9: Excellent structural similarity
- 0.8-0.9: Good structural similarity
- 0.7-0.8: Moderate structural similarity
- < 0.7: Poor structural similarity

**LPIPS (Lower is Better)**:
- < 0.1: Excellent perceptual similarity
- 0.1-0.2: Good perceptual similarity
- 0.2-0.3: Moderate perceptual similarity
- > 0.3: Poor perceptual similarity

**Detail Transfer Score (Higher is Better)**:
- > 0.8: Excellent detail preservation
- 0.6-0.8: Good detail preservation
- 0.4-0.6: Moderate detail preservation
- < 0.4: Poor detail preservation

**Ghost Score (Lower is Better)**:
- < 0.1: Minimal artifacts
- 0.1-0.2: Low artifacts
- 0.2-0.3: Moderate artifacts
- > 0.3: High artifacts

## Advanced Usage

### Custom Fusion Parameters

Modify fusion behavior by adjusting parameters in `align_and_fuse.py`:

```python
# Adjust fusion strength
alpha = 1.0  # Higher = more telephoto detail

# Adjust confidence threshold
thresh = 0.08  # Lower = more aggressive fusion

# Adjust Gaussian blur sigma
sigma = 5.0  # Higher = smoother fusion
```

### Batch Processing

Process multiple image pairs:

```bash
for i in {01..05}; do
    python experiments/multicam/align_and_fuse.py \
        --wide samples/sample_$i/wide.jpg \
        --tele samples/sample_$i/tele.jpg \
        --out results/sample_$i
done
```

### Custom Evaluation

Add custom metrics by extending the `MultiCameraEvaluator` class:

```python
def compute_custom_metric(self, img1, img2):
    # Your custom metric implementation
    return metric_value
```

## Troubleshooting

### Common Issues

1. **No features found**: Ensure images have sufficient texture and contrast
2. **Poor alignment**: Check for significant parallax or motion between images
3. **Artifacts in fusion**: Adjust confidence threshold or fusion parameters
4. **SOTA methods fail**: Ensure external repositories are properly cloned and dependencies installed

### Performance Optimization

- Use GPU acceleration for LPIPS computation
- Reduce image resolution for faster processing
- Use fewer SIFT features for faster registration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## References

- **DCSR**: Dual-Camera Super-Resolution (ICCV 2021)
- **ZoomGS**: Dual-Camera Smooth Zoom (ECCV 2024)
- **Handheld MFSR**: Multi-Frame Super-Resolution
- **RefVSR**: Reference-based Video Super-Resolution

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenCV community for computer vision tools
- PyTorch team for deep learning framework
- Original authors of DCSR and ZoomGS methods
