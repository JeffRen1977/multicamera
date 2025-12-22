# Section 4: 3D Reconstruction Approach (ZoomGS)

This section covers **ZoomGS (Dual-Camera Smooth Zoom)** using 3D Gaussian Splatting for continuous zoom rendering.

## 📋 What This Section Covers

- 3D Gaussian scene representation
- Structure-from-Motion initialization
- Differentiable Gaussian rasterization
- Continuous zoom via camera interpolation
- Running ZoomGS inference

## 🚀 Quick Start

```bash
# From chapter15/ directory
cd 04_zoomgs_method

# Run ZoomGS fusion
bash run_zoomgs.sh \
    ../data/sample_01/wide.jpg \
    ../data/sample_01/tele.jpg \
    ../results/zoomgs
```

## 🔬 How ZoomGS Works

**Key Innovation**: Builds **3D scene representation** using Gaussian splatting, enabling continuous zoom at arbitrary levels.

**Pipeline**:
```
Wide + Tele Images
  ↓
Structure-from-Motion (SfM)
  ↓
Dense Depth Estimation
  ↓
3D Gaussian Initialization
  ↓
Optimization (7K iterations)
  ↓
Differentiable Rendering
  ↓
Continuous Zoom Rendering
```

**Advantages**:
- ✅ Best visual quality (PSNR 32-38 dB)
- ✅ Smooth continuous zoom (not just discrete)
- ✅ Handles strong parallax
- ✅ Physically correct rendering

**Trade-offs**:
- ❌ Per-scene optimization (~8 seconds)
- ❌ Requires GPU with CUDA
- ❌ Memory intensive (~4GB)
- ❌ Complex implementation

## 📊 Expected Performance

- **PSNR**: 32-38 dB (best quality)
- **SSIM**: 0.92-0.96 (excellent)
- **LPIPS**: 0.06-0.12 (best perceptual)
- **Processing**: ~8 seconds (high-end GPU)
- **Rendering**: 30-60 FPS after optimization

## 🔍 Understanding the Script

The `run_zoomgs.sh` script:

1. **Clones ZoomGS repository** from GitHub
2. **Builds CUDA extensions** for Gaussian splatting
3. **Downloads pre-trained models**
4. **Runs full pipeline**: SfM → Optimization → Rendering
5. **Saves results** to output directory

**First run**: Takes ~10 minutes (downloads + builds CUDA)  
**Subsequent runs**: ~8 seconds

## 📝 Requirements

- **NVIDIA GPU**: Required (CUDA support)
- **GPU Memory**: 4GB+ for 1920×1080 images
- **CUDA**: Version 11.0 or higher
- **Disk space**: ~5GB for repository and models
- **Internet**: Required for first run

## 🎓 Learning Objectives

After this section, you should:
- ✅ Understand 3D scene representation
- ✅ See how Gaussian splatting works
- ✅ Understand continuous zoom capability
- ✅ Compare ZoomGS vs other methods

## 🔗 Related Content

- **Paper**: "Dual-Camera Smooth Zoom on Mobile Phones" (ECCV 2024)
- **Main README**: Part IV, Sections 14-16
- **Repository**: https://github.com/ZcsrenlongZ/ZoomGS

## ⚠️ Note

If you don't have a CUDA-capable GPU, you can:
- Read the algorithm description in main README
- View example results if provided
- Focus on Sections 2 and 3 (classical and DCSR)

## ➡️ Next Step

Proceed to `../05_evaluation/` to compare all methods quantitatively!

---

**Note**: ZoomGS is the most advanced method but also most resource-intensive. Use when maximum quality is required.


