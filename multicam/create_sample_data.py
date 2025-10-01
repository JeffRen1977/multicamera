#!/usr/bin/env python3
"""
create_sample_data.py
Create sample dual-camera data for testing multi-camera fusion methods.
This script generates synthetic wide and telephoto image pairs for demonstration.
"""

import cv2
import numpy as np
import os
import argparse
from pathlib import Path
import matplotlib.pyplot as plt
from skimage import data, transform, filters
from skimage.color import rgb2gray, gray2rgb


def create_synthetic_scene() -> np.ndarray:
    """Create a synthetic scene with various textures and objects."""
    # Create a base image with different regions
    img = np.zeros((800, 1200, 3), dtype=np.float32)
    
    # Add background gradient
    for i in range(800):
        for j in range(1200):
            img[i, j] = [0.3 + 0.2 * i / 800, 0.4 + 0.3 * j / 1200, 0.5 + 0.1 * (i + j) / 2000]
    
    # Add some geometric shapes
    cv2.circle(img, (300, 200), 80, (0.8, 0.2, 0.2), -1)
    cv2.rectangle(img, (600, 150), (800, 350), (0.2, 0.8, 0.2), -1)
    cv2.ellipse(img, (1000, 250), (120, 80), 45, 0, 360, (0.2, 0.2, 0.8), -1)
    
    # Add text
    cv2.putText(img, "DUAL CAMERA", (400, 500), cv2.FONT_HERSHEY_SIMPLEX, 2, (1, 1, 1), 3)
    cv2.putText(img, "FUSION TEST", (400, 550), cv2.FONT_HERSHEY_SIMPLEX, 2, (1, 1, 1), 3)
    
    # Add some noise and texture
    noise = np.random.normal(0, 0.05, img.shape)
    img = np.clip(img + noise, 0, 1)
    
    # Add some high-frequency details
    details = np.random.normal(0, 0.1, img.shape)
    details = cv2.GaussianBlur(details, (3, 3), 0)
    img = np.clip(img + details, 0, 1)
    
    return img


def simulate_wide_camera(img: np.ndarray, zoom_factor: float = 1.0) -> np.ndarray:
    """Simulate wide camera capture with lower resolution and some blur."""
    h, w = img.shape[:2]
    
    # Crop center region (simulate wide FOV)
    crop_h, crop_w = int(h * 0.8), int(w * 0.8)
    start_h, start_w = (h - crop_h) // 2, (w - crop_w) // 2
    
    wide_img = img[start_h:start_h + crop_h, start_w:start_w + crop_w]
    
    # Resize to simulate lower resolution
    wide_img = cv2.resize(wide_img, (w, h))
    
    # Add slight blur to simulate wide camera characteristics
    wide_img = cv2.GaussianBlur(wide_img, (3, 3), 0)
    
    # Add slight color shift (warmer tones typical of wide cameras)
    wide_img[:, :, 0] *= 1.1  # Increase red
    wide_img[:, :, 1] *= 1.05  # Slight increase in green
    wide_img = np.clip(wide_img, 0, 1)
    
    return wide_img


def simulate_tele_camera(img: np.ndarray, zoom_factor: float = 2.0) -> np.ndarray:
    """Simulate tele camera capture with higher resolution and sharper details."""
    h, w = img.shape[:2]
    
    # Crop center region (simulate tele FOV)
    crop_h, crop_w = int(h / zoom_factor), int(w / zoom_factor)
    start_h, start_w = (h - crop_h) // 2, (w - crop_w) // 2
    
    tele_img = img[start_h:start_h + crop_h, start_w:start_w + crop_w]
    
    # Resize to original size (simulate higher resolution)
    tele_img = cv2.resize(tele_img, (w, h), interpolation=cv2.INTER_CUBIC)
    
    # Enhance details (simulate tele camera characteristics)
    # Apply unsharp masking
    blurred = cv2.GaussianBlur(tele_img, (0, 0), 2)
    tele_img = tele_img + 0.5 * (tele_img - blurred)
    tele_img = np.clip(tele_img, 0, 1)
    
    # Add slight color shift (cooler tones typical of tele cameras)
    tele_img[:, :, 2] *= 1.1  # Increase blue
    tele_img[:, :, 1] *= 1.05  # Slight increase in green
    tele_img = np.clip(tele_img, 0, 1)
    
    return tele_img


