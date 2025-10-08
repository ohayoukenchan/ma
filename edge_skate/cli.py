"""Command line interface for running the prototype pipeline."""
from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import EdgeSkatePipeline, PipelineConfig


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the EdgeSkate prototype pipeline")
    parser.add_argument("sources", nargs="+", type=Path, help="JSON files describing grayscale frames")
    parser.add_argument("--output", type=Path, default=PipelineConfig.output_dir, help="Directory for exports")
    parser.add_argument("--resolution", type=int, nargs=2, metavar=("H", "W"), default=(128, 128))
    parser.add_argument("--denoise", type=float, default=0.25)
    parser.add_argument("--threshold", type=float, default=0.25)
    parser.add_argument("--smoothing", type=float, default=0.5)
    parser.add_argument("--speed", type=float, default=2.0)
    parser.add_argument("--trick-interval", type=int, default=15)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    config = PipelineConfig(
        target_resolution=(args.resolution[0], args.resolution[1]),
        denoise_strength=args.denoise,
        edge_threshold=args.threshold,
        smoothing_factor=args.smoothing,
        base_speed=args.speed,
        trick_interval=args.trick_interval,
        output_dir=args.output,
    )
    pipeline = EdgeSkatePipeline(config)
    pipeline.batch_run(args.sources)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
