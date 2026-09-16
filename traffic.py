"""Image-based traffic timing demonstration, not a vehicle-count estimator."""
from dataclasses import dataclass
from pathlib import Path
import math
import cv2
import numpy as np
from CannyEdgeDetector import CannyEdgeDetector

ROOT = Path(__file__).resolve().parent
DEFAULT_REFERENCE = ROOT / 'images' / 'refrence.png'

def read_gray(path):
    path = Path(path)
    if not path.is_file(): raise ValueError(f'Image not found: {path}')
    image = cv2.imdecode(np.frombuffer(path.read_bytes(), dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
    if image is None or min(image.shape) < 3: raise ValueError(f'Cannot read a usable image: {path.name}')
    return image.astype(np.float64)

def detect_edges(image):
    return CannyEdgeDetector([image], sigma=1.4, kernel_size=5,
        lowthreshold=0.09, highthreshold=0.20, weak_pixel=100).detect()[0].astype(np.uint8)

def green_seconds(ratio):
    if not math.isfinite(ratio) or ratio < 0: raise ValueError('Ratio must be finite and nonnegative.')
    if ratio >= 90: return 60
    if ratio > 85: return 50
    if ratio > 75: return 40
    if ratio > 50: return 30
    return 20

@dataclass
class Analysis:
    sample_edges: np.ndarray
    reference_edges: np.ndarray
    sample_pixels: int
    reference_pixels: int
    ratio: float
    seconds: int

def analyze(sample_path, reference_path=DEFAULT_REFERENCE):
    sample, reference = read_gray(sample_path), read_gray(reference_path)
    if sample.shape != reference.shape:
        sample = cv2.resize(sample, (reference.shape[1], reference.shape[0]), interpolation=cv2.INTER_AREA)
    sample_edges, reference_edges = detect_edges(sample), detect_edges(reference)
    sample_pixels = int(np.count_nonzero(sample_edges == 255))
    reference_pixels = int(np.count_nonzero(reference_edges == 255))
    if reference_pixels == 0: raise ValueError('Reference image has no detectable edges. Choose a nonblank reference.')
    ratio = 100.0 * sample_pixels / reference_pixels
    return Analysis(sample_edges, reference_edges, sample_pixels, reference_pixels, ratio, green_seconds(ratio))

def save_edges(path, image):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    ok, data = cv2.imencode('.png', image)
    if not ok: raise ValueError('Unable to encode edge image.')
    path.write_bytes(data.tobytes())
