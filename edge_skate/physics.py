"""Simple physics approximation for the skateboard run."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .course_generation import Course, Point, _distance


@dataclass
class TrickEvent:
    frame: int
    name: str


@dataclass
class SimulationResult:
    path: List[Point]
    velocities: List[float]
    trick_events: List[TrickEvent]


def simulate_run(
    course: Course,
    *,
    base_speed: float,
    trick_interval: int,
) -> SimulationResult:
    if len(course.points) < 2:
        return SimulationResult(path=course.points, velocities=[], trick_events=[])
    distances = _segment_lengths(course.points)
    velocities = _simulate_velocities(distances, base_speed)
    path = _interpolate_path(course.points, distances)
    tricks = _generate_tricks(path, trick_interval)
    return SimulationResult(path=path, velocities=velocities, trick_events=tricks)


def _segment_lengths(points: List[Point]) -> List[float]:
    return [_distance(a, b) for a, b in zip(points[:-1], points[1:])]


def _simulate_velocities(distances: List[float], base_speed: float) -> List[float]:
    if not distances:
        return []
    mean_distance = sum(distances) / len(distances)
    velocity = base_speed
    velocities: List[float] = []
    for distance in distances:
        slope_factor = 1.0 + 0.3 * (distance - mean_distance)
        velocity = max(0.5, velocity * 0.9 + slope_factor * 0.1)
        velocities.append(float(velocity))
    return velocities


def _interpolate_path(points: List[Point], distances: List[float]) -> List[Point]:
    interpolated: List[Point] = [points[0]]
    for (x0, y0), (x1, y1), dist in zip(points[:-1], points[1:], distances):
        steps = max(1, int(round(dist)))
        for step in range(1, steps + 1):
            t = step / (steps + 1)
            interpolated.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
    interpolated.append(points[-1])
    return interpolated


def _generate_tricks(path: List[Point], trick_interval: int) -> List[TrickEvent]:
    if trick_interval <= 0:
        return []
    events: List[TrickEvent] = []
    for idx in range(trick_interval, len(path), trick_interval):
        name = "kickflip" if idx % (2 * trick_interval) == 0 else "ollie"
        events.append(TrickEvent(frame=idx, name=name))
    return events
