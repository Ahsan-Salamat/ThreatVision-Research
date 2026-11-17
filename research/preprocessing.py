"""Numerical functions extracted from the application; provenance in baseline audit."""
import numpy as np
import cv2
from scipy.fftpack import dct as scipy_dct
MATRIX_DIM = 256
CNN_SIZE = 224

def bytes_to_stream(raw: bytes) -> np.ndarray:
    return np.frombuffer(raw, dtype=np.uint8)

def build_bigram_matrix(stream: np.ndarray) -> np.ndarray:
    left = stream[:-1].astype(np.int32)
    right = stream[1:].astype(np.int32)
    flat_indices = left << 8 | right
    matrix = np.bincount(flat_indices, minlength=65536).reshape(MATRIX_DIM, MATRIX_DIM).astype(np.float64)
    return matrix

def preprocess_matrix(matrix: np.ndarray) -> np.ndarray:
    matrix[0, 0] = 0.0
    max_val = matrix.max()
    if max_val > 0.0:
        return matrix / max_val
    return matrix

def matrix_to_gray(matrix: np.ndarray) -> np.ndarray:
    return (matrix * 255.0).astype(np.uint8)

def apply_2d_dct(gray: np.ndarray) -> np.ndarray:
    f64 = gray.astype(np.float64)
    dct_r = scipy_dct(f64, type=2, axis=0, norm='ortho')
    dct_2d = scipy_dct(dct_r, type=2, axis=1, norm='ortho')
    log_mag = np.log1p(np.abs(dct_2d))
    max_v = log_mag.max()
    if max_v > 0.0:
        normalised = (log_mag / max_v * 255.0).astype(np.uint8)
    else:
        normalised = log_mag.astype(np.uint8)
    return normalised

def resize_to_cnn(arr: np.ndarray, size: int=CNN_SIZE) -> np.ndarray:
    if arr.shape != (size, size):
        return cv2.resize(arr, (size, size), interpolation=cv2.INTER_AREA)
    return arr
def tensor(raw):
    """Transform bytes with the production operations; no PE label is implied."""
    if not isinstance(raw, bytes) or len(raw) < 2:
        raise ValueError("At least two bytes required")
    if len(raw) > 32 * 1024 * 1024:
        raise ValueError("Input exceeds 32 MiB")
    matrix = build_bigram_matrix(bytes_to_stream(raw))
    image = resize_to_cnn(apply_2d_dct(matrix_to_gray(preprocess_matrix(matrix))))
    return prepare_tensor(image)

def prepare_tensor(image):
    if image.shape != (224, 224) or image.dtype != np.uint8:
        raise ValueError("Expected a 224 x 224 uint8 image")
    return image.astype(np.float32)[None, :, :, None] / 255.0
