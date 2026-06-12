from __future__ import annotations

import csv
import json
import platform
import subprocess
import sys
from dataclasses import asdict, is_dataclass
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_ROOT = PROJECT_ROOT / "results"


def _package_version(name: str) -> str:
    try:
        return version(name)
    except PackageNotFoundError:
        return "not-installed"


def _git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=PROJECT_ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.SubprocessError):
        return "unknown"


def runtime_metadata(seed: int) -> dict[str, Any]:
    return {
        "seed": seed,
        "git_commit": _git_commit(),
        "python": sys.version,
        "platform": platform.platform(),
        "packages": {
            name: _package_version(name)
            for name in ("numpy", "scipy", "galois", "plkg")
        },
    }


def save_run(
    experiment: str,
    parameters: dict[str, Any],
    rows: list[dict[str, Any]],
    seed: int,
) -> tuple[Path, Path]:
    run_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
    output_dir = RESULTS_ROOT / experiment / run_id
    output_dir.mkdir(parents=True, exist_ok=False)

    csv_path = output_dir / "results.csv"
    if rows:
        with csv_path.open("w", newline="", encoding="utf-8") as output:
            writer = csv.DictWriter(output, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    else:
        csv_path.touch()

    manifest = {
        "experiment": experiment,
        "run_id": run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "parameters": parameters,
        "runtime": runtime_metadata(seed),
        "rows": rows,
    }
    json_path = output_dir / "manifest.json"
    json_path.write_text(
        json.dumps(manifest, indent=2, default=_json_default),
        encoding="utf-8",
    )
    return csv_path, json_path


def _json_default(value: Any) -> Any:
    if is_dataclass(value):
        return asdict(value)
    if hasattr(value, "item"):
        return value.item()
    if hasattr(value, "tolist"):
        return value.tolist()
    raise TypeError(f"{type(value).__name__} is not JSON serializable")
