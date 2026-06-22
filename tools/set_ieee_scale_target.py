from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGETS = ROOT / "paper/tables/ieee_scale_eval_targets.csv"
MIN_EPOCHS = 100


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Enable a scale-diagnostic target only after its completed local VisDrone run exists."
    )
    parser.add_argument("--targets-csv", default=str(DEFAULT_TARGETS), help="Scale evaluation target CSV.")
    parser.add_argument("--model", required=True, help="Model name in the targets CSV.")
    parser.add_argument("--run-dir", required=True, help="Local VisDrone run directory.")
    parser.add_argument(
        "--note",
        default="enabled after completed VisDrone weights were synced",
        help="Note written to the target row when enabling it.",
    )
    parser.add_argument("--apply", action="store_true", help="Write enabled=true. Without this flag, only check readiness.")
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


def read_rows(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing target CSV: {path}")
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = list(reader.fieldnames or [])
    return rows, fieldnames


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
            f"{args.model} target remains disabled because the local VisDrone run is not complete: {detail}"
        )

    rows, fieldnames = read_rows(targets)
    if not rows or not fieldnames:
        raise SystemExit(f"No rows found in {targets}")

    found = False
    changed = False
    for row in rows:
        if row.get("model") != args.model:
            continue
        found = True
        if row.get("enabled", "").strip().lower() != "true":
            row["enabled"] = "true"
            row["note"] = args.note
            changed = True

    if not found:
        raise SystemExit(f"Missing {args.model} row in {targets}")
    if args.apply:
        if changed:
            write_rows(targets, rows, fieldnames)
            print(f"Enabled {args.model} in {targets.relative_to(ROOT)}")
        else:
            print(f"{args.model} is already enabled in {targets.relative_to(ROOT)}")
    else:
        print(f"Ready to enable {args.model}: {detail}")
        print("Re-run with --apply after confirming the result gate is open.")


if __name__ == "__main__":
    main()
