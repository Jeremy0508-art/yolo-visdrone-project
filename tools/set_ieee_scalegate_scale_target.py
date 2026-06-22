from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGETS = ROOT / "paper/tables/ieee_scale_eval_targets.csv"
DEFAULT_RUN_DIR = ROOT / "runs/detect/yolo11n_p2_scalegate_960_visdrone"
MODEL = "YOLO11n-P2-ScaleGate-960"
MIN_EPOCHS = 100


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Enable the ScaleGate scale-diagnostic target only after the completed local VisDrone run exists."
    )
    parser.add_argument("--targets-csv", default=str(DEFAULT_TARGETS), help="Scale evaluation target CSV.")
    parser.add_argument("--run-dir", default=str(DEFAULT_RUN_DIR), help="Local ScaleGate VisDrone run directory.")
    parser.add_argument("--apply", action="store_true", help="Write the enabled=true update. Without this flag, only check readiness.")
    return parser.parse_args()


def count_epochs(run_dir: Path) -> int:
    results = run_dir / "results.csv"
    if not results.exists():
        return 0
    with results.open(encoding="utf-8-sig", errors="ignore") as f:
        lines = [line for line in f if line.strip()]
    return max(len(lines) - 1, 0)


def complete_run(run_dir: Path) -> tuple[bool, str]:
    results = run_dir / "results.csv"
    args = run_dir / "args.yaml"
    weight = run_dir / "weights/best.pt"
    epochs = count_epochs(run_dir)
    missing = [str(path.relative_to(ROOT)).replace("\\", "/") for path in [results, args, weight] if not path.exists()]
    if epochs >= MIN_EPOCHS and not missing:
        return True, f"{run_dir.relative_to(ROOT).as_posix()}; epochs={epochs}; core artifacts present"
    detail = f"{run_dir.relative_to(ROOT).as_posix()}; epochs={epochs}/{MIN_EPOCHS}"
    if missing:
        detail += f"; missing: {', '.join(missing)}"
    return False, detail


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing target CSV: {path}")
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_rows(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    targets = Path(args.targets_csv)
    if not targets.is_absolute():
        targets = ROOT / targets
    run_dir = Path(args.run_dir)
    if not run_dir.is_absolute():
        run_dir = ROOT / run_dir

    complete, detail = complete_run(run_dir)
    if not complete:
        raise SystemExit(
            "ScaleGate target remains disabled because the local VisDrone run is not complete: "
            + detail
        )

    rows = read_rows(targets)
    if not rows:
        raise SystemExit(f"No rows found in {targets}")
    fieldnames = list(rows[0].keys())
    changed = False
    found = False
    for row in rows:
        if row.get("model") != MODEL:
            continue
        found = True
        if row.get("enabled", "").strip().lower() != "true":
            row["enabled"] = "true"
            row["note"] = "enabled after completed ScaleGate VisDrone weights were synced"
            changed = True

    if not found:
        raise SystemExit(f"Missing {MODEL} row in {targets}")
    if args.apply:
        if changed:
            write_rows(targets, rows, fieldnames)
            print(f"Enabled {MODEL} in {targets.relative_to(ROOT)}")
        else:
            print(f"{MODEL} is already enabled in {targets.relative_to(ROOT)}")
    else:
        print(f"Ready to enable {MODEL}: {detail}")
        print("Re-run with --apply after confirming the result gate is open.")


if __name__ == "__main__":
    main()
