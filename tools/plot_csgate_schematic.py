from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "paper/figures/method/csgate_schematic.png"

PALETTE = {
    "bg": "#f6f7f9",
    "mist": "#e3eef1",
    "rose": "#f8d8da",
    "peach": "#f1d0b0",
    "green": "#daebcf",
    "mint": "#d0ede4",
    "steel": "#8ab2d1",
    "blue": "#4f71be",
    "ink": "#243040",
    "gray": "#6b7280",
    "white": "#ffffff",
}


def add_box(ax, xy, width, height, text, fc, fontsize=9.5, weight="normal"):
    import matplotlib.patches as patches

    box = patches.FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.018,rounding_size=0.07",
        linewidth=1.45,
        edgecolor=PALETTE["ink"],
        facecolor=fc,
    )
    ax.add_patch(box)
    ax.text(
        xy[0] + width / 2,
        xy[1] + height / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        fontweight=weight,
        color=PALETTE["ink"],
        linespacing=1.18,
    )


def add_circle(ax, center, radius, text, fontsize=9.0):
    import matplotlib.patches as patches

    circle = patches.Circle(
        center,
        radius=radius,
        facecolor=PALETTE["white"],
        edgecolor=PALETTE["ink"],
        linewidth=1.45,
    )
    ax.add_patch(circle)
    ax.text(center[0], center[1], text, ha="center", va="center", fontsize=fontsize, color=PALETTE["ink"], fontweight="bold")


def add_arrow(ax, start, end, label="", color=None, rad=0.0, label_offset=(0.0, 0.08)):
    color = color or PALETTE["ink"]
    style = f"arc3,rad={rad}" if rad else "arc3"
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops=dict(
            arrowstyle="-|>",
            lw=1.45,
            color=color,
            shrinkA=3,
            shrinkB=3,
            mutation_scale=12,
            connectionstyle=style,
        ),
    )
    if label:
        ax.text(
            (start[0] + end[0]) / 2 + label_offset[0],
            (start[1] + end[1]) / 2 + label_offset[1],
            label,
            ha="center",
            va="center",
            fontsize=8.2,
            color=color,
        )


def add_polyline_arrow(ax, points, label="", label_xy=None, color=None):
    color = color or PALETTE["ink"]
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    ax.plot(xs[:-1], ys[:-1], color=color, lw=1.35)
    add_arrow(ax, points[-2], points[-1], color=color)
    if label and label_xy:
        ax.text(label_xy[0], label_xy[1], label, ha="center", va="center", fontsize=8.4, color=color)


