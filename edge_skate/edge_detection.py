"""Edge detection approximating Sobel behavior using pure Python."""
from __future__ import annotations

from typing import List

Matrix = List[List[float]]

_SOBEL_X = ((1, 0, -1), (2, 0, -2), (1, 0, -1))
_SOBEL_Y = ((1, 2, 1), (0, 0, 0), (-1, -2, -1))


def detect_edges(frame: Matrix, *, threshold: float) -> Matrix:
    height = len(frame)
    width = len(frame[0]) if frame else 0
    magnitude = [[0.0 for _ in range(width)] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            gx = _apply_kernel(frame, _SOBEL_X, x, y)
            gy = _apply_kernel(frame, _SOBEL_Y, x, y)
            magnitude[y][x] = (gx ** 2 + gy ** 2) ** 0.5
    max_val = max((value for row in magnitude for value in row), default=1.0)
    if max_val == 0:
        max_val = 1.0
    normalized = [[value / max_val for value in row] for row in magnitude]
    return [[1.0 if value >= threshold else 0.0 for value in row] for row in normalized]


def _apply_kernel(frame: Matrix, kernel: tuple[tuple[int, ...], ...], x: int, y: int) -> float:
    height = len(frame)
    width = len(frame[0]) if frame else 0
    k_size = len(kernel)
    radius = k_size // 2
    accum = 0.0
    for ky in range(k_size):
        for kx in range(k_size):
            weight = kernel[ky][kx]
            src_x = min(width - 1, max(0, x + kx - radius))
            src_y = min(height - 1, max(0, y + ky - radius))
            accum += frame[src_y][src_x] * weight
    return accum
