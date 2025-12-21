# Getting Started - Multi-Camera Computational Photography

**Welcome!** This guide will get you running multi-camera fusion experiments in minutes.

> **Note**: All code is organized in the `chapter15/` directory. All commands assume you're in the `MultiCamera/` root directory with the virtual environment activated.

---

## 📚 Documentation Overview

We have **5 documentation files** to help you:

| File | Purpose | Read Time | Who Is It For? |
|------|---------|-----------|----------------|
| **GETTING_STARTED.md** (this file) | Start here! | 2 min | Everyone |
| **QUICKSTART.md** | Get results in 60 seconds | 3 min | First-timers |
| **USAGE.md** | Command reference | 10 min | Practitioners |
| **EXPERIMENTS.md** | Detailed protocols | 20 min | Researchers |
| **SCRIPTS.md** | Script documentation | 5 min | Developers |
| **README.md** | Complete book chapter | 60 min | Deep learners |

---

## 🎯 Choose Your Path

### Path 1: "Just show me results!" (30 seconds)

```bash
# Setup (one-time)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

# Run quick test (make sure venv is activated)
source venv/bin/activate  # On Windows: venv\Scripts\activate
./run_quick_test.sh
open results/quick_test/composite.png
```

**What you'll see**: Side-by-side comparison of fusion methods  
**Next**: Read `QUICKSTART.md`

---

### Path 2: "I want to understand how it works" (5 minutes)

```bash
# Setup
source venv/bin/activate

# Generate sample data
python chapter15/01_setup/create_sample_data.py --num_samples 1

# Run fusion with visualization
python chapter15/02_classical_method/align_and_fuse.py \
    --wide samples/sample_01/wide.jpg \
    --tele samples/sample_01/tele.jpg \
    --out results/learn \
    --visualize

# Check outputs
open match_vis.jpg  # See feature matching
open results/learn/confidence_mask.png  # See fusion confidence
open results/learn/composite.png  # See final comparison
```

**Next**: Read `README.md` Part II (Classical Approach)

---

### Path 3: "I have my own photos to process" (2 minutes)

```bash
source venv/bin/activate

python chapter15/02_classical_method/align_and_fuse.py \
    --wide /path/to/your/wide_photo.jpg \
    --tele /path/to/your/tele_photo.jpg \
    --out results/my_photos \
    --visualize

open results/my_photos/composite.png
```

**Tips for capture**:
- Take both photos within 1 second
- Keep camera steady
- Subject 2-10 meters away

**Next**: Read `USAGE.md` section on "Testing Your Own Images"

---

### Path 4: "I want to compare all methods" (3 minutes)

```bash
source venv/bin/activate

python chapter15/05_evaluation/compare_all_methods.py \
    --wide samples/sample_01/wide.jpg \
    --tele samples/sample_01/tele.jpg \
    --output results/comparison

cat results/comparison/comparison_report.json
```

**Next**: Read `README.md` Part V (Comprehensive Analysis)

---

### Path 5: "I'm doing research" (Full deep dive)

1. Read `README.md` completely (the book chapter)
2. Follow `EXPERIMENTS.md` protocols
3. Run all methods and collect data
4. Use `SCRIPTS.md` as reference
5. Customize and extend

---

## 🛠️ One-Time Setup (Do This First)

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Verify
python -c "import cv2, numpy, torch, lpips; print('✅ Ready!')"
```

**Only do this once!** For future sessions, just run: `source venv/bin/activate`

---

## 🎓 What You Get

### Three Fusion Methods

1. **Classical (Teaching Method)**
   - Algorithm: SIFT + Homography + Frequency fusion
   - Speed: ~1 second (CPU)
   - Quality: PSNR 34 dB
   - Best for: Learning, fast prototyping

2. **DCSR (Deep Learning)**
   - Algorithm: Attention-based alignment
   - Speed: ~5 seconds (GPU)
   - Quality: PSNR 30-35 dB
   - Best for: Production deployment

3. **ZoomGS (3D Gaussian)**
   - Algorithm: 3D scene reconstruction
   - Speed: ~8 seconds (GPU)
   - Quality: PSNR 32-38 dB
   - Best for: Best quality, smooth zoom

### Evaluation Metrics

- **PSNR**: Image quality (higher = better)
- **SSIM**: Structural similarity (higher = better)
- **LPIPS**: Perceptual quality (lower = better)
- **Detail Transfer**: Tele detail preservation (higher = better)
- **Ghost Score**: Artifact level (lower = better)
- **Alignment Quality**: Registration accuracy (higher = better)

---

## 📊 Expected Results

When you run `./run_quick_test.sh`, you should see:

```
✅ Virtual environment activated
📸 Creating sample data...
🔬 Running fusion...
  Found 252 matches
  Computing homography...
  Fusing images...