def main() -> None:
    import matplotlib.pyplot as plt

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(12.0, 5.6), dpi=260)
    ax.set_facecolor(PALETTE["bg"])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis("off")

    ax.text(
        6,
        5.62,
        "CrossScaleP2P3ConsistencyGate (CSGate)",
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold",
        color=PALETTE["ink"],
    )
    ax.text(
        6,
        5.25,
        "High-resolution P2 detail is corrected with adjacent P3 semantic context through a bounded residual path.",
        ha="center",
        va="center",
        fontsize=10.2,
        color=PALETTE["gray"],
    )

    # Feature inputs and projections.
    add_box(ax, (0.45, 3.85), 1.28, 0.72, "P2 feature\n$F_2$", PALETTE["steel"], fontsize=9.8, weight="bold")
    add_box(ax, (0.45, 1.50), 1.28, 0.72, "P3 feature\n$F_3$", PALETTE["green"], fontsize=9.8, weight="bold")
    add_box(ax, (2.15, 3.65), 1.70, 1.05, "P2 local context\nDWConv 3x3\n+ Conv 1x1", PALETTE["mint"], fontsize=8.8)
    add_box(ax, (2.15, 1.30), 1.70, 1.05, "P3 projection\nConv 1x1\n+ upsample", PALETTE["mist"], fontsize=8.8)
    add_arrow(ax, (1.73, 4.21), (2.15, 4.21), "$F_2$")
    add_arrow(ax, (1.73, 1.86), (2.15, 1.86), "$F_3$")

    add_box(ax, (4.35, 3.82), 1.00, 0.78, "$C_2$", PALETTE["white"], fontsize=12.5, weight="bold")
    add_box(ax, (4.35, 1.47), 1.00, 0.78, "$C_3$", PALETTE["white"], fontsize=12.5, weight="bold")
    add_arrow(ax, (3.85, 4.21), (4.35, 4.21))
    add_arrow(ax, (3.85, 1.86), (4.35, 1.86))

    # Gate branch.
    add_circle(ax, (5.95, 3.04), 0.25, "cat", fontsize=8.2)
    add_arrow(ax, (5.35, 4.08), (5.78, 3.20), "$C_2$", rad=-0.12)
    add_arrow(ax, (5.35, 2.00), (5.78, 2.88), "$C_3$", rad=0.12)
    add_box(ax, (6.55, 2.45), 1.72, 1.18, "Consistency gate\n1x1 Conv + SiLU\n5x5 Conv + Sigmoid", PALETTE["peach"], fontsize=8.6)
    add_arrow(ax, (6.20, 3.04), (6.55, 3.04), "$[C_2,C_3]$")
    add_box(ax, (8.75, 2.64), 0.92, 0.80, "$A_{23}$", PALETTE["white"], fontsize=12.5, weight="bold")
    add_arrow(ax, (8.27, 3.04), (8.75, 3.04))

    # Difference and bounded gain.
    add_circle(ax, (5.95, 4.55), 0.31, "$C_2-C_3$", fontsize=8.2)
    add_arrow(ax, (5.25, 4.38), (5.66, 4.56), "$C_2$", rad=0.06, label_offset=(0.0, 0.04))
    add_polyline_arrow(
        ax,
        [(5.05, 1.86), (5.55, 1.86), (5.55, 4.26), (5.68, 4.45)],
        label="$C_3$",
        label_xy=(5.35, 3.18),
        color=PALETTE["ink"],
    )
    add_box(ax, (7.10, 4.45), 1.62, 0.70, "bounded gain\n$\\lambda=\\Delta_{max}\\tanh(\\eta)$", PALETTE["rose"], fontsize=8.5)

    add_circle(ax, (10.25, 3.55), 0.29, r"$\odot$", fontsize=13.0)
    add_arrow(ax, (9.67, 3.05), (10.00, 3.42), "$A_{23}$", rad=0.05, label_offset=(0.06, 0.02))
    add_arrow(ax, (6.25, 4.55), (10.00, 3.64), rad=-0.06)
    add_arrow(ax, (8.72, 4.80), (10.05, 3.74), "$\\lambda$", rad=-0.10, label_offset=(0.05, 0.02))

    # Residual output.
    add_circle(ax, (10.35, 1.72), 0.31, "+", fontsize=15.0)
    add_arrow(ax, (10.25, 3.26), (10.34, 2.03), "correction", label_offset=(0.32, 0.00))
    add_polyline_arrow(
        ax,
        [(0.98, 3.85), (0.22, 3.85), (0.22, 0.82), (10.05, 0.82), (10.30, 1.42)],
        label="identity path $F_2$",
        label_xy=(5.9, 0.62),
        color=PALETTE["gray"],
    )
    add_box(ax, (11.00, 1.30), 0.66, 0.84, "$\\tilde{F}_2$", PALETTE["blue"], fontsize=13.0, weight="bold")
    add_arrow(ax, (10.66, 1.72), (11.00, 1.72))

    ax.text(
        6,
        0.22,
        r"$\tilde{F}_2 = F_2 + \Delta_{max}\tanh(\eta)\, A_{23}\odot(C_2-C_3)$, with $\eta=0$ at initialization",
        ha="center",
        va="center",
        fontsize=10.0,
        color=PALETTE["ink"],
    )

    fig.tight_layout(pad=0.4)
    fig.savefig(OUTPUT, bbox_inches="tight", facecolor=PALETTE["bg"])
    plt.close(fig)
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
