import json
from pathlib import Path

from edge_skate.pipeline import EdgeSkatePipeline, PipelineConfig


def test_pipeline_generates_outputs(tmp_path: Path) -> None:
    source = Path("samples/sample_frame.json")
    config = PipelineConfig(
        target_resolution=(16, 16),
        denoise_strength=0.2,
        edge_threshold=0.2,
        smoothing_factor=0.3,
        base_speed=2.5,
        trick_interval=5,
        output_dir=tmp_path,
    )
    pipeline = EdgeSkatePipeline(config)
    result_dir = pipeline.run(source, export_name="test")
    assert result_dir.exists()
    overlay = (result_dir / "overlay.txt").read_text(encoding="utf-8")
    assert "S" in overlay
    course_data = json.loads((result_dir / "course.json").read_text(encoding="utf-8"))
    assert len(course_data["points"]) > 0
    simulation_data = json.loads((result_dir / "simulation.json").read_text(encoding="utf-8"))
    assert simulation_data["velocities"], "expected non-empty velocity sequence"
