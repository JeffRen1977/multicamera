#!/usr/bin/env python3
"""
example_step_by_step.py
Step-by-step tutorial showing each stage of the multi-camera fusion algorithm.
This script saves intermediate results at each step for educational purposes.
"""

import cv2
import numpy as np
from align_and_fuse import (
    read_image, to_bgr_uint8, compute_homography,
    warp_image, extract_highpass, compute_confidence_mask,
    fuse
)


def visualize_frequencies(img, low, high, output_path):
    """Visualize frequency decomposition."""
    # Normalize high-frequency for visualization
    high_vis = (high + 0.5).clip(0, 1)
    
    # Create composite
    composite = np.hstack([img, low, high_vis])
    
    cv2.imwrite(output_path, to_bgr_uint8(composite))
    print(f"  Saved: {output_path} (Original | Low-freq | High-freq)")


def main(wide_path, tele_path, output_dir):
    """Run step-by-step tutorial."""
    os.makedirs(output_dir, exist_ok=True)
    
    print("="*60)
    print("Multi-Camera Fusion - Step-by-Step Tutorial")
    print("="*60)
    print()
    
    # Load images
    print("Loading images...")
    img_wide = read_image(wide_path)
    img_tele = read_image(tele_path)
    print(f"  Wide: {img_wide.shape}")
    print(f"  Tele: {img_tele.shape}")
    print()
    
    # Step 1-3: Feature Detection, Matching, and Homography
    print("Steps 1-3: Feature Detection, Matching, and Homography Estimation")
    print("-" * 60)
    H, mask = compute_homography(img_wide, img_tele, visualize=True)
    
    # Copy match visualization if it exists
    if os.path.exists("match_vis.jpg"):
        import shutil
        shutil.copy("match_vis.jpg", os.path.join(output_dir, "step2_matches.png"))
        print(f"  Saved: {os.path.join(output_dir, 'step2_matches.png')}")
    
    print(f"  Homography matrix H:")
    print(f"  {H}")
    print()
    
    # Visualize alignment
    h, w = img_wide.shape[:2]
    corners = np.array([[0, 0], [w, 0], [w, h], [0, h]], dtype=np.float32)
    corners_warped = cv2.perspectiveTransform(
        corners.reshape(-1, 1, 2), H
    ).reshape(-1, 2)
    
    img_wide_vis = (img_wide * 255).astype(np.uint8)
    img_wide_bgr = cv2.cvtColor(img_wide_vis, cv2.COLOR_RGB2BGR)
    cv2.polylines(img_wide_bgr, [corners_warped.astype(np.int32)], True, (0, 255, 0), 2)
    cv2.imwrite(os.path.join(output_dir, "step3_alignment.png"), img_wide_bgr)
    print(f"  Saved: {os.path.join(output_dir, 'step3_alignment.png')}")
    print()
    
    # Step 4: Image Warping
    print("Step 4: Image Warping")
    print("-" * 60)
    img_tele_warped = warp_image(img_tele, H, img_wide.shape)
    cv2.imwrite(os.path.join(output_dir, "step4_tele_warped.png"),
                to_bgr_uint8(img_tele_warped))
    print(f"  Saved: {os.path.join(output_dir, 'step4_tele_warped.png')}")
    print()
    
    # Step 5: Frequency Decomposition
    print("Step 5: Frequency Decomposition")
    print("-" * 60)
    low_wide, high_wide = extract_highpass(img_wide, sigma=5.0)
    low_tele, high_tele = extract_highpass(img_tele_warped, sigma=5.0)
    
    visualize_frequencies(img_wide, low_wide, high_wide,
                         os.path.join(output_dir, "step5_wide_frequencies.png"))
    visualize_frequencies(img_tele_warped, low_tele, high_tele,
                         os.path.join(output_dir, "step5_tele_frequencies.png"))
    print()
    
    # Step 6: Confidence Computation
    print("Step 6: Confidence Computation")
    print("-" * 60)
    confidence = compute_confidence_mask(img_wide, img_tele_warped, thresh=0.08)
    
    # Save confidence map
    conf_vis = (confidence[:, :, 0] * 255).astype(np.uint8)
    cv2.imwrite(os.path.join(output_dir, "step6_confidence.png"), conf_vis)
    print(f"  Saved: {os.path.join(output_dir, 'step6_confidence.png')}")
    print(f"  Mean confidence: {confidence.mean():.3f}")
    print(f"  High confidence (>0.8): {(confidence > 0.8).mean()*100:.1f}%")
    print()
    
    # Step 7: Fusion
    print("Step 7: Frequency-Domain Fusion")
    print("-" * 60)
    fused, _ = fuse(img_wide, img_tele_warped, alpha=1.0)
    
    cv2.imwrite(os.path.join(output_dir, "step7_fused.png"),
                to_bgr_uint8(fused))
    print(f"  Saved: {os.path.join(output_dir, 'step7_fused.png')}")
    print()
    
    # Create final comparison
    print("Creating final comparison...")
    digital_zoom = cv2.resize(
        img_wide[:, img_wide.shape[1]//4:3*img_wide.shape[1]//4, :],
        (img_wide.shape[1], img_wide.shape[0]),
        interpolation=cv2.INTER_CUBIC
    )
    
    composite = np.hstack([
        img_wide,
        digital_zoom,
        fused,
        img_tele_warped
    ])
    
    cv2.imwrite(os.path.join(output_dir, "final_comparison.png"),
                to_bgr_uint8(composite))
    print(f"  Saved: {os.path.join(output_dir, 'final_comparison.png')}")
    print()
    
    print("="*60)
    print("Tutorial completed!")
    print(f"All intermediate results saved to: {output_dir}")
    print("="*60)
    print()
    print("Files created:")
    print("  step2_matches.png - Feature matches")
    print("  step3_alignment.png - Alignment visualization")
    print("  step4_tele_warped.png - Warped telephoto")
    print("  step5_*_frequencies.png - Frequency decomposition")
    print("  step6_confidence.png - Confidence map")
    print("  step7_fused.png - Final fusion result")
    print("  final_comparison.png - Side-by-side comparison")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Step-by-step tutorial for multi-camera fusion"
    )
    parser.add_argument(
        "--wide", required=True,
        help="Path to wide-angle image"
    )
    parser.add_argument(
        "--tele", required=True,
        help="Path to telephoto image"
    )
    parser.add_argument(
        "--out", default="../results/tutorial",
        help="Output directory for intermediate results"
    )
    
    args = parser.parse_args()
    main(args.wide, args.tele, args.out)

