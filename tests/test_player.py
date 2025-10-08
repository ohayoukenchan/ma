from __future__ import annotations

from io import StringIO
from pathlib import Path

from edge_skate.pipeline import EdgeSkatePipeline, PipelineConfig
from edge_skate.player import iter_playback_frames, play


def _build_pipeline(tmp_path: Path | None = None) -> EdgeSkatePipeline:
    config = PipelineConfig(
        target_resolution=(16, 16),
        denoise_strength=0.2,
        edge_threshold=0.2,
        smoothing_factor=0.3,
        base_speed=2.5,
        trick_interval=5,
        output_dir=tmp_path or Path("output"),
    )
    return EdgeSkatePipeline(config)


def test_iter_playback_frames_matches_final_overlay(tmp_path: Path) -> None:
    pipeline = _build_pipeline(tmp_path)
    artifacts = pipeline.create_session(Path("samples/sample_frame.json"))
    frames = list(iter_playback_frames(artifacts))
    assert frames, "expected at least one playback frame"
    assert frames[-1].overlay == artifacts.overlay


def test_play_streams_ascii_without_sleep(tmp_path: Path) -> None:
    pipeline = _build_pipeline(tmp_path)
    stream = StringIO()
    artifacts = play(
        Path("samples/sample_frame.json"),
        config=pipeline.config,
        frame_delay=0,
        stream=stream,
        clear_between_frames=False,
    )
    output = stream.getvalue()
    assert artifacts.overlay in output
    assert "velocity:" in output
