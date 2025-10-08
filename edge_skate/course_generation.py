"""Generate a rideable course from extracted edges."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence, Tuple

Matrix = List[List[float]]
Point = Tuple[float, float]


def _distance(a: Point, b: Point) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


@dataclass
class Course:
    points: List[Point]

    def length(self) -> float:
        if len(self.points) < 2:
            return 0.0
        return sum(_distance(a, b) for a, b in zip(self.points[:-1], self.points[1:]))


def generate_course(edge_map: Matrix, *, smoothing: float) -> Course:
    candidates = _largest_component(edge_map)
    if not candidates:
        return Course(points=[])
    ordered = _order_points(candidates)
    smoothed = _smooth_path(ordered, smoothing)
    return Course(points=smoothed)


def _largest_component(edge_map: Matrix) -> List[Point]:
    rows = len(edge_map)
    cols = len(edge_map[0]) if edge_map else 0
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    best: List[Point] = []
    for y in range(rows):
        for x in range(cols):
            if edge_map[y][x] <= 0 or visited[y][x]:
                continue
            stack = [(y, x)]
            visited[y][x] = True
            component: List[Point] = []
            while stack:
                cy, cx = stack.pop()
                component.append((float(cx), float(cy)))
                for ny in range(max(0, cy - 1), min(rows - 1, cy + 1) + 1):
                    for nx in range(max(0, cx - 1), min(cols - 1, cx + 1) + 1):
                        if visited[ny][nx] or edge_map[ny][nx] <= 0:
                            continue
                        visited[ny][nx] = True
                        stack.append((ny, nx))
            if len(component) > len(best):
                best = component
    return best


def _order_points(points: Sequence[Point]) -> List[Point]:
    if not points:
        return []
    cx = sum(p[0] for p in points) / len(points)
    cy = sum(p[1] for p in points) / len(points)
    points_with_angle = [((p[0], p[1]), _angle(p[0] - cx, p[1] - cy)) for p in points]
    points_with_angle.sort(key=lambda item: item[1])
    return [point for point, _ in points_with_angle]


def _angle(x: float, y: float) -> float:
    import math

    return math.atan2(y, x)


def _smooth_path(points: Sequence[Point], smoothing: float) -> List[Point]:
    if len(points) < 3:
        return list(points)
    window = max(2, int(round(3 * smoothing)))
    smoothed: List[Point] = [points[0]]
    for idx in range(1, len(points) - 1):
        start = max(0, idx - window)
        end = min(len(points), idx + window + 1)
        segment = points[start:end]
        avg_x = sum(p[0] for p in segment) / len(segment)
        avg_y = sum(p[1] for p in segment) / len(segment)
        smoothed.append((avg_x, avg_y))
    smoothed.append(points[-1])
    return smoothed
