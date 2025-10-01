# QuickStart Guide - Get Results in 60 Seconds

This guide gets you from zero to results in under 1 minute.

---

## ⚡ Super Quick (30 seconds)

```bash
# One-time setup (if not done yet)
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# Run everything
./run_quick_test.sh

# View results
open results/quick_test/composite.png
```

**Done!** You should see a 4-panel comparison showing wide, digital zoom, fusion, and tele images.

---

## 🎯 Standard Workflow (60 seconds)

### Step 1: Setup (10 seconds)

```bash
source venv/bin/activate
```

### Step 2: Generate Sample Data (3 seconds)

```bash
python multicam/create_sample_data.py --num_samples 1
```

### Step 3: Run Fusion (1 second)

```bash
python multicam/align_and_fuse.py \
    --wide samples/sample_01/wide.jpg \
    --tele samples/sample_01/tele.jpg \
    --out results/my_first_experiment
```

### Step 4: Check Results (instant)

```bash
open results/my_first_experiment/composite.png
cat results/my_first_experiment/*.png
```

---

## 📊 With Evaluation (90 seconds)

```bash
# After running fusion above, evaluate:
python multicam/eval_multicam.py \
    --fused results/my_first_experiment/fused.png \
    --wide results/my_first_experiment/wide.png \
    --tele_warp results/my_first_experiment/tele_warp.png \
    --digital_zoom results/my_first_experiment/digital_zoom.png \
    --output results/my_first_experiment/metrics.json

# View metrics
cat results/my_first_experiment/metrics.json
```

**You should see**:
- PSNR: ~34 dB (excellent)
- SSIM: ~0.90 (excellent)
- LPIPS: ~0.11 (good)

---

## 🔄 Compare All Methods (2 minutes)

```bash
source venv/bin/activate

# Automated comparison
python multicam/compare_all_methods.py \
    --wide samples/sample_01/wide.jpg \
    --tele samples/sample_01/tele.jpg \
    --output results/comparison
```

**Note**: DCSR and ZoomGS will fail if dependencies not installed, but classical method will complete.

---

## 🎨 Use Your Own Photos

```bash
source venv/bin/activate

python multicam/align_and_fuse.py \
    --wide /path/to/your/wide.jpg \
    --tele /path/to/your/tele.jpg \
    --out results/my_photos \
    --visualize
```

**Tips**:
- Capture both photos within 1 second
- Keep camera steady
- Subject 2-10 meters away
- Good lighting

---

## 🐛 If Something Goes Wrong

```bash
# Check environment
python --version  # Should be 3.9+

# Reinstall
pip install -r requirements.txt

# Try simple test
./run_quick_test.sh

# Still broken? Try demo
python demo.py
```

---

## 📚 For More Details

- **Complete usage**: See `USAGE.md`
- **Experiments**: See `EXPERIMENTS.md`
- **Full documentation**: See `README.md`

---

## ✅ Success Checklist

After running `./run_quick_test.sh`, you should have:

- [x] `results/quick_test/fused.png` - Your fusion result
- [x] `results/quick_test/composite.png` - Side-by-side comparison
- [x] `results/quick_test/confidence_mask.png` - Confidence visualization
- [x] Console output showing "Found XXX matches"
- [x] No error messages

If all checked, **you're ready to go!** 🎉

---

## 🎓 Next Steps

1. ✅ Got basic fusion working → Try `./run_all.sh` for full pipeline
2. ✅ Want to compare methods → See `USAGE.md` section on method comparison
3. ✅ Have your own photos → Replace paths in commands above
4. ✅ Want to understand algorithm → Read `README.md` Part II
5. ✅ Ready for research → Read `README.md` Parts III-IV on DCSR and ZoomGS

---

*Total time from clone to results: <60 seconds* ⚡

