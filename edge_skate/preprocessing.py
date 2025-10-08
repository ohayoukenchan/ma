"""Frame preprocessing mimicking noise removal and normalization."""
from __future__ import annotations

import math
from typing import List

Matrix = List[List[float]]


def preprocess_frame(
    frame: Matrix,
    *,
    target_resolution: tuple[int, int],
    denoise_strength: float,
) -> Matrix:
    """Resize, normalize, and denoise the frame."""

    normalized = _normalize(frame)
    resized = _resize(normalized, target_resolution)
    if denoise_strength > 0:
        sigma = max(0.1, denoise_strength * 2)
        return _gaussian_blur(resized, sigma)
    return resized


def _normalize(frame: Matrix) -> Matrix:
    min_val = min(min(row) for row in frame)
    max_val = max(max(row) for row in frame)
    if max_val - min_val < 1e-5:
        return [[0.0 for _ in row] for row in frame]
    scale = max_val - min_val
    return [[(value - min_val) / scale for value in row] for row in frame]


def _resize(frame: Matrix, target_resolution: tuple[int, int]) -> Matrix:
    target_h, target_w = target_resolution
    src_h = len(frame)
    src_w = len(frame[0]) if frame else 0
    if src_h == 0 or src_w == 0:
        return [[0.0] * target_w for _ in range(target_h)]
    scale_y = src_h / target_h
    scale_x = src_w / target_w
    resized: Matrix = []
    for y in range(target_h):
        src_y = min(src_h - 1, int(y * scale_y))
        row: List[float] = []
        for x in range(target_w):
            src_x = min(src_w - 1, int(x * scale_x))
            row.append(frame[src_y][src_x])
        resized.append(row)
    return resized


def _gaussian_blur(frame: Matrix, sigma: float) -> Matrix:
    radius = max(1, int(math.ceil(3 * sigma)))
    kernel = [_gaussian_value(x, sigma) for x in range(-radius, radius + 1)]
    norm = sum(kernel)
    kernel = [value / norm for value in kernel]
    vertical = _convolve1d(frame, kernel, axis=0)
    return _convolve1d(vertical, kernel, axis=1)


def _gaussian_value(x: int, sigma: float) -> float:
    return math.exp(-(x ** 2) / (2 * sigma ** 2))


def _convolve1d(frame: Matrix, kernel: List[float], axis: int) -> Matrix:
    height = len(frame)
    width = len(frame[0]) if frame else 0
    radius = len(kernel) // 2
    result = [[0.0 for _ in range(width)] for _ in range(height)]
    if axis == 0:
        for y in range(height):
            for x in range(width):
                accum = 0.0
                for k, weight in enumerate(kernel):
                    offset = k - radius
                    src_y = min(height - 1, max(0, y + offset))
                    accum += frame[src_y][x] * weight
                result[y][x] = accum
    else:
        for y in range(height):
            for x in range(width):
                accum = 0.0
                for k, weight in enumerate(kernel):
                    offset = k - radius
                    src_x = min(width - 1, max(0, x + offset))
                    accum += frame[y][src_x] * weight
                result[y][x] = accum
    return result
