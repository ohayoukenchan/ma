"""Simple ASCII player for EdgeSkate sessions."""
from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, TextIO

from .pipeline import EdgeSkatePipeline, PipelineConfig, SessionArtifacts
from .physics import TrickEvent
from .rendering import render_overlay


@dataclass
class PlaybackFrame:
    """Represents a single playback step."""

    index: int
    overlay: str
    velocity: float | None = None
    trick_event: TrickEvent | None = None


def iter_playback_frames(artifacts: SessionArtifacts) -> Iterator[PlaybackFrame]:
    """Yield ASCII overlays to animate the simulated run."""

    path = artifacts.simulation.path
    if not path:
        yield PlaybackFrame(index=0, overlay=render_overlay(artifacts.processed_frame, []))
        return

    trick_lookup = {event.frame: event for event in artifacts.simulation.trick_events}
    velocities = artifacts.simulation.velocities
    for idx in range(1, len(path) + 1):
        segment = path[:idx]
        overlay = render_overlay(artifacts.processed_frame, segment)
        velocity = None
        if velocities:
            velocity = velocities[min(idx - 1, len(velocities) - 1)]
        yield PlaybackFrame(
            index=idx,
            overlay=overlay,
            velocity=velocity,
            trick_event=trick_lookup.get(idx),
        )


def play(
    source: Path,
    *,
    config: PipelineConfig | None = None,
    frame_delay: float = 0.15,
    stream: TextIO | None = None,
    clear_between_frames: bool = True,
) -> SessionArtifacts:
    """Run the pipeline for a source and stream a simple ASCII playback."""

    pipeline = EdgeSkatePipeline(config)
    artifacts = pipeline.create_session(source)
    target_stream = stream or sys.stdout

    for frame in iter_playback_frames(artifacts):
        _write_frame(target_stream, frame, clear_between_frames)
        _sleep_for_frame(frame_delay, frame.velocity)

    return artifacts


def _write_frame(stream: TextIO, frame: PlaybackFrame, clear: bool) -> None:
    if clear:
        stream.write("\x1b[2J\x1b[H")
    stream.write(frame.overlay)
    stream.write("\n")
    if frame.velocity is not None:
        stream.write(f"velocity: {frame.velocity:.2f}\n")
    if frame.trick_event:
        stream.write(f"trick: {frame.trick_event.name} (frame {frame.trick_event.frame})\n")
    stream.flush()


def _sleep_for_frame(base_delay: float, velocity: float | None) -> None:
    if base_delay <= 0:
        return
    delay = base_delay
    if velocity and velocity > 0:
        delay = base_delay / max(0.5, velocity)
    time.sleep(delay)

