# Section 1: Setup and Data Preparation

This section covers environment setup and generating sample dual-camera data for experiments.

## 📋 What This Section Covers

- Creating virtual environment
- Installing dependencies
- Generating synthetic dual-camera image pairs
- Understanding data structure

## 🚀 Quick Start

```bash
# From chapter15/ directory
cd 01_setup

# Generate 3 sample pairs
python create_sample_data.py --num_samples 3 --output ../data

# Check generated data
ls -lh ../data/sample_01/
```

## 📁 Generated Data Structure

After running `create_sample_data.py`, you'll have:

```
chapter15/data/
├── sample_01/
│   ├── wide.jpg      # Wide-angle camera simulation (800×1200)
│   ├── tele.jpg      # Telephoto camera simulation (800×1200)
│   ├── scene.jpg     # Original synthetic scene
│   └── composite.jpg # Side-by-side input comparison
├── sample_02/
└── sample_03/
```

## 🔍 Understanding the Data

**Wide Camera Simulation**:
- Field of view: Full scene (1× zoom)
- Characteristics: Slight blur, warm color cast
- Purpose: Provides context and structure

**Telephoto Camera Simulation**:
- Field of view: Center crop (2× zoom)
- Characteristics: Enhanced details, cool color cast
- Purpose: Provides fine details and sharpness

## 📝 Code Explanation

The `create_sample_data.py` script:

1. **Creates synthetic scene**: Geometric shapes, text, gradients
2. **Simulates wide camera**: Applies blur and color shift
3. **Simulates tele camera**: Crops center, enhances details
4. **Adds camera artifacts**: Vignetting, chromatic aberration, noise

**Key Parameters**:
- `--num_samples`: Number of image pairs to generate
- `--output`: Where to save the data
- `--realistic`: Use real image instead of synthetic

## 🎯 Learning Objectives

After this section, you should:
- ✅ Understand dual-camera data structure
- ✅ Know how to generate test data
- ✅ Be ready to process images in next sections

## ➡️ Next Step

Proceed to `../02_classical_method/` to learn the fusion algorithm!

---

**Related README Sections**: Main README Part I, Section 4


