"""Export helpers writing pipeline artifacts to disk."""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .course_generation import Course
from .physics import SimulationResult


class DirectoryWriter:
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir

    def prepare(self, name: str) -> Path:
        target = self.base_dir / name
        target.mkdir(parents=True, exist_ok=True)
        return target


def export_session(
    writer: DirectoryWriter,
    name: str,
    frame: Any,
    edges: Any,
    course: Course,
    simulation: SimulationResult,
    overlay: str,
) -> Path:
    target = writer.prepare(name)
    _write_json(target / "frame.json", frame)
    _write_json(target / "edges.json", edges)
    _write_json(target / "course.json", {"points": course.points, "length": course.length()})
    _write_json(
        target / "simulation.json",
        {
            "path": simulation.path,
            "velocities": simulation.velocities,
            "trick_events": [asdict(event) for event in simulation.trick_events],
        },
    )
    (target / "overlay.txt").write_text(overlay, encoding="utf-8")
    return target


def _write_json(path: Path, data: Any) -> None:
    serializable = _to_serializable(data)
    with Path(path).open("w", encoding="utf-8") as handle:
        json.dump(serializable, handle, ensure_ascii=False, indent=2)


def _to_serializable(data: Any) -> Any:
    if isinstance(data, dict):
        return {key: _to_serializable(value) for key, value in data.items()}
    if isinstance(data, (list, tuple)):
        return [_to_serializable(item) for item in data]
    return data
