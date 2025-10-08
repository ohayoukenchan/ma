"""High level orchestration for the Edge Skate prototype pipeline."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from . import media, preprocessing, edge_detection, course_generation, physics, rendering, export


@dataclass
class PipelineConfig:
    """Configuration flags for the full pipeline."""

    target_resolution: tuple[int, int] = (128, 128)
    denoise_strength: float = 0.25
    edge_threshold: float = 0.25
    smoothing_factor: float = 0.5
    base_speed: float = 2.0
    trick_interval: int = 15
    output_dir: Path = Path("output")


@dataclass
class SessionArtifacts:
    """Intermediate results for a single pipeline run."""

    processed_frame: List[List[float]]
    edge_map: List[List[float]]
    course: course_generation.Course
    simulation: physics.SimulationResult
    overlay: str


class EdgeSkatePipeline:
    """Glues all pipeline steps together to mirror the README flow."""

    def __init__(self, config: PipelineConfig | None = None) -> None:
        self.config = config or PipelineConfig()
        self.config.output_dir.mkdir(parents=True, exist_ok=True)

    def run(self, source: Path, *, export_name: str = "session") -> Path:
        """Execute the full pipeline for a given media source."""

        artifacts = self.create_session(source)
        export_path = export.export_session(
            export.DirectoryWriter(self.config.output_dir),
            export_name,
            artifacts.processed_frame,
            artifacts.edge_map,
            artifacts.course,
            artifacts.simulation,
            artifacts.overlay,
        )
        return export_path

    def batch_run(self, sources: Iterable[Path]) -> List[Path]:
        """Run the pipeline for multiple sources, returning output paths."""

        results: List[Path] = []
        for idx, source in enumerate(sources):
            name = f"session_{idx:02d}"
            results.append(self.run(source, export_name=name))
        return results

    def create_session(self, source: Path) -> SessionArtifacts:
        """Return in-memory artifacts for a media source without exporting."""

        frame = media.MediaLoader().load_frame(source)
        processed = preprocessing.preprocess_frame(
            frame,
            target_resolution=self.config.target_resolution,
            denoise_strength=self.config.denoise_strength,
        )
        edges = edge_detection.detect_edges(processed, threshold=self.config.edge_threshold)
        course = course_generation.generate_course(edges, smoothing=self.config.smoothing_factor)
        simulation = physics.simulate_run(
            course,
            base_speed=self.config.base_speed,
            trick_interval=self.config.trick_interval,
        )
        overlay = rendering.render_overlay(processed, simulation.path)
        return SessionArtifacts(
            processed_frame=processed,
            edge_map=edges,
            course=course,
            simulation=simulation,
            overlay=overlay,
        )
