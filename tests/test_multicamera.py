"""
Pytest tests for the MultiCamera fusion system (Chapter 15).

Tests cover the pure image-processing functions from align_and_fuse.py
and the synthetic data generation from create_sample_data.py.
Uses synthetic images so no external data files are needed.
"""

import sys
import os
import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "chapter15", "02_classical_method"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "chapter15", "01_setup"))

from align_and_fuse import (
    to_bgr_uint8,
    extract_highpass,
    compute_confidence_mask,
    fuse,
    digital_zoom,
)
from create_sample_data import (
    create_synthetic_scene,
    simulate_wide_camera,
    simulate_tele_camera,
    add_camera_artifacts,
)


def make_rgb_float(height=64, width=64):
    """Create a synthetic RGB float32 image in [0, 1]."""
    return np.random.rand(height, width, 3).astype(np.float32)


# ---------- align_and_fuse tests ----------

class TestToBgrUint8:
    def test_output_dtype_and_shape(self):
        img = make_rgb_float(32, 48)
        result = to_bgr_uint8(img)
        assert result.dtype == np.uint8
        assert result.shape == (32, 48, 3)

    def test_clamps_values(self):
        img = np.array([[[1.5, -0.1, 0.5]]], dtype=np.float32)
        result = to_bgr_uint8(img)
        assert result.max() <= 255
        assert result.min() >= 0


class TestExtractHighpass:
    def test_low_plus_high_equals_original(self):
        img = make_rgb_float(64, 64)
        low, high = extract_highpass(img, sigma=3.0)
        reconstructed = low + high
        np.testing.assert_allclose(reconstructed, img, atol=1e-5)

    def test_output_shapes(self):
        img = make_rgb_float(48, 64)
        low, high = extract_highpass(img, sigma=2.0)
        assert low.shape == img.shape
        assert high.shape == img.shape

    def test_low_is_smoother(self):
        img = make_rgb_float(64, 64)
        low, high = extract_highpass(img, sigma=5.0)
        assert np.std(low) < np.std(img)


class TestComputeConfidenceMask:
    def test_identical_images_high_confidence(self):
        img = make_rgb_float(64, 64)
        mask = compute_confidence_mask(img, img, thresh=0.08)
        assert mask.shape == (64, 64, 1)
        assert mask.mean() > 0.5

    def test_very_different_images_low_confidence(self):
        img1 = np.ones((64, 64, 3), dtype=np.float32) * 0.8
        img2 = np.ones((64, 64, 3), dtype=np.float32) * 0.1
        mask = compute_confidence_mask(img1, img2, thresh=0.08)
        assert mask.mean() < 0.3

    def test_blank_tele_zero_confidence(self):
        wide = make_rgb_float(64, 64)
        tele = np.zeros((64, 64, 3), dtype=np.float32)
        mask = compute_confidence_mask(wide, tele, thresh=0.08)
        assert mask.mean() == pytest.approx(0.0, abs=0.01)


class TestFuse:
    def test_output_shape_and_range(self):
        wide = make_rgb_float(64, 64)
        tele_warp = make_rgb_float(64, 64)
        fused, conf = fuse(wide, tele_warp, alpha=1.0)
        assert fused.shape == wide.shape
        assert conf.shape == (64, 64, 1)
        assert fused.min() >= 0.0
        assert fused.max() <= 1.0

    def test_fuse_with_identical_inputs(self):
        img = make_rgb_float(64, 64)
        fused, conf = fuse(img, img, alpha=1.0)
        assert fused.shape == img.shape


class TestDigitalZoom:
    def test_output_shape_preserved(self):
        img = make_rgb_float(128, 128)
        zoomed = digital_zoom(img, scale=2.0)
        assert zoomed.shape == img.shape

    def test_different_scales(self):
        img = make_rgb_float(128, 128)
        z1 = digital_zoom(img, scale=1.5)
        z2 = digital_zoom(img, scale=3.0)
        assert z1.shape == img.shape
        assert z2.shape == img.shape


# ---------- create_sample_data tests ----------

class TestCreateSyntheticScene:
    def test_shape_and_range(self):
        scene = create_synthetic_scene()
        assert scene.shape == (800, 1200, 3)
        assert scene.dtype in (np.float32, np.float64)
        assert scene.min() >= 0.0
        assert scene.max() <= 1.0


class TestSimulateWideCamera:
    def test_output_shape(self):
        scene = np.random.rand(200, 300, 3).astype(np.float32)
        wide = simulate_wide_camera(scene, zoom_factor=1.0)
        assert wide.shape == scene.shape
        assert wide.dtype == np.float32

    def test_values_in_range(self):
        scene = np.random.rand(200, 300, 3).astype(np.float32)
        wide = simulate_wide_camera(scene, zoom_factor=1.0)
        assert wide.min() >= 0.0
        assert wide.max() <= 1.0


class TestSimulateTeleCamera:
    def test_output_shape(self):
        scene = np.random.rand(200, 300, 3).astype(np.float32)
        tele = simulate_tele_camera(scene, zoom_factor=2.0)
        assert tele.shape == scene.shape
        assert tele.dtype == np.float32

    def test_values_in_range(self):
        scene = np.random.rand(200, 300, 3).astype(np.float32)
        tele = simulate_tele_camera(scene, zoom_factor=2.0)
        assert tele.min() >= 0.0
        assert tele.max() <= 1.0


class TestAddCameraArtifacts:
    def test_wide_artifacts(self):
        img = np.random.rand(100, 150, 3).astype(np.float32)
        result = add_camera_artifacts(img, "wide")
        assert result.shape == img.shape
        assert result.min() >= 0.0
        assert result.max() <= 1.0

    def test_tele_artifacts(self):
        img = np.random.rand(100, 150, 3).astype(np.float32)
        result = add_camera_artifacts(img, "tele")
        assert result.shape == img.shape
        assert result.min() >= 0.0
        assert result.max() <= 1.0
