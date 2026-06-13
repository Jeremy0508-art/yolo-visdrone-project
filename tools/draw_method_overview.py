from __future__ import annotations

from pathlib import Path


def add_box(ax, xy, width, height, text, facecolor, edgecolor="#1f2937", fontsize=10):
    import matplotlib.patches as patches

    box = patches.FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.025",
        linewidth=1.4,
        edgecolor=edgecolor,
        facecolor=facecolor,
    )
    ax.add_patch(box)
    ax.text(
        xy[0] + width / 2,
        xy[1] + height / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        color="#111827",
        linespacing=1.15,
    )


def add_arrow(ax, start, end, color="#374151"):
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops=dict(arrowstyle="->", linewidth=1.6, color=color, shrinkA=4, shrinkB=4),
    )


def main() -> None:
    import matplotlib.pyplot as plt

    out = Path("paper/figures/method/hrpca_yolo11n_overview.png")
    out.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(11.2, 5.8), dpi=180)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(
        0.5,
        0.94,
        "HRPCA-YOLO11n Overview for VisDrone Small-Object Detection",
        ha="center",
        va="center",
        fontsize=15,
        weight="bold",
        color="#111827",
    )

    add_box(ax, (0.04, 0.44), 0.12, 0.16, "Input\n960 x 960", "#dbeafe")
    add_box(ax, (0.22, 0.44), 0.16, 0.16, "YOLO11n\nBackbone", "#e0f2fe")
    add_box(ax, (0.43, 0.44), 0.15, 0.16, "Neck / Feature\nFusion", "#dcfce7")
    add_box(ax, (0.63, 0.44), 0.13, 0.16, "CoordAttention\nEnhancement", "#fef3c7", fontsize=9.0)
    add_box(ax, (0.88, 0.24), 0.09, 0.57, "Detect\nHead", "#fee2e2")

    add_arrow(ax, (0.16, 0.52), (0.22, 0.52))
    add_arrow(ax, (0.38, 0.52), (0.43, 0.52))
    add_arrow(ax, (0.58, 0.52), (0.63, 0.52))

    scale_y = [0.72, 0.61, 0.35, 0.24]
    scale_names = ["P2\nhigh-res", "P3", "P4", "P5"]
    scale_colors = ["#bfdbfe", "#bbf7d0", "#fde68a", "#fecaca"]
    for y, name, color in zip(scale_y, scale_names, scale_colors):
        add_box(ax, (0.78, y - 0.035), 0.08, 0.07, name, color, fontsize=8.4)
        add_arrow(ax, (0.76, y), (0.78, y))
        add_arrow(ax, (0.86, y), (0.88, y))

    ax.text(
        0.82,
        0.86,
        "Four-scale prediction branch",
        ha="center",
        va="center",
        fontsize=9.5,
        color="#374151",
    )

    add_box(ax, (0.35, 0.14), 0.32, 0.10, "Small-object-oriented design:\nshallow high-resolution features + position-aware attention", "#f3f4f6", fontsize=9)
    add_arrow(ax, (0.505, 0.44), (0.505, 0.24), color="#6b7280")

    ax.text(
        0.91,
        0.32,
        "VisDrone\npredictions",
        ha="center",
        va="center",
        fontsize=9.5,
        color="#374151",
    )
    add_arrow(ax, (0.925, 0.24), (0.925, 0.36), color="#6b7280")

    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
