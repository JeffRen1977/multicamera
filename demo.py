#!/usr/bin/env python3
"""
demo.py
Quick demonstration of the dual-camera fusion system.
This script creates sample data and runs the teaching-level fusion method.
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(cmd, description):
    """Run a command and print the result."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent)
        if result.returncode == 0:
            print("✅ SUCCESS")
            if result.stdout:
                print("Output:", result.stdout)
        else:
            print("❌ FAILED")
            if result.stderr:
                print("Error:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def main():
    """Run the complete demo pipeline."""
    print("🚀 Dual-Camera Fusion Demo")
    print("This demo will create sample data and run fusion experiments.")
    
    # Check if we're in the right directory
    if not Path("experiments/multicam/align_and_fuse.py").exists():
        print("❌ Error: Please run this script from the MultiCamera root directory")
        sys.exit(1)
    
    # Step 1: Create sample data
    print("\n📸 Step 1: Creating sample data...")
    success = run_command([
        "python", "experiments/multicam/create_sample_data.py",
        "--num_samples", "3",
        "--output", "samples"
    ], "Creating 3 sample dual-camera image pairs")
    
    if not success:
        print("❌ Failed to create sample data. Exiting.")
        sys.exit(1)
    
    # Step 2: Run teaching-level fusion
    print("\n🔬 Step 2: Running teaching-level fusion...")
    success = run_command([
        "python", "experiments/multicam/align_and_fuse.py",
        "--wide", "samples/sample_01/wide.jpg",
        "--tele", "samples/sample_01/tele.jpg",
        "--out", "results/demo_teaching",
        "--visualize"
    ], "Teaching-level OpenCV-based fusion")
    
    if not success:
        print("❌ Failed to run fusion. Exiting.")
        sys.exit(1)
    
    # Step 3: Evaluate results
    print("\n📊 Step 3: Evaluating fusion results...")
    success = run_command([
        "python", "experiments/multicam/eval_multicam.py",
        "--fused", "results/demo_teaching/fused.png",
        "--wide", "samples/sample_01/wide.jpg",
        "--tele_warp", "results/demo_teaching/tele_warp.png",
        "--digital_zoom", "results/demo_teaching/digital_zoom.png",
        "--output", "results/demo_evaluation.json"
    ], "Comprehensive evaluation with custom metrics")
    
    # Step 4: Show results
    print("\n📁 Step 4: Results Summary")
    print("="*60)
    
    results_dir = Path("results/demo_teaching")
    if results_dir.exists():
        print("Generated files:")
        for file_path in sorted(results_dir.glob("*")):
            print(f"  📄 {file_path.name}")
    
    # Check if evaluation was successful
    eval_file = Path("results/demo_evaluation.json")
    if eval_file.exists():
        print(f"\n📊 Evaluation report: {eval_file}")
        print("Key metrics:")
        try:
            import json
            with open(eval_file, 'r') as f:
                eval_data = json.load(f)
            
            if 'image_quality_metrics' in eval_data:
                metrics = eval_data['image_quality_metrics']
                print(f"  PSNR: {metrics.get('psnr_fused_vs_wide', 'N/A'):.2f} dB")
                print(f"  SSIM: {metrics.get('ssim_fused_vs_wide', 'N/A'):.4f}")
                print(f"  LPIPS: {metrics.get('lpips_fused_vs_wide', 'N/A'):.4f}")
            
            if 'custom_metrics' in eval_data:
                custom = eval_data['custom_metrics']
                print(f"  Detail Transfer Score: {custom.get('detail_transfer_score', 'N/A'):.4f}")
                print(f"  Ghost Score: {custom.get('ghost_score', 'N/A'):.4f}")
                print(f"  Alignment Quality: {custom.get('alignment_quality', 'N/A'):.4f}")
        except Exception as e:
            print(f"  Could not parse evaluation results: {e}")
    
    print("\n🎉 Demo completed successfully!")
    print("\nNext steps:")
    print("1. Check the results in the 'results/demo_teaching/' directory")
    print("2. View the composite.png for side-by-side comparison")
    print("3. Try different parameters with --alpha option")
    print("4. Run SOTA methods with run_dcsr.sh or run_zoomgs.sh")
    print("5. Use compare_all_methods.py for comprehensive comparison")


if __name__ == "__main__":
    main()