✅ Quick test completed!

📁 Results: results/quick_test/
   - fused.png (PSNR: ~34 dB)
   - composite.png (comparison)
```

---

## ❓ Common Questions

**Q: Do I need a GPU?**  
A: No! Classical method runs on CPU. GPU only needed for DCSR/ZoomGS.

**Q: Can I use my phone photos?**  
A: Yes! Just provide paths to your wide and tele photos.

**Q: How long does it take?**  
A: Classical method: ~1 second. Full comparison: ~15 seconds.

**Q: What if I get errors?**  
A: Check `USAGE.md` troubleshooting section or try `./run_quick_test.sh`

**Q: Which method should I use?**  
A: Start with classical method. If you need better quality and have GPU, try DCSR.

---

## 🎯 Success Criteria

After running `./run_quick_test.sh`, you should have:

- ✅ No error messages in console
- ✅ `results/quick_test/fused.png` file created
- ✅ `results/quick_test/composite.png` showing 4-panel comparison
- ✅ Fusion result looks sharper than digital zoom
- ✅ Console shows "Found XXX matches" (where XXX > 50)

If all checked, **you're all set!** 🎉

---

## 🚀 Next Steps

After successful quick test:

1. **Understand the algorithm**:
   - Read `README.md` sections 5-8 (Classical approach)
   - Examine `match_vis.jpg` to see feature matching
   - Study `confidence_mask.png` to understand fusion weights

2. **Run full evaluation**:
   - Follow `USAGE.md` "Step-by-Step" section
   - Collect quantitative metrics
   - Analyze results

3. **Try different parameters**:
   - Test `--alpha` values: 0.5, 0.7, 1.0, 1.3, 1.5
   - Compare quality vs artifacts
   - Find optimal settings for your use case

4. **Compare methods**:
   - Run DCSR: `bash chapter15/03_dcsr_method/run_dcsr.sh ...`
   - Run ZoomGS: `bash chapter15/04_zoomgs_method/run_zoomgs.sh ...`
   - Compare quantitative metrics

5. **Use your own photos**:
   - Capture dual-camera photos
   - Process with fusion algorithm
   - Evaluate real-world performance

---

## 📖 Reading Guide

**If you have**:
- **5 minutes**: Read this file + run `./run_quick_test.sh`
- **15 minutes**: Read `QUICKSTART.md` + `USAGE.md`
- **30 minutes**: Read `EXPERIMENTS.md` + run Experiments 1-3
- **1 hour**: Read `README.md` Part II (Classical approach)
- **3 hours**: Read complete `README.md` (full book chapter)
- **1 day**: Read all docs + run all experiments + understand theory

---

## 🎓 Learning Outcomes

After completing this chapter, you will:

✅ **Understand** the challenges of multi-camera fusion  
✅ **Implement** a working fusion algorithm from scratch  
✅ **Evaluate** results with proper metrics  
✅ **Compare** classical vs deep learning vs 3D approaches  
✅ **Apply** to your own dual-camera images  
✅ **Optimize** parameters for different scenarios

---

## 💡 Pro Tips

1. **Start simple**: Run `./run_quick_test.sh` first
2. **Visualize**: Always use `--visualize` flag to see feature matches
3. **Compare**: Look at `composite.png` for side-by-side comparisons
4. **Metrics**: PSNR >30 dB is excellent, <20 dB is poor
5. **Parameters**: Start with defaults, tune only if needed
6. **Real photos**: Capture with tripod for best results

---

## 🆘 Quick Help

**Script won't run?**
```bash
chmod +x run_quick_test.sh run_all.sh
```

**Import errors?**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**No results?**
```bash
ls -lh results/
# Should show directories with .png files
```

---

## 📞 Support Resources

1. **QUICKSTART.md** - Basic usage
2. **USAGE.md** - Command reference
3. **EXPERIMENTS.md** - Detailed protocols
4. **SCRIPTS.md** - Script documentation
5. **README.md** - Complete theory

**Still stuck?** Check the troubleshooting sections in `USAGE.md`

---

**Ready to start?** Run this now:

```bash
source venv/bin/activate && ./run_quick_test.sh
```

Then explore the other documentation files based on your needs! 🚀
