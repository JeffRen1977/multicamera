# Chapter 15: Multi-Camera Fusion Implementation

This directory contains all code, examples, and data for **Chapter 15: Multi-Camera Fusion for Computational Photography**.

## 📚 Directory Structure

```
chapter15/
├── README.md                    # This file - Chapter overview
├── 01_setup/                    # Setup and data preparation
│   ├── README.md               # Setup instructions
│   └── create_sample_data.py   # Generate test data
├── 02_classical_method/         # Classical CV approach
│   ├── README.md               # Method explanation
│   ├── align_and_fuse.py       # Main fusion algorithm
│   └── example_step_by_step.py # Step-by-step tutorial
├── 03_dcsr_method/              # Deep learning (DCSR)
│   ├── README.md               # DCSR explanation
│   └── run_dcsr.sh            # DCSR integration
├── 04_zoomgs_method/            # 3D reconstruction (ZoomGS)
│   ├── README.md               # ZoomGS explanation
│   └── run_zoomgs.sh          # ZoomGS integration
├── 05_evaluation/               # Evaluation and comparison
│   ├── README.md               # Evaluation guide
│   ├── eval_multicam.py       # Metrics computation
│   └── compare_all_methods.py # Method comparison
├── utils/                       # Shared utilities
│   └── image_utils.py         # Helper functions
├── data/                        # Sample data (generated)
└── results/                     # Output results
```

## 🎯 Learning Path

Follow these sections in order to understand multi-camera fusion:

### Step 1: Setup (Section 01_setup)
**Goal**: Prepare your environment and generate test data

```bash
cd chapter15/01_setup
python create_sample_data.py --num_samples 3
```

**What you'll learn**: How dual-camera data is structured

### Step 2: Classical Method (Section 02_classical_method)
**Goal**: Understand the fundamental fusion algorithm

```bash
cd chapter15/02_classical_method
python align_and_fuse.py \
    --wide ../data/sample_01/wide.jpg \
    --tele ../data/sample_01/tele.jpg \
    --out ../results/classical
```

**What you'll learn**: 
- Feature detection and matching
- Geometric alignment
- Frequency-domain fusion

### Step 3: Deep Learning (Section 03_dcsr_method)
**Goal**: See how deep learning improves fusion

```bash
cd chapter15/03_dcsr_method
bash run_dcsr.sh ../data/sample_01/wide.jpg ../data/sample_01/tele.jpg ../results/dcsr
```

**What you'll learn**: Attention-based alignment

### Step 4: 3D Reconstruction (Section 04_zoomgs_method)
**Goal**: Understand 3D scene representation

```bash
cd chapter15/04_zoomgs_method
bash run_zoomgs.sh ../data/sample_01/wide.jpg ../data/sample_01/tele.jpg ../results/zoomgs
```

**What you'll learn**: Gaussian splatting and continuous zoom

### Step 5: Evaluation (Section 05_evaluation)
**Goal**: Compare all methods quantitatively

```bash
cd chapter15/05_evaluation
python compare_all_methods.py \
    --wide ../data/sample_01/wide.jpg \
    --tele ../data/sample_01/tele.jpg \
    --output ../results/comparison
```

**What you'll learn**: Evaluation metrics and method comparison

## 🚀 Quick Start

**Complete workflow** (runs all steps):

```bash
cd chapter15

# Step 1: Setup
cd 01_setup && python create_sample_data.py --num_samples 1 && cd ..

# Step 2: Classical method
cd 02_classical_method && python align_and_fuse.py \
    --wide ../data/sample_01/wide.jpg \
    --tele ../data/sample_01/tele.jpg \
    --out ../results/classical && cd ..

# Step 3: Evaluate
cd 05_evaluation && python eval_multicam.py \
    --fused ../results/classical/fused.png \
    --wide ../results/classical/wide.png \
    --tele_warp ../results/classical/tele_warp.png \
    --digital_zoom ../results/classical/digital_zoom.png \
    --output ../results/classical/metrics.json && cd ..
```

## 📖 How to Use This Chapter

### For Students Learning

1. **Read the main README.md** (in parent directory) for theory
2. **Follow each section** in order (01 → 02 → 03 → 04 → 05)
3. **Run the code** as you read each section
4. **Examine the outputs** to understand what each step does
5. **Modify parameters** to see their effects

### For Researchers

1. **Start with 02_classical_method** for baseline
2. **Compare with 03_dcsr_method** and **04_zoomgs_method**
3. **Use 05_evaluation** for quantitative analysis
4. **Modify code** in each section for your experiments

### For Practitioners

1. **Go directly to 02_classical_method** for working code
2. **Use your own images** by replacing sample paths
3. **Tune parameters** in `align_and_fuse.py`
4. **Evaluate results** with `05_evaluation/eval_multicam.py`

## 🔗 Links to Main README

Each section corresponds to parts of the main README.md:

- **01_setup** → README Part I, Section 4
- **02_classical_method** → README Part II, Sections 5-10
- **03_dcsr_method** → README Part III, Sections 11-13
- **04_zoomgs_method** → README Part IV, Sections 14-16
- **05_evaluation** → README Part V, Sections 17-19

## 📝 Code Organization Philosophy

**Why this structure?**

1. **Progressive Learning**: Each section builds on previous
2. **Clear Separation**: Each method in its own directory
3. **Easy Navigation**: Find code related to specific topics
4. **Self-Contained**: Each section can be understood independently
5. **Reproducible**: Clear paths and dependencies

## 🎓 Exercises

After completing each section, try:

1. **Modify parameters** and observe changes
2. **Use your own images** instead of samples
3. **Compare outputs** between methods
4. **Analyze metrics** to understand quality tradeoffs

## 📞 Need Help?

- Check each section's README.md for specific instructions
- See main README.md for detailed theory
- Review USAGE.md for command reference
- Check EXPERIMENTS.md for detailed protocols

---

**Start here**: `cd chapter15/01_setup` and follow the README!


