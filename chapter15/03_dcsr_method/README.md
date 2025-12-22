# Section 3: Deep Learning Approach (DCSR)

This section covers the **DCSR (Dual-Camera Super-Resolution)** method using deep learning with aligned attention modules.

## 📋 What This Section Covers

- DCSR architecture overview
- Attention-based feature alignment
- Running DCSR inference
- Comparing with classical method

## 🚀 Quick Start

```bash
# From chapter15/ directory
cd 03_dcsr_method

# Run DCSR fusion
bash run_dcsr.sh \
    ../data/sample_01/wide.jpg \
    ../data/sample_01/tele.jpg \
    ../results/dcsr
```

## 🔬 How DCSR Works

**Key Innovation**: Uses **Aligned Attention Modules (AAM)** to learn feature alignment instead of geometric homography.

**Architecture**:
```
Wide Image → Feature Encoder → ┐
                                ├→ Aligned Attention Module → Fusion → SR Image
Tele Image → Feature Encoder → ┘
```

**Advantages over Classical Method**:
- ✅ Handles moderate parallax better
- ✅ Learns alignment from data
- ✅ Better detail preservation
- ✅ More robust to scene variations

**Trade-offs**:
- ❌ Requires GPU for reasonable speed
- ❌ Needs pre-trained model
- ❌ Less interpretable (black box)

## 📊 Expected Performance

- **PSNR**: 30-35 dB (vs 28-32 dB classical)
- **SSIM**: 0.90-0.95 (vs 0.88-0.92 classical)
- **Processing**: ~5 seconds (GPU) vs ~1 second (CPU classical)
- **Quality**: Better for complex scenes with parallax

## 🔍 Understanding the Script

The `run_dcsr.sh` script:

1. **Clones DCSR repository** from GitHub
2. **Creates isolated environment** (`dcsr_venv`)
3. **Downloads pre-trained model** (~200MB)
4. **Runs inference** with your images
5. **Saves results** to output directory

**First run**: Takes ~5 minutes (downloads repo + model)  
**Subsequent runs**: ~5 seconds

## 📝 Requirements

- **GPU**: Recommended (works on CPU but slower)
- **Internet**: Required for first run (to download repo)
- **Disk space**: ~2GB for repository and models

## 🎓 Learning Objectives

After this section, you should:
- ✅ Understand how deep learning improves fusion
- ✅ See attention-based alignment in action
- ✅ Compare DCSR vs classical method
- ✅ Know when to use DCSR

## 🔗 Related Content

- **Paper**: "Dual-Camera Super-Resolution with Aligned Attention Modules" (ICCV 2021)
- **Main README**: Part III, Sections 11-13
- **Repository**: https://github.com/Tengfei-Wang/DCSR

## ➡️ Next Step

Proceed to `../04_zoomgs_method/` to learn 3D reconstruction approach!

---

**Note**: If DCSR fails (no GPU, network issues), you can still proceed to Section 4 or compare with Section 2 results.


