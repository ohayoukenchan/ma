"""Rendering helpers that produce ASCII overlays for the prototype."""
from __future__ import annotations

from typing import Iterable, List

from .course_generation import Point

Matrix = List[List[float]]

ASCII_MAP = list(" .:-=+*#%@")


def render_overlay(frame: Matrix, path: Iterable[Point]) -> str:
    height = len(frame)
    width = len(frame[0]) if frame else 0
    display = [
        [ASCII_MAP[_intensity_to_index(value)] for value in row]
        for row in frame
    ]
    for x, y in path:
        ix = min(width - 1, max(0, int(round(x)))) if width else 0
        iy = min(height - 1, max(0, int(round(y)))) if height else 0
        if height and width:
            display[iy][ix] = "S"
    return "\n".join("".join(row) for row in display)


def _intensity_to_index(value: float) -> int:
    clamped = max(0.0, min(1.0, value))
    return min(int(clamped * (len(ASCII_MAP) - 1)), len(ASCII_MAP) - 1)
