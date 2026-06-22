from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "paper/figures/method/scalegate_schematic.png"


def add_box(ax, xy, width, height, text, fc, ec="#1f2937", fontsize=9):
    import matplotlib.patches as patches

    box = patches.FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.04",
        linewidth=1.4,
        edgecolor=ec,
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
        color="#111827",
        fontweight="bold" if "\n" not in text else "normal",
    )


def add_arrow(ax, start, end, text: str = ""):
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops=dict(arrowstyle="-|>", lw=1.4, color="#374151", shrinkA=4, shrinkB=4),
    )
    if text:
        ax.text(
            (start[0] + end[0]) / 2,
            (start[1] + end[1]) / 2 + 0.04,
            text,
            ha="center",
            va="bottom",
            fontsize=8,
            color="#4b5563",
        )


def main() -> None:
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(9.2, 4.2), dpi=220)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.4)
    ax.axis("off")

    add_box(ax, (0.25, 1.75), 1.25, 0.9, "P2 feature\n$F_2$", "#dbeafe")
    add_box(ax, (2.0, 1.65), 1.7, 1.1, "Local context\nDWConv 3x3\n+ Conv 1x1", "#dcfce7", fontsize=8.5)
    add_box(ax, (4.35, 2.75), 1.65, 0.75, "Channel gate\nGAP + MLP", "#fef3c7", fontsize=8.5)
    add_box(ax, (4.35, 1.0), 1.65, 0.75, "Spatial gate\nAvg/Max + Conv", "#fef3c7", fontsize=8.5)
    add_box(ax, (6.55, 1.85), 1.2, 0.75, "Gate\n$M_2$", "#ede9fe")
    add_box(ax, (8.15, 2.65), 1.25, 0.65, "Bounded gain\n$\\Delta_{max}\\tanh\\gamma$", "#fee2e2", fontsize=8)
    add_box(ax, (8.05, 1.25), 1.45, 0.8, "Residual add\n$\\hat{F}_2$", "#e0f2fe")

    add_arrow(ax, (1.5, 2.2), (2.0, 2.2))
    add_arrow(ax, (3.7, 2.25), (4.35, 3.12), "$L_2$")
    add_arrow(ax, (3.7, 2.05), (4.35, 1.38), "$L_2$")
    add_arrow(ax, (6.0, 3.12), (6.55, 2.35), "$G_c$")
    add_arrow(ax, (6.0, 1.38), (6.55, 2.05), "$G_s$")
    add_arrow(ax, (7.75, 2.2), (8.05, 1.72), "$L_2 \\odot M_2$")
    add_arrow(ax, (8.8, 2.65), (8.8, 2.05), "$\\delta$")
    add_arrow(ax, (1.5, 1.95), (8.05, 1.55), "identity path")

    ax.text(
        5.0,
        4.05,
        "ScaleAwareP2Gate: identity-initialized bounded modulation for high-resolution P2 features",
        ha="center",
        va="center",
        fontsize=11,
        fontweight="bold",
        color="#111827",
    )
    ax.text(
        5.0,
        0.35,
        "$\\hat{F}_2 = F_2 + \\Delta_{max}\\tanh(\\gamma) \\cdot L_2 \\odot M_2$, with $\\gamma=0$ at initialization",
        ha="center",
        va="center",
        fontsize=9.2,
        color="#374151",
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout(pad=0.3)
    fig.savefig(OUTPUT, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
