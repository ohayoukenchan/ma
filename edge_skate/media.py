"""Media loading utilities for the Edge Skate prototype."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, List

Matrix = List[List[float]]


class MediaLoader:
    """Load frames from simple JSON matrices used for prototyping."""

    def load_frame(self, source: Path) -> Matrix:
        data = self._read_json(source)
        frame = self._validate_frame(data)
        return frame

    @staticmethod
    def _read_json(path: Path) -> Any:
        with Path(path).open("r", encoding="utf-8") as handle:
            return json.load(handle)

    @staticmethod
    def _validate_frame(data: Any) -> Matrix:
        if not isinstance(data, list) or not data:
            raise ValueError("Frame JSON must be a non-empty 2D list")
        frame: Matrix = []
        width = None
        for row in data:
            if not isinstance(row, list):
                raise ValueError("Frame rows must be lists")
            if width is None:
                width = len(row)
            elif len(row) != width:
                raise ValueError("Frame rows must have consistent lengths")
            frame.append([float(value) for value in row])
        return frame
