#!/usr/bin/env python3
"""
align_and_fuse.py
Teaching-level multi-camera fusion (Wide + Tele -> hybrid zoom)
Input: wide.jpg, tele.jpg
Output: fused.png, digital_zoom.png, composite.png
Dependencies: opencv-python, numpy, skimage
"""

import cv2
import numpy as np
from skimage import img_as_float
import os
import argparse
from typing import Tuple, Optional
import matplotlib.pyplot as plt


def read_image(path: str) -> np.ndarray:
    """Read image and convert to RGB float format."""
    im = cv2.imread(path, cv2.IMREAD_COLOR)  # BGR
    if im is None:
        raise ValueError(f"Failed to read: {path}")
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    return im


def to_bgr_uint8(im: np.ndarray) -> np.ndarray:
    """Convert RGB float image to BGR uint8 for OpenCV saving."""
    im = np.clip(im * 255.0, 0, 255).astype(np.uint8)
    return cv2.cvtColor(im, cv2.COLOR_RGB2BGR)


def compute_homography(wide: np.ndarray, tele: np.ndarray, visualize: bool = False) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute homography between wide and tele images using SIFT features.
    
    Args:
        wide: Wide angle image (RGB float)
        tele: Telephoto image (RGB float)
        visualize: Whether to save visualization of matches
        
    Returns:
        H: Homography matrix (3x3)
        mask: Inlier mask from RANSAC
    """
    # Convert to uint8 for feature detection
    wide_uint8 = (wide * 255).astype(np.uint8)
    tele_uint8 = (tele * 255).astype(np.uint8)
    
    # SIFT keypoints + BF matcher
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(wide_uint8, None)
    kp2, des2 = sift.detectAndCompute(tele_uint8, None)
    
    if des1 is None or des2 is None:
        raise RuntimeError("No features found.")
    
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    
    # Apply Lowe's ratio test
    good = []
    pts1 = []
    pts2 = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)
            pts1.append(kp1[m.queryIdx].pt)
            pts2.append(kp2[m.trainIdx].pt)
    
    if len(pts1) < 6:
        raise RuntimeError(f"Not enough matches: {len(pts1)}")
    
    pts1 = np.array(pts1)
    pts2 = np.array(pts2)
    
    # Compute homography: map tele -> wide
    H, mask = cv2.findHomography(pts2, pts1, cv2.RANSAC, 4.0)
    
    if visualize:
        vis = cv2.drawMatches(
            cv2.cvtColor(wide_uint8, cv2.COLOR_RGB2BGR),
            kp1,
            cv2.cvtColor(tele_uint8, cv2.COLOR_RGB2BGR),
            kp2,
            good,
            None,
            flags=2
        )
        cv2.imwrite("match_vis.jpg", vis)
        print(f"Found {len(good)} matches, saved visualization to match_vis.jpg")
    
    return H, mask


def warp_image(im: np.ndarray, H: np.ndarray, target_shape: Tuple[int, int]) -> np.ndarray:
    """
    Warp image using homography matrix.
    
    Args:
        im: Input image (RGB float)
        H: Homography matrix (3x3)
        target_shape: Target output shape (height, width)
        
    Returns:
        Warped image (RGB float)
    """
    h, w = target_shape[:2]
    im_warp = cv2.warpPerspective((im * 255).astype(np.uint8), H, (w, h))
    im_warp = cv2.cvtColor(im_warp, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    return im_warp


def extract_highpass(im: np.ndarray, sigma: float = 3.0) -> Tuple[np.ndarray, np.ndarray]:
    """
    Extract high-frequency components using Gaussian blur.
    
    Args:
        im: Input image (RGB float)
        sigma: Gaussian blur sigma
        
    Returns:
        low: Low-frequency components
        high: High-frequency components
    """
    # highpass = im - lowpass(Gaussian)
    low = cv2.GaussianBlur(im, (0, 0), sigmaX=sigma, sigmaY=sigma)
    high = im - low
    return low, high


def compute_confidence_mask(wide: np.ndarray, tele_warp: np.ndarray, thresh: float = 0.08) -> np.ndarray:
    """
    Compute confidence mask based on photometric similarity.
    
    Args:
        wide: Wide angle image (RGB float)
        tele_warp: Warped telephoto image (RGB float)
        thresh: Photometric difference threshold
        
    Returns:
        Confidence mask (H, W, 1)
    """
    # Confidence based on photometric similarity and non-blank pixels
    diff = np.mean(np.abs(wide - tele_warp), axis=2)
    mask = (diff < thresh).astype(np.float32)
    
    # Also blank regions where warp produced zeros (black)
    blank = np.mean(tele_warp, axis=2) < 1e-3
    mask[blank] = 0.0
    
    # Smooth mask
    mask = cv2.GaussianBlur(mask, (0, 0), sigmaX=3)
    mask = np.expand_dims(mask, axis=2)
    return mask


def fuse(wide: np.ndarray, tele_warp: np.ndarray, alpha: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
    """
    Fuse wide and tele images using multi-scale approach.
    
    Args:
        wide: Wide angle image (RGB float)
        tele_warp: Warped telephoto image (RGB float)
        alpha: Fusion strength parameter
        
    Returns:
        fused: Fused image (RGB float)
        conf: Confidence mask (H, W, 1)
    """
    # Multi-scale fusion: lowfreq = wide lowpass; highfreq from tele_warp masked by confidence
    low_w, high_w = extract_highpass(wide, sigma=5)
    low_t, high_t = extract_highpass(tele_warp, sigma=5)
    conf = compute_confidence_mask(wide, tele_warp, thresh=0.08)
    
    # Cross-fade: result = low_w + masked_high_t + (1-mask)*high_w*attenuate
    fused = low_w + conf * high_t * alpha + (1.0 - conf) * high_w * 0.6
    fused = np.clip(fused, 0.0, 1.0)
    
    return fused, conf


def digital_zoom(wide: np.ndarray, scale: float = 2.0) -> np.ndarray:
    """
    Create digital zoom by cropping and upscaling center region.
    
    Args:
        wide: Wide angle image (RGB float)
        scale: Zoom scale factor
        
    Returns:
        Digitally zoomed image (RGB float)
    """
    h, w, _ = wide.shape
    ch, cw = int(h / scale), int(w / scale)
    cy, cx = h // 2, w // 2
    
    crop = wide[cy - ch // 2:cy + ch // 2, cx - cw // 2:cx + cw // 2, :]
    zoom = cv2.resize((crop * 255).astype(np.uint8), (w, h), interpolation=cv2.INTER_CUBIC)
    zoom = cv2.cvtColor(zoom, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    
    return zoom


def create_composite(wide: np.ndarray, digital_zoom: np.ndarray, fused: np.ndarray, tele_warp: np.ndarray) -> np.ndarray:
    """Create side-by-side composite image for visualization."""
    # Add labels
    def add_label(img, label):
        img_labeled = img.copy()
        cv2.putText(img_labeled, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(img_labeled, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
        return img_labeled
    
    wide_labeled = add_label(to_bgr_uint8(wide), "Wide")
    dz_labeled = add_label(to_bgr_uint8(digital_zoom), "Digital Zoom")
    fused_labeled = add_label(to_bgr_uint8(fused), "Fused")
    tele_labeled = add_label(to_bgr_uint8(tele_warp), "Tele Warped")
    
    # Create horizontal composite
    composite = np.hstack([wide_labeled, dz_labeled, fused_labeled, tele_labeled])
    return composite


def main(wide_path: str, tele_path: str, out_dir: str = "results", visualize: bool = False, alpha: float = 1.0):
    """
    Main function to perform dual-camera fusion.
    
    Args:
        wide_path: Path to wide angle image
        tele_path: Path to telephoto image
        out_dir: Output directory
        visualize: Whether to save intermediate visualizations
        alpha: Fusion strength parameter
    """
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"Loading images: {wide_path}, {tele_path}")
    wide = read_image(wide_path)
    tele = read_image(tele_path)
    
    print("Computing homography...")
    H, mask = compute_homography(wide, tele, visualize=visualize)
    
    print("Warping telephoto image...")
    tele_warp = warp_image(tele, H, wide.shape)
    
    print("Fusing images...")
    fused, conf = fuse(wide, tele_warp, alpha=alpha)
    
    print("Creating digital zoom baseline...")
    dz = digital_zoom(wide, scale=2.0)
    
    # Save outputs
    print("Saving results...")
    cv2.imwrite(os.path.join(out_dir, "wide.png"), to_bgr_uint8(wide))
    cv2.imwrite(os.path.join(out_dir, "tele_warp.png"), to_bgr_uint8(tele_warp))
    cv2.imwrite(os.path.join(out_dir, "fused.png"), to_bgr_uint8(fused))
    cv2.imwrite(os.path.join(out_dir, "digital_zoom.png"), to_bgr_uint8(dz))
    cv2.imwrite(os.path.join(out_dir, "confidence_mask.png"), (conf * 255).astype(np.uint8))
    
    # Create composite for comparison
    composite = create_composite(wide, dz, fused, tele_warp)
    cv2.imwrite(os.path.join(out_dir, "composite.png"), composite)
    
    print(f"Saved outputs to {out_dir}")
    print("Files created:")
    print("  - wide.png: Original wide angle image")
    print("  - tele_warp.png: Warped telephoto image")
    print("  - fused.png: Multi-camera fusion result")
    print("  - digital_zoom.png: Digital zoom baseline")
    print("  - confidence_mask.png: Fusion confidence mask")
    print("  - composite.png: Side-by-side comparison")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dual-Camera Fusion for Hybrid Zoom")
    parser.add_argument("--wide", required=True, help="Path to wide angle image")
    parser.add_argument("--tele", required=True, help="Path to telephoto image")
    parser.add_argument("--out", default="results", help="Output directory")
    parser.add_argument("--visualize", action="store_true", help="Save intermediate visualizations")
    parser.add_argument("--alpha", type=float, default=1.0, help="Fusion strength parameter")
    
    args = parser.parse_args()
    main(args.wide, args.tele, out_dir=args.out, visualize=args.visualize, alpha=args.alpha)



