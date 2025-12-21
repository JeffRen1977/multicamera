# QuickStart Guide - Get Results in 60 Seconds

This guide gets you from zero to results in under 1 minute.

> **Note**: 
> - All code is organized in the `chapter15/` directory
> - All commands assume you're in the `MultiCamera/` root directory
> - The virtual environment is in the **parent directory** (one level above MultiCamera/)
> - Activate it with: `cd .. && source venv/bin/activate && cd MultiCamera`

---

## ⚡ Super Quick (30 seconds)

```bash
# One-time setup (if not done yet)
cd ..  # Go to parent directory (one level above MultiCamera/)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r MultiCamera/requirements.txt
cd MultiCamera  # Return to MultiCamera

# Run everything (make sure venv is activated from parent)
cd .. && source venv/bin/activate && cd MultiCamera  # On Windows: cd .. && venv\Scripts\activate && cd MultiCamera
./run_quick_test.sh

# View results
open results/quick_test/composite.png
```

**Done!** You should see a 4-panel comparison showing wide, digital zoom, fusion, and tele images.

---

## 🎯 Standard Workflow (60 seconds)

### Step 1: Setup (10 seconds)

```bash
# Activate virtual environment from parent directory
cd .. && source venv/bin/activate && cd MultiCamera  # On Windows: cd .. && venv\Scripts\activate && cd MultiCamera
# You should see (venv) in your prompt
```

### Step 2: Generate Sample Data (3 seconds)

```bash
# Make sure venv is activated (you should see (venv) in prompt)
python chapter15/01_setup/create_sample_data.py --num_samples 1 --output samples
```

### Step 3: Run Fusion (1 second)

```bash
python chapter15/02_classical_method/align_and_fuse.py \
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
# Make sure venv is activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

# After running fusion above, evaluate:
python chapter15/05_evaluation/eval_multicam.py \
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
# Make sure venv is activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Automated comparison
python chapter15/05_evaluation/compare_all_methods.py \
    --wide samples/sample_01/wide.jpg \
    --tele samples/sample_01/tele.jpg \
    --output results/comparison
```

**Note**: DCSR and ZoomGS will fail if dependencies not installed, but classical method will complete.

---

## 🎨 Use Your Own Photos

```bash
# Make sure venv is activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

python chapter15/02_classical_method/align_and_fuse.py \
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
# Make sure venv is activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Check environment
python --version  # Should be 3.8+

# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Try simple test
./run_quick_test.sh

# Still broken? Try complete workflow
cd chapter15 && bash run_complete_workflow.sh && cd ..
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

1. ✅ Got basic fusion working → Try `cd chapter15 && bash run_complete_workflow.sh` for full pipeline
2. ✅ Want to compare methods → See `USAGE.md` section on method comparison
3. ✅ Have your own photos → Replace paths in commands above
4. ✅ Want to understand algorithm → Read `README.md` Part II
5. ✅ Ready for research → Read `README.md` Parts III-IV on DCSR and ZoomGS
6. ✅ Want step-by-step tutorial → See `chapter15/02_classical_method/example_step_by_step.py`

---

*Total time from clone to results: <60 seconds* ⚡

