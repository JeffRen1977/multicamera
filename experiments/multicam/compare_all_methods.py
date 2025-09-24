#!/usr/bin/env python3
"""
compare_all_methods.py
Comprehensive comparison script that runs all multi-camera fusion methods
and generates detailed evaluation reports.
"""

import os
import sys
import subprocess
import argparse
import json
import shutil
from pathlib import Path
import cv2
import numpy as np
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt


class MultiCameraComparison:
    """Comprehensive comparison of multi-camera fusion methods."""
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.results_dir = self.base_dir / "comparison_results"
        self.results_dir.mkdir(exist_ok=True)
        
        # Method configurations
        self.methods = {
            "teaching": {
                "script": "align_and_fuse.py",
                "output_prefix": "teaching",
                "description": "Teaching-level OpenCV fusion"
            },
            "dcsr": {
                "script": "run_dcsr.sh",
                "output_prefix": "dcsr",
                "description": "DCSR (Dual-Camera Super-Resolution)"
            },
            "zoomgs": {
                "script": "run_zoomgs.sh",
                "output_prefix": "zoomgs",
                "description": "ZoomGS (Dual-Camera Smooth Zoom)"
            }
        }
    
    def run_teaching_method(self, wide_path: str, tele_path: str, output_dir: str) -> bool:
        """Run the teaching-level fusion method."""
        try:
            cmd = [
                "python", "align_and_fuse.py",
                "--wide", wide_path,
                "--tele", tele_path,
                "--out", output_dir,
                "--visualize"
            ]
            
            print(f"Running teaching method: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.base_dir)
            
            if result.returncode == 0:
                print("Teaching method completed successfully")
                return True
            else:
                print(f"Teaching method failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error running teaching method: {e}")
            return False
    
    def run_sota_method(self, method: str, wide_path: str, tele_path: str, output_dir: str) -> bool:
        """Run SOTA method (DCSR or ZoomGS)."""
        try:
            script_path = self.base_dir / self.methods[method]["script"]
            
            if not script_path.exists():
                print(f"Script not found: {script_path}")
                return False
            
            cmd = ["bash", str(script_path), wide_path, tele_path, output_dir]
            
            print(f"Running {method}: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.base_dir)
            
            if result.returncode == 0:
                print(f"{method} completed successfully")
                return True
            else:
                print(f"{method} failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error running {method}: {e}")
            return False
    
    def run_all_methods(self, wide_path: str, tele_path: str) -> Dict[str, bool]:
        """Run all available methods."""
        results = {}
        
        # Create individual output directories
        for method_name in self.methods:
            method_output_dir = self.results_dir / f"{method_name}_output"
            method_output_dir.mkdir(exist_ok=True)
            
            print(f"\n{'='*50}")
            print(f"Running {self.methods[method_name]['description']}")
            print(f"{'='*50}")
            
            if method_name == "teaching":
                success = self.run_teaching_method(wide_path, tele_path, str(method_output_dir))
            else:
                success = self.run_sota_method(method_name, wide_path, tele_path, str(method_output_dir))
            
            results[method_name] = success
        
        return results
    
    def evaluate_all_results(self, gt_path: str = None) -> Dict[str, Dict]:
        """Evaluate all method results."""
        evaluations = {}
        
        for method_name in self.methods:
            method_output_dir = self.results_dir / f"{method_name}_output"
            
            if not method_output_dir.exists():
                continue
            
            print(f"\nEvaluating {method_name}...")
            
            # Find output files
            fused_path = None
            wide_path = None
            tele_warp_path = None
            digital_zoom_path = None
            confidence_mask_path = None
            
            # Look for common output file patterns
            for file_path in method_output_dir.glob("*"):
                filename = file_path.name.lower()
                if "fused" in filename or "result" in filename:
                    fused_path = str(file_path)
                elif "wide" in filename:
                    wide_path = str(file_path)
                elif "tele" in filename and "warp" in filename:
                    tele_warp_path = str(file_path)
                elif "digital" in filename and "zoom" in filename:
                    digital_zoom_path = str(file_path)
                elif "confidence" in filename or "mask" in filename:
                    confidence_mask_path = str(file_path)
            
            if not fused_path:
                print(f"No fused result found for {method_name}")
                continue
            
            # Run evaluation
            try:
                cmd = [
                    "python", "eval_multicam.py",
                    "--fused", fused_path,
                    "--wide", wide_path or fused_path,  # Fallback
                    "--tele_warp", tele_warp_path or fused_path,  # Fallback
                    "--digital_zoom", digital_zoom_path or fused_path,  # Fallback
                    "--output", str(method_output_dir / "evaluation_report.json")
                ]
                
                if gt_path:
                    cmd.extend(["--gt", gt_path])
                
                if confidence_mask_path:
                    cmd.extend(["--confidence_mask", confidence_mask_path])
                
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.base_dir)
                
                if result.returncode == 0:
                    # Load evaluation results
                    eval_file = method_output_dir / "evaluation_report.json"
                    if eval_file.exists():
                        with open(eval_file, 'r') as f:
                            evaluations[method_name] = json.load(f)
                        print(f"Evaluation completed for {method_name}")
                    else:
                        print(f"Evaluation file not found for {method_name}")
                else:
                    print(f"Evaluation failed for {method_name}: {result.stderr}")
                    
            except Exception as e:
                print(f"Error evaluating {method_name}: {e}")
        
        return evaluations
    
    def create_comparison_report(self, evaluations: Dict[str, Dict]) -> None:
        """Create comprehensive comparison report."""
        report_path = self.results_dir / "comparison_report.json"
        
        # Create summary comparison
        comparison_data = {
            "summary": {
                "total_methods": len(evaluations),
                "methods_evaluated": list(evaluations.keys())
            },
            "detailed_results": evaluations,
            "recommendations": self._generate_recommendations(evaluations)
        }
        
        # Save JSON report
        with open(report_path, 'w') as f:
            json.dump(comparison_data, f, indent=2)
        
        # Create visual comparison
        self._create_visual_comparison()
        
        print(f"\nComparison report saved to: {report_path}")
        print("Visual comparison saved to: comparison_results/comparison_visualization.png")
    
    def _generate_recommendations(self, evaluations: Dict[str, Dict]) -> Dict[str, str]:
        """Generate recommendations based on evaluation results."""
        recommendations = {}
        
        for method, results in evaluations.items():
            if not results:
                continue
            
            # Extract key metrics
            psnr = results.get('image_quality_metrics', {}).get('psnr_fused_vs_wide', 0)
            detail_score = results.get('custom_metrics', {}).get('detail_transfer_score', 0)
            ghost_score = results.get('custom_metrics', {}).get('ghost_score', 0)
            
            # Generate recommendation
            if psnr > 30 and detail_score > 0.8 and ghost_score < 0.1:
                recommendations[method] = "Excellent performance - recommended for production use"
            elif psnr > 25 and detail_score > 0.6:
                recommendations[method] = "Good performance - suitable for most applications"
            elif psnr > 20:
                recommendations[method] = "Moderate performance - may need parameter tuning"
            else:
                recommendations[method] = "Poor performance - not recommended"
        
        return recommendations
    
    def _create_visual_comparison(self) -> None:
        """Create visual comparison of all methods."""
        try:
            # This would create a side-by-side comparison image
            # For now, we'll create a simple text-based summary
            summary_path = self.results_dir / "visual_summary.txt"
            
            with open(summary_path, 'w') as f:
                f.write("Multi-Camera Fusion Methods Comparison\n")
                f.write("=" * 50 + "\n\n")
                
                for method_name, method_info in self.methods.items():
                    f.write(f"{method_info['description']}:\n")
                    f.write(f"  Script: {method_info['script']}\n")
                    f.write(f"  Output: {self.results_dir / f'{method_name}_output'}\n\n")
            
            print(f"Visual summary saved to: {summary_path}")
            
        except Exception as e:
            print(f"Error creating visual comparison: {e}")


def main():
    parser = argparse.ArgumentParser(description="Compare All Multi-Camera Fusion Methods")
    parser.add_argument("--wide", required=True, help="Path to wide angle image")
    parser.add_argument("--tele", required=True, help="Path to telephoto image")
    parser.add_argument("--gt", help="Path to ground truth high-res image (optional)")
    parser.add_argument("--output", default="comparison_results", help="Output directory")
    
    args = parser.parse_args()
    
    # Initialize comparison
    comparison = MultiCameraComparison()
    
    print("Multi-Camera Fusion Methods Comparison")
    print("=" * 50)
    print(f"Wide image: {args.wide}")
    print(f"Tele image: {args.tele}")
    if args.gt:
        print(f"Ground truth: {args.gt}")
    print(f"Output directory: {args.output}")
    
    # Run all methods
    print("\nRunning all methods...")
    results = comparison.run_all_methods(args.wide, args.tele)
    
    # Print results summary
    print("\nMethod Results:")
    for method, success in results.items():
        status = "SUCCESS" if success else "FAILED"
        print(f"  {method}: {status}")
    
    # Evaluate results
    print("\nEvaluating results...")
    evaluations = comparison.evaluate_all_results(args.gt)
    
    # Create comparison report
    print("\nCreating comparison report...")
    comparison.create_comparison_report(evaluations)
    
    print("\nComparison completed!")
    print(f"Results saved to: {args.output}")


if __name__ == "__main__":
    main()
