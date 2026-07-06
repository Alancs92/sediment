"""Runs the daily pipeline on a schedule and exposes a tiny status endpoint.

Deliberately stdlib-only (threading + http.server) — this is a personal,
single-container batch job, not a service; a full web framework would be
more than the job needs. `GET /status` and `GET /healthz` are enough to
monitor it with `curl` or a browser.
"""

from __future__ import annotations

import json
import logging
import threading
import time
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .config import Settings
from .ollama_client import OllamaClient
from .pipeline import run_for_date
from .sources.file_based import JsonFileMeetilySource, JsonFileScreenpipeSource

logger = logging.getLogger(__name__)


@dataclass
class RunStatus:
    last_run_at: str | None = None
    last_run_ok: bool | None = None
    last_error: str | None = None
    last_output_path: str | None = None
    next_run_at: str | None = None


class _StatusHandler(BaseHTTPRequestHandler):
    status: RunStatus  # set via factory below

    def do_GET(self):  # noqa: N802 (stdlib method name)
        if self.path == "/healthz":
            body, code = b"ok", 200
        elif self.path == "/status":
            body = json.dumps(asdict(self.status)).encode("utf-8")
            code = 200
        else:
            body, code = b"not found", 404

        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):  # noqa: A002 - stdlib signature
        logger.debug("status server: " + format, *args)


def _make_handler(status: RunStatus) -> type[_StatusHandler]:
    return type("BoundStatusHandler", (_StatusHandler,), {"status": status})


def _seconds_until(run_time: str, now: datetime) -> float:
    hour, minute = (int(part) for part in run_time.split(":"))
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=1)
    return (target - now).total_seconds()


def run_once(settings: Settings, status: RunStatus) -> None:
    today = date.today()
    try:
        output_path = run_for_date(
            today,
            meetily=JsonFileMeetilySource(settings.meetily_export_dir),
            screenpipe=JsonFileScreenpipeSource(settings.screenpipe_export_dir),
            ollama=OllamaClient(settings.ollama_base_url, settings.ollama_model),
            output_dir=settings.output_dir,
        )
        status.last_run_ok = True
        status.last_error = None
        status.last_output_path = str(output_path)
    except Exception as exc:  # a scheduler loop must not die from one bad run
        logger.exception("daily run failed")
        status.last_run_ok = False
        status.last_error = str(exc)
    finally:
        status.last_run_at = datetime.now().isoformat(timespec="seconds")


def serve(settings: Settings) -> None:
    status = RunStatus()
    server = ThreadingHTTPServer(("0.0.0.0", settings.status_port), _make_handler(status))
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    logger.info("status endpoint on :%d (/status, /healthz)", settings.status_port)

    while True:
        wait_seconds = _seconds_until(settings.daily_run_time, datetime.now())
        status.next_run_at = (datetime.now() + timedelta(seconds=wait_seconds)).isoformat(
            timespec="seconds"
        )
        logger.info("next run at %s (in %.0fs)", status.next_run_at, wait_seconds)
        time.sleep(wait_seconds)
        run_once(settings, status)
