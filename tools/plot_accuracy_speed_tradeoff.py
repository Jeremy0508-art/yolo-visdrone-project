from __future__ import annotations

import argparse
import csv
from pathlib import Path


def read_rows(main_csv: Path, speed_csv: Path) -> list[dict[str, str]]:
    with main_csv.open(newline="", encoding="utf-8-sig") as f:
        main_rows = list(csv.DictReader(f))
    with speed_csv.open(newline="", encoding="utf-8-sig") as f:
        speed_rows = {row["model"]: row for row in csv.DictReader(f)}

    rows: list[dict[str, str]] = []
    for row in main_rows:
        model = row["model"]
        speed = speed_rows.get(model)
        if not speed:
            continue
        if not row.get("best_map50_95") or not speed.get("fps_wall"):
            continue
        rows.append(
            {
                "model": model,
                "input_size": row["input_size"],
                "params_m": f"{float(row['params']) / 1_000_000:.3f}",
                "best_map50_95": row["best_map50_95"],
                "fps_wall": speed["fps_wall"],
            }
        )
    return rows


def write_plot(rows: list[dict[str, str]], output: Path) -> None:
    import matplotlib.pyplot as plt

    output.parent.mkdir(parents=True, exist_ok=True)
    x = [float(row["fps_wall"]) for row in rows]
    y = [float(row["best_map50_95"]) for row in rows]
    params = [float(row["params_m"]) for row in rows]
    sizes = [max(80.0, p * 90.0) for p in params]

    fig, ax = plt.subplots(figsize=(8.5, 5.4), dpi=180)
    scatter = ax.scatter(x, y, s=sizes, c=params, cmap="viridis", alpha=0.82, edgecolors="#202020", linewidths=0.8)

    for row in rows:
        label = row["model"].replace("YOLO11n-P2-CoordAttention", "P2-CA").replace(" baseline", "")
        ax.annotate(
            label,
            (float(row["fps_wall"]), float(row["best_map50_95"])),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=7.5,
        )

    ax.set_xlabel("FPS (single-image wall-clock)")
    ax.set_ylabel("Best mAP50-95 on VisDrone val")
    ax.set_title("Accuracy-Speed-Parameter Trade-off")
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.45)
    ax.set_axisbelow(True)
    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label("Parameters (M)")
    fig.tight_layout()
    fig.savefig(output)
    plt.close(fig)


def write_table(rows: list[dict[str, str]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["model", "input_size", "params_m", "best_map50_95", "fps_wall"])
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot paper-facing accuracy-speed trade-off from audited CSV tables.")
    parser.add_argument("--main-csv", type=Path, default=Path("paper/tables/main_comparison_for_paper.csv"))
    parser.add_argument("--speed-csv", type=Path, default=Path("paper/tables/speed_results.csv"))
    parser.add_argument("--output", type=Path, default=Path("paper/figures/tradeoff/accuracy_speed_tradeoff.png"))
    parser.add_argument("--table-output", type=Path, default=Path("paper/tables/accuracy_speed_tradeoff.csv"))
    args = parser.parse_args()

    rows = read_rows(args.main_csv, args.speed_csv)
    if not rows:
        raise SystemExit("No matching completed model rows found in the input tables.")
    write_table(rows, args.table_output)
    write_plot(rows, args.output)
    print(f"Wrote {args.table_output}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
