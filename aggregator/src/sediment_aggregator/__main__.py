"""CLI entrypoint: `python -m sediment_aggregator run|serve`."""

from __future__ import annotations

import argparse
import os
from datetime import date

from .config import Settings
from .logging_config import configure_logging
from .ollama_client import OllamaClient
from .pipeline import run_for_date
from .scheduler import serve
from .sources.file_based import JsonFileMeetilySource, JsonFileScreenpipeSource


def main() -> None:
    parser = argparse.ArgumentParser(prog="sediment-aggregator")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run once for a single date and exit")
    run_parser.add_argument(
        "--date", type=date.fromisoformat, default=date.today(), help="YYYY-MM-DD, default today"
    )

    subparsers.add_parser("serve", help="Run daily on a schedule with a status endpoint")

    args = parser.parse_args()
    configure_logging(os.environ.get("LOG_LEVEL", "INFO"))
    settings = Settings.from_env()

    if args.command == "run":
        output_path = run_for_date(
            args.date,
            meetily=JsonFileMeetilySource(settings.meetily_export_dir),
            screenpipe=JsonFileScreenpipeSource(settings.screenpipe_export_dir),
            ollama=OllamaClient(settings.ollama_base_url, settings.ollama_model),
            output_dir=settings.output_dir,
        )
        print(f"wrote {output_path}")
    elif args.command == "serve":
        serve(settings)


if __name__ == "__main__":
    main()