def add_camera_artifacts(img: np.ndarray, camera_type: str) -> np.ndarray:
    """Add realistic camera artifacts."""
    # Add slight vignetting
    h, w = img.shape[:2]
    center_x, center_y = w // 2, h // 2
    
    # Create vignette mask
    y, x = np.ogrid[:h, :w]
    mask = np.sqrt((x - center_x)**2 + (y - center_y)**2)
    mask = mask / mask.max()
    vignette = 1 - 0.3 * mask**2
    
    # Apply vignette
    img = img * vignette[:, :, np.newaxis]
    
    # Add slight chromatic aberration
    if camera_type == "tele":
        # Tele cameras often have more chromatic aberration
        img[:, :, 0] = cv2.GaussianBlur(img[:, :, 0], (0, 0), 0.5)  # Red channel
        img[:, :, 2] = cv2.GaussianBlur(img[:, :, 2], (0, 0), 0.5)  # Blue channel
    
    # Add slight noise
    noise = np.random.normal(0, 0.01, img.shape)
    img = np.clip(img + noise, 0, 1)
    
    return img


def create_sample_dataset(output_dir: str, num_samples: int = 5) -> None:
    """Create a sample dataset of dual-camera image pairs."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    print(f"Creating {num_samples} sample dual-camera image pairs...")
    
    for i in range(num_samples):
        print(f"Creating sample {i+1}/{num_samples}...")
        
        # Create synthetic scene
        scene = create_synthetic_scene()
        
        # Simulate wide camera
        wide_img = simulate_wide_camera(scene, zoom_factor=1.0)
        wide_img = add_camera_artifacts(wide_img, "wide")
        
        # Simulate tele camera
        tele_img = simulate_tele_camera(scene, zoom_factor=2.0)
        tele_img = add_camera_artifacts(tele_img, "tele")
        
        # Save images
        sample_dir = output_path / f"sample_{i+1:02d}"
        sample_dir.mkdir(exist_ok=True)
        
        # Convert to uint8 for saving
        wide_uint8 = (wide_img * 255).astype(np.uint8)
        tele_uint8 = (tele_img * 255).astype(np.uint8)
        scene_uint8 = (scene * 255).astype(np.uint8)
        
        # Save as BGR for OpenCV
        cv2.imwrite(str(sample_dir / "wide.jpg"), cv2.cvtColor(wide_uint8, cv2.COLOR_RGB2BGR))
        cv2.imwrite(str(sample_dir / "tele.jpg"), cv2.cvtColor(tele_uint8, cv2.COLOR_RGB2BGR))
        cv2.imwrite(str(sample_dir / "scene.jpg"), cv2.cvtColor(scene_uint8, cv2.COLOR_RGB2BGR))
        
        # Create a composite for visualization
        composite = np.hstack([wide_uint8, tele_uint8])
        cv2.imwrite(str(sample_dir / "composite.jpg"), cv2.cvtColor(composite, cv2.COLOR_RGB2BGR))
    
    print(f"Sample dataset created in: {output_dir}")
    print("Each sample contains:")
    print("  - wide.jpg: Wide angle camera simulation")
    print("  - tele.jpg: Telephoto camera simulation")
    print("  - scene.jpg: Original synthetic scene")
    print("  - composite.jpg: Side-by-side comparison")


def create_realistic_sample() -> None:
    """Create a more realistic sample using real image data."""
    # Use a real image from skimage
    img = data.astronaut()
    img = img.astype(np.float32) / 255.0
    
    # Create wide and tele versions
    wide_img = simulate_wide_camera(img, zoom_factor=1.0)
    tele_img = simulate_tele_camera(img, zoom_factor=2.0)
    
    # Add artifacts
    wide_img = add_camera_artifacts(wide_img, "wide")
    tele_img = add_camera_artifacts(tele_img, "tele")
    
    # Save
    output_dir = Path("samples/realistic")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    wide_uint8 = (wide_img * 255).astype(np.uint8)
    tele_uint8 = (tele_img * 255).astype(np.uint8)
    
    cv2.imwrite(str(output_dir / "wide.jpg"), cv2.cvtColor(wide_uint8, cv2.COLOR_RGB2BGR))
    cv2.imwrite(str(output_dir / "tele.jpg"), cv2.cvtColor(tele_uint8, cv2.COLOR_RGB2BGR))
    
    print("Realistic sample created in: samples/realistic/")


def main():
    parser = argparse.ArgumentParser(description="Create Sample Dual-Camera Data")
    parser.add_argument("--output", default="samples", help="Output directory")
    parser.add_argument("--num_samples", type=int, default=5, help="Number of samples to create")
    parser.add_argument("--realistic", action="store_true", help="Create realistic sample using real image")
    
    args = parser.parse_args()
    
    if args.realistic:
        create_realistic_sample()
    else:
        create_sample_dataset(args.output, args.num_samples)
    
    print("\nSample data creation completed!")
    print("You can now test the fusion methods using:")
    print("  python align_and_fuse.py --wide samples/sample_01/wide.jpg --tele samples/sample_01/tele.jpg")


if __name__ == "__main__":
    main()



