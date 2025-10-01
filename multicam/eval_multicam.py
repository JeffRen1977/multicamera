#!/usr/bin/env python3
"""
eval_multicam.py
Comprehensive evaluation script for multi-camera fusion results.
Computes PSNR, SSIM, LPIPS, Detail Transfer Score, and Ghost Score.
"""

import cv2
import numpy as np
import os
import argparse
from typing import Dict, Tuple, Optional
import json
import csv
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
import lpips
import torch
from scipy import ndimage
import matplotlib.pyplot as plt


class MultiCameraEvaluator:
    """Evaluator for multi-camera fusion results."""
    
    def __init__(self, device: str = 'cuda' if torch.cuda.is_available() else 'cpu'):
        """Initialize evaluator with LPIPS model."""
        self.device = device
        self.lpips_model = lpips.LPIPS(net='alex').to(device)
        print(f"Using device: {device}")
    
    def read_image(self, path: str) -> np.ndarray:
        """Read image and convert to RGB float format."""
        im = cv2.imread(path, cv2.IMREAD_COLOR)
        if im is None:
            raise ValueError(f"Failed to read: {path}")
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        return im
    
    def compute_psnr(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """Compute Peak Signal-to-Noise Ratio."""
        return psnr(img1, img2, data_range=1.0)
    
    def compute_ssim(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """Compute Structural Similarity Index."""
        return ssim(img1, img2, multichannel=True, channel_axis=2, data_range=1.0)
    
    def compute_lpips(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """Compute Learned Perceptual Image Patch Similarity."""
        # Convert to tensor format expected by LPIPS
        img1_tensor = torch.from_numpy(img1).permute(2, 0, 1).unsqueeze(0).to(self.device)
        img2_tensor = torch.from_numpy(img2).permute(2, 0, 1).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            lpips_score = self.lpips_model(img1_tensor, img2_tensor)
        
        return lpips_score.item()
    
    def extract_high_frequency(self, img: np.ndarray, sigma: float = 1.0) -> np.ndarray:
        """Extract high-frequency components using Laplacian."""
        gray = cv2.cvtColor((img * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        return np.abs(laplacian)
    
    def compute_detail_transfer_score(self, fused: np.ndarray, tele_warp: np.ndarray, 
                                    wide: np.ndarray, mask: Optional[np.ndarray] = None) -> float:
        """
        Compute Detail Transfer Score: ratio of high-frequency energy preserved from tele.
        
        Args:
            fused: Fused image
            tele_warp: Warped telephoto image
            wide: Wide angle image
            mask: Optional mask for region of interest
            
        Returns:
            Detail transfer score (higher is better)
        """
        # Extract high-frequency components
        hf_fused = self.extract_high_frequency(fused)
        hf_tele = self.extract_high_frequency(tele_warp)
        hf_wide = self.extract_high_frequency(wide)
        
        if mask is not None:
            if mask.ndim == 3:
                mask = mask[:, :, 0]
            hf_fused = hf_fused * mask
            hf_tele = hf_tele * mask
            hf_wide = hf_wide * mask
        
        # Compute energy ratios
        tele_energy = np.sum(hf_tele)
        wide_energy = np.sum(hf_wide)
        fused_energy = np.sum(hf_fused)
        
        if tele_energy == 0:
            return 0.0
        
        # Detail transfer score: how much tele detail is preserved
        detail_score = fused_energy / tele_energy if tele_energy > 0 else 0.0
        
        return detail_score
    
    def compute_ghost_score(self, fused: np.ndarray, wide: np.ndarray, 
                          tele_warp: np.ndarray, thresh: float = 0.1) -> float:
        """
        Compute Ghost Score: measure of artifacts introduced by tele details.
        
        Args:
            fused: Fused image
            wide: Wide angle image
            tele_warp: Warped telephoto image
            thresh: Threshold for detecting inconsistent regions
            
        Returns:
            Ghost score (lower is better)
        """
        # Find regions where tele and wide differ significantly
        diff = np.mean(np.abs(wide - tele_warp), axis=2)
        inconsistent_mask = diff > thresh
        
        if np.sum(inconsistent_mask) == 0:
            return 0.0
        
        # In inconsistent regions, measure how much fused differs from wide
        fused_diff = np.mean(np.abs(fused - wide), axis=2)
        ghost_score = np.mean(fused_diff[inconsistent_mask])
        
        return ghost_score
    
    def compute_alignment_quality(self, wide: np.ndarray, tele_warp: np.ndarray) -> float:
        """
        Compute alignment quality based on feature matching consistency.
        
        Args:
            wide: Wide angle image
            tele_warp: Warped telephoto image
            
        Returns:
            Alignment quality score (higher is better)
        """
        # Convert to grayscale for feature detection
        gray1 = cv2.cvtColor((wide * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
        gray2 = cv2.cvtColor((tele_warp * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
        
        # Detect corners
        corners1 = cv2.goodFeaturesToTrack(gray1, maxCorners=100, qualityLevel=0.01, minDistance=10)
        corners2 = cv2.goodFeaturesToTrack(gray2, maxCorners=100, qualityLevel=0.01, minDistance=10)
        
        if corners1 is None or corners2 is None:
            return 0.0
        
        # Track features using optical flow
        lk_params = dict(winSize=(15, 15), maxLevel=2, 
                        criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        
        p1, st, err = cv2.calcOpticalFlowPyrLK(gray1, gray2, corners1, None, **lk_params)
        
        if p1 is None:
            return 0.0
        
        # Compute alignment error
        good_points = st == 1
        if np.sum(good_points) == 0:
            return 0.0
        
        error = np.mean(err[good_points])
        alignment_score = 1.0 / (1.0 + error / 10.0)  # Normalize to [0, 1]
        
        return alignment_score
    
    def evaluate_all(self, fused_path: str, wide_path: str, tele_warp_path: str, 
                    digital_zoom_path: str, gt_path: Optional[str] = None,
                    confidence_mask_path: Optional[str] = None) -> Dict[str, float]:
        """
        Evaluate all metrics for multi-camera fusion results.
        
        Args:
            fused_path: Path to fused image
            wide_path: Path to wide angle image
            tele_warp_path: Path to warped telephoto image
            digital_zoom_path: Path to digital zoom baseline
            gt_path: Optional path to ground truth high-res image
            confidence_mask_path: Optional path to confidence mask
            
        Returns:
            Dictionary of evaluation metrics
        """
        print("Loading images...")
        fused = self.read_image(fused_path)
        wide = self.read_image(wide_path)
        tele_warp = self.read_image(tele_warp_path)
        digital_zoom = self.read_image(digital_zoom_path)
        
        confidence_mask = None
        if confidence_mask_path and os.path.exists(confidence_mask_path):
            confidence_mask = cv2.imread(confidence_mask_path, cv2.IMREAD_GRAYSCALE)
            confidence_mask = confidence_mask.astype(np.float32) / 255.0
        
        results = {}
        
        print("Computing basic metrics...")
        # Basic image quality metrics
        results['psnr_fused_vs_wide'] = self.compute_psnr(fused, wide)
        results['ssim_fused_vs_wide'] = self.compute_ssim(fused, wide)
        results['lpips_fused_vs_wide'] = self.compute_lpips(fused, wide)
        
        results['psnr_dz_vs_wide'] = self.compute_psnr(digital_zoom, wide)
        results['ssim_dz_vs_wide'] = self.compute_ssim(digital_zoom, wide)
        results['lpips_dz_vs_wide'] = self.compute_lpips(digital_zoom, wide)
        
        print("Computing custom metrics...")
        # Custom multi-camera metrics
        results['detail_transfer_score'] = self.compute_detail_transfer_score(
            fused, tele_warp, wide, confidence_mask)
        results['ghost_score'] = self.compute_ghost_score(fused, wide, tele_warp)
        results['alignment_quality'] = self.compute_alignment_quality(wide, tele_warp)
        
        # Compare with ground truth if available
        if gt_path and os.path.exists(gt_path):
            print("Computing ground truth metrics...")
            gt = self.read_image(gt_path)
            # Resize GT to match fused image
            gt_resized = cv2.resize(gt, (fused.shape[1], fused.shape[0]))
            
            results['psnr_fused_vs_gt'] = self.compute_psnr(fused, gt_resized)
            results['ssim_fused_vs_gt'] = self.compute_ssim(fused, gt_resized)
            results['lpips_fused_vs_gt'] = self.compute_lpips(fused, gt_resized)
            
            results['psnr_dz_vs_gt'] = self.compute_psnr(digital_zoom, gt_resized)
            results['ssim_dz_vs_gt'] = self.compute_ssim(digital_zoom, gt_resized)
            results['lpips_dz_vs_gt'] = self.compute_lpips(digital_zoom, gt_resized)
        
        return results
    
    def create_evaluation_report(self, results: Dict[str, float], output_path: str):
        """Create a comprehensive evaluation report."""
        # Convert numpy types to Python native types
        def convert_to_native(value):
            if hasattr(value, 'item'):
                return float(value.item())
            return float(value) if value else 0.0
        
        report = {
            'summary': {
                'method': 'Multi-Camera Fusion Evaluation',
                'metrics_computed': len(results)
            },
            'image_quality_metrics': {
                'psnr_fused_vs_wide': convert_to_native(results.get('psnr_fused_vs_wide', 0)),
                'ssim_fused_vs_wide': convert_to_native(results.get('ssim_fused_vs_wide', 0)),
                'lpips_fused_vs_wide': convert_to_native(results.get('lpips_fused_vs_wide', 0)),
                'psnr_dz_vs_wide': convert_to_native(results.get('psnr_dz_vs_wide', 0)),
                'ssim_dz_vs_wide': convert_to_native(results.get('ssim_dz_vs_wide', 0)),
                'lpips_dz_vs_wide': convert_to_native(results.get('lpips_dz_vs_wide', 0))
            },
            'custom_metrics': {
                'detail_transfer_score': convert_to_native(results.get('detail_transfer_score', 0)),
                'ghost_score': convert_to_native(results.get('ghost_score', 0)),
                'alignment_quality': convert_to_native(results.get('alignment_quality', 0))
            }
        }
        
        if 'psnr_fused_vs_gt' in results:
            report['ground_truth_comparison'] = {
                'psnr_fused_vs_gt': convert_to_native(results.get('psnr_fused_vs_gt', 0)),
                'ssim_fused_vs_gt': convert_to_native(results.get('ssim_fused_vs_gt', 0)),
                'lpips_fused_vs_gt': convert_to_native(results.get('lpips_fused_vs_gt', 0)),
                'psnr_dz_vs_gt': convert_to_native(results.get('psnr_dz_vs_gt', 0)),
                'ssim_dz_vs_gt': convert_to_native(results.get('ssim_dz_vs_gt', 0)),
                'lpips_dz_vs_gt': convert_to_native(results.get('lpips_dz_vs_gt', 0))
            }
        
        # Save JSON report
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Evaluation report saved to {output_path}")
        return report


def main():
    parser = argparse.ArgumentParser(description="Evaluate Multi-Camera Fusion Results")
    parser.add_argument("--fused", required=True, help="Path to fused image")
    parser.add_argument("--wide", required=True, help="Path to wide angle image")
    parser.add_argument("--tele_warp", required=True, help="Path to warped telephoto image")
    parser.add_argument("--digital_zoom", required=True, help="Path to digital zoom baseline")
    parser.add_argument("--gt", help="Path to ground truth high-res image (optional)")
    parser.add_argument("--confidence_mask", help="Path to confidence mask (optional)")
    parser.add_argument("--output", default="evaluation_report.json", help="Output report path")
    parser.add_argument("--csv", help="Also save results as CSV")
    
    args = parser.parse_args()
    
    evaluator = MultiCameraEvaluator()
    
    print("Starting evaluation...")
    results = evaluator.evaluate_all(
        args.fused, args.wide, args.tele_warp, args.digital_zoom,
        args.gt, args.confidence_mask
    )
    
    # Create and save report
    report = evaluator.create_evaluation_report(results, args.output)
    
    # Print summary
    print("\n" + "="*50)
    print("EVALUATION SUMMARY")
    print("="*50)
    print(f"PSNR (Fused vs Wide): {results.get('psnr_fused_vs_wide', 0):.2f} dB")
    print(f"SSIM (Fused vs Wide): {results.get('ssim_fused_vs_wide', 0):.4f}")
    print(f"LPIPS (Fused vs Wide): {results.get('lpips_fused_vs_wide', 0):.4f}")
    print(f"Detail Transfer Score: {results.get('detail_transfer_score', 0):.4f}")
    print(f"Ghost Score: {results.get('ghost_score', 0):.4f}")
    print(f"Alignment Quality: {results.get('alignment_quality', 0):.4f}")
    
    if 'psnr_fused_vs_gt' in results:
        print(f"\nGround Truth Comparison:")
        print(f"PSNR (Fused vs GT): {results.get('psnr_fused_vs_gt', 0):.2f} dB")
        print(f"SSIM (Fused vs GT): {results.get('ssim_fused_vs_gt', 0):.4f}")
        print(f"LPIPS (Fused vs GT): {results.get('lpips_fused_vs_gt', 0):.4f}")
    
    # Save CSV if requested
    if args.csv:
        with open(args.csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Metric', 'Value'])
            for key, value in results.items():
                writer.writerow([key, value])
        print(f"\nCSV results saved to {args.csv}")


if __name__ == "__main__":
    main()



