"""
Modul ekstraksi fitur untuk Skrining Anemia Non-Invasif.

PENTING: Seluruh fungsi di file ini HARUS identik dengan pipeline yang
digunakan saat training di notebook (skrining_anemia_FINAL.ipynb).
Jangan ubah parameter apapun di sini tanpa melatih ulang model.
"""

import cv2
import numpy as np
from skimage.feature import local_binary_pattern, graycomatrix, graycoprops


# ── Konfigurasi (harus sama dengan notebook training) ───────────────────
IMG_SIZE = (256, 256)
CLAHE_CLIP = 2.0
CLAHE_GRID = (8, 8)
COLOR_BINS = 32
GLCM_DISTANCES = [1]
GLCM_ANGLES = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]
LBP_PARAMS = [(1, 8), (2, 16), (3, 24)]
LBP_METHOD = "uniform"

FEATURE_DIM = 346  # 192 + 96 + 4 + 54


def load_and_resize(image_bgr: np.ndarray) -> np.ndarray:
    """Resize citra ke ukuran standar 256x256."""
    return cv2.resize(image_bgr, IMG_SIZE, interpolation=cv2.INTER_AREA)


def preprocess_image(img_bgr: np.ndarray) -> np.ndarray:
    """
    CLAHE pada kanal L ruang warna LAB.
    Mereduksi variasi pencahayaan tanpa mengubah informasi warna.
    """
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=CLAHE_CLIP, tileGridSize=CLAHE_GRID)
    l_eq = clahe.apply(l)
    lab_eq = cv2.merge([l_eq, a, b])
    return cv2.cvtColor(lab_eq, cv2.COLOR_LAB2BGR)


def extract_color_histogram(img_bgr: np.ndarray, bins: int = COLOR_BINS) -> np.ndarray:
    """Color Histogram RGB + HSV -> 192 dimensi."""
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    features = []
    for space in [img_rgb, img_hsv]:
        for ch in range(3):
            h = cv2.calcHist([space], [ch], None, [bins], [0, 256])
            h = cv2.normalize(h, h, norm_type=cv2.NORM_L1).flatten()
            features.append(h)
    return np.concatenate(features)


def extract_lab_histogram(img_bgr: np.ndarray, bins: int = COLOR_BINS) -> np.ndarray:
    """Color Histogram LAB -> 96 dimensi."""
    img_lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    features = []
    for ch in range(3):
        h = cv2.calcHist([img_lab], [ch], None, [bins], [0, 256])
        h = cv2.normalize(h, h, norm_type=cv2.NORM_L1).flatten()
        features.append(h)
    return np.concatenate(features)


def extract_glcm_features(img_bgr: np.ndarray) -> np.ndarray:
    """GLCM: contrast, correlation, energy, homogeneity -> 4 dimensi."""
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    glcm = graycomatrix(
        gray,
        distances=GLCM_DISTANCES,
        angles=GLCM_ANGLES,
        levels=256,
        symmetric=True,
        normed=True,
    )
    return np.array(
        [
            graycoprops(glcm, prop).mean()
            for prop in ["contrast", "correlation", "energy", "homogeneity"]
        ]
    )


def extract_lbp_multiscale(img_bgr: np.ndarray) -> np.ndarray:
    """LBP multi-skala r=1,2,3 -> 54 dimensi."""
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    features = []
    for radius, n_points in LBP_PARAMS:
        lbp_map = local_binary_pattern(gray, n_points, radius, method=LBP_METHOD)
        n_bins = n_points + 2
        hist, _ = np.histogram(
            lbp_map.ravel(), bins=n_bins, range=(0, n_bins), density=True
        )
        features.append(hist)
    return np.concatenate(features)


def extract_all_features(img_bgr: np.ndarray) -> np.ndarray:
    """
    Pipeline lengkap feature fusion: 346 dimensi.
    Input: citra BGR mentah (belum di-resize).
    Output: vektor fitur 346 dimensi siap di-scale dan diprediksi.
    """
    img_resized = load_and_resize(img_bgr)
    img_proc = preprocess_image(img_resized)
    return np.concatenate(
        [
            extract_color_histogram(img_proc),
            extract_lab_histogram(img_proc),
            extract_glcm_features(img_proc),
            extract_lbp_multiscale(img_proc),
        ]
    )
