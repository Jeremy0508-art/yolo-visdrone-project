from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "paper/tables/ieee_experiment_registry.csv"
AUDIT_PATH = ROOT / "paper/ieee_experiment_registry_audit.md"
MIN_EPOCHS = 100


@dataclass(frozen=True)
class RegistryItem:
    experiment_id: str
    dataset: str
    model: str
    input_size: str
    role: str
    config_or_command: str
    run_dir: str
    primary_artifact: str
    paper_use: str
    kind: str = "training"


ITEMS = [
    RegistryItem(
        "vis_yolo11n_640",
        "VisDrone2019-DET",
        "YOLO11n",
        "640",
        "nano baseline",
        "configs/train/baseline_yolo11n.yaml",
        "runs/detect/baseline_yolo11n_visdrone",
        "runs/detect/baseline_yolo11n_visdrone/weights/best.pt",
        "completed VisDrone baseline evidence",
    ),
    RegistryItem(
        "vis_yolo11n_960",
        "VisDrone2019-DET",
        "YOLO11n",
        "960",
        "high-resolution nano baseline",
        "configs/train/baseline_yolo11n_960.yaml",
        "runs/detect/baseline_yolo11n_960_visdrone",
        "runs/detect/baseline_yolo11n_960_visdrone/weights/best.pt",
        "completed fair-resolution baseline evidence",
    ),
    RegistryItem(
        "vis_yolo11n_p2_640",
        "VisDrone2019-DET",
        "YOLO11n-P2",
        "640",
        "P2 ablation",
        "configs/train/yolo11n_p2.yaml",
        "runs/detect/yolo11n_p2_pretrained_visdrone",
        "runs/detect/yolo11n_p2_pretrained_visdrone/weights/best.pt",
        "completed P2 ablation evidence",
    ),
    RegistryItem(
        "vis_yolo11n_p2_960",
        "VisDrone2019-DET",
        "YOLO11n-P2",
        "960",
        "P2 high-resolution ablation",
        "configs/train/yolo11n_p2_960.yaml",
        "runs/detect/yolo11n_p2_960_visdrone",
        "runs/detect/yolo11n_p2_960_visdrone/weights/best.pt",
        "completed fair P2 evidence",
    ),
    RegistryItem(
        "vis_yolo11n_p2_ca_640",
        "VisDrone2019-DET",
        "YOLO11n-P2-CA",
        "640",
        "attention ablation",
        "configs/train/yolo11n_p2_coordatt.yaml",
        "runs/detect/yolo11n_p2_coordatt_visdrone",
        "runs/detect/yolo11n_p2_coordatt_visdrone/weights/best.pt",
        "completed attention ablation evidence",
    ),
    RegistryItem(
        "vis_yolo11n_p2_ca_960",
        "VisDrone2019-DET",
        "YOLO11n-P2-CA",
        "960",
        "attention high-resolution ablation",
        "configs/train/yolo11n_p2_coordatt_960.yaml",
        "runs/detect/yolo11n_p2_coordatt_960_visdrone_full",
        "runs/detect/yolo11n_p2_coordatt_960_visdrone_full/weights/best.pt",
        "completed attention fair-resolution evidence",
    ),
    RegistryItem(
        "vis_yolo11n_p2_ca_smallobjaug",
        "VisDrone2019-DET",
        "YOLO11n-P2-CA-SmallObjAug",
        "640",
        "small-object augmentation ablation",
        "configs/train/yolo11n_p2_coordatt_smallobj_aug.yaml",
        "runs/detect/yolo11n_p2_coordatt_smallobj_aug_visdrone",
        "runs/detect/yolo11n_p2_coordatt_smallobj_aug_visdrone/weights/best.pt",
        "completed augmentation ablation evidence",
    ),
    RegistryItem(
        "vis_yolov5n_640",
        "VisDrone2019-DET",
        "YOLOv5n",
        "640",
        "classic lightweight YOLO reference",
        "configs/train/baseline_yolov5n.yaml",
        "runs/detect/baseline_yolov5n_visdrone",
        "runs/detect/baseline_yolov5n_visdrone/weights/best.pt",
        "completed external baseline evidence",
    ),
    RegistryItem(
        "vis_yolov8n_640",
        "VisDrone2019-DET",
        "YOLOv8n",
        "640",
        "lightweight YOLO reference",
        "configs/train/baseline_yolov8n.yaml",
        "runs/detect/baseline_yolov8n_visdrone",
        "runs/detect/baseline_yolov8n_visdrone/weights/best.pt",
        "completed external baseline evidence",
    ),
    RegistryItem(
        "vis_yolov8n_960",
        "VisDrone2019-DET",
        "YOLOv8n",
        "960",
        "high-resolution YOLOv8n reference",
        "configs/train/baseline_yolov8n_960.yaml",
        "runs/detect/baseline_yolov8n_960_visdrone",
        "runs/detect/baseline_yolov8n_960_visdrone/weights/best.pt",
        "completed fair-resolution external baseline evidence",
    ),
    RegistryItem(
        "vis_yolo11s_640",
        "VisDrone2019-DET",
        "YOLO11s",
        "640",
        "larger-capacity reference",
        "configs/train/baseline_yolo11s.yaml",
        "runs/detect/baseline_yolo11s_visdrone",
        "runs/detect/baseline_yolo11s_visdrone/weights/best.pt",
        "completed capacity reference evidence",
    ),
    RegistryItem(
        "vis_yolo11s_960",
        "VisDrone2019-DET",
        "YOLO11s",
        "960",
        "high-resolution larger-capacity reference",
        "configs/train/baseline_yolo11s_960.yaml",
        "runs/detect/baseline_yolo11s_960_visdrone",
        "runs/detect/baseline_yolo11s_960_visdrone/weights/best.pt",
        "completed capacity reference evidence",
    ),
    RegistryItem(
        "vis_yolo11n_p2_tofc_960",
        "VisDrone2019-DET",
        "YOLO11n-P2-TOFC",
        "960",
        "candidate IEEE new method",
        "configs/train/yolo11n_p2_tofc_960.yaml",
        "runs/detect/yolo11n_p2_tofc_960_visdrone",
        "runs/detect/yolo11n_p2_tofc_960_visdrone/weights/best.pt",
        "locked until complete training evidence exists",
    ),
    RegistryItem(
        "vis_yolo11n_p2_scalegate_960",
        "VisDrone2019-DET",
        "YOLO11n-P2-ScaleGate",
        "960",
        "adaptive P2 gate candidate",
        "configs/train/yolo11n_p2_scalegate_960.yaml",
        "runs/detect/yolo11n_p2_scalegate_960_visdrone",
        "runs/detect/yolo11n_p2_scalegate_960_visdrone/weights/best.pt",
        "new IEEE method candidate locked until complete evidence exists",
    ),
    RegistryItem(
        "vis_yolo11n_p2_csgate_960",
        "VisDrone2019-DET",
        "YOLO11n-P2-CSGate",
        "960",
        "second-cycle cross-scale P2/P3 gate candidate",
        "configs/train/yolo11n_p2_csgate_960.yaml",
        "runs/detect/yolo11n_p2_csgate_960_visdrone",
        "runs/detect/yolo11n_p2_csgate_960_visdrone/weights/best.pt",
        "second-cycle method evidence; use only after post-result audits",
    ),
    RegistryItem(
        "uavdt_yolo11n_960",
        "UAVDT",
        "YOLO11n",
        "960",
        "cross-dataset baseline",
        "configs/train/baseline_yolo11n_960_uavdt.yaml",
        "runs/detect/baseline_yolo11n_960_uavdt",
        "runs/detect/baseline_yolo11n_960_uavdt/weights/best.pt",
        "locked until UAVDT conversion and training complete",
    ),
    RegistryItem(
        "uavdt_yolo11n_p2_960",
        "UAVDT",
        "YOLO11n-P2",
        "960",
        "cross-dataset P2 validation",
        "configs/train/yolo11n_p2_960_uavdt.yaml",
        "runs/detect/yolo11n_p2_960_uavdt",
        "runs/detect/yolo11n_p2_960_uavdt/weights/best.pt",
        "locked until UAVDT conversion and training complete",
    ),
    RegistryItem(
        "uavdt_yolov8n_960",
        "UAVDT",
        "YOLOv8n",
        "960",
        "cross-dataset external baseline",
        "configs/train/baseline_yolov8n_960_uavdt.yaml",
        "runs/detect/baseline_yolov8n_960_uavdt",
        "runs/detect/baseline_yolov8n_960_uavdt/weights/best.pt",
        "locked until UAVDT conversion and training complete",
    ),
    RegistryItem(
        "uavdt_yolo11s_960",
        "UAVDT",
        "YOLO11s",
        "960",
        "cross-dataset capacity reference",
        "configs/train/baseline_yolo11s_960_uavdt.yaml",
        "runs/detect/baseline_yolo11s_960_uavdt",
        "runs/detect/baseline_yolo11s_960_uavdt/weights/best.pt",
        "locked until UAVDT conversion and training complete",
    ),
    RegistryItem(
        "uavdt_yolo11n_p2_scalegate_960",
        "UAVDT",
        "YOLO11n-P2-ScaleGate",
        "960",
        "cross-dataset adaptive P2 gate candidate",
        "configs/train/yolo11n_p2_scalegate_960_uavdt.yaml",
        "runs/detect/yolo11n_p2_scalegate_960_uavdt",
        "runs/detect/yolo11n_p2_scalegate_960_uavdt/weights/best.pt",
        "cross-dataset method gate locked until complete evidence exists",
    ),
    RegistryItem(
        "uavdt_yolo11n_p2_csgate_960_full100",
        "UAVDT",
        "YOLO11n-P2-CSGate",
        "960",
        "strict 100-epoch second-cycle cross-scale gate candidate",
        "configs/train/yolo11n_p2_csgate_960_uavdt_full100.yaml",
        "runs/detect/yolo11n_p2_csgate_960_uavdt_full100",
        "runs/detect/yolo11n_p2_csgate_960_uavdt_full100/weights/best.pt",
        "strict 100-epoch cross-dataset method evidence; use only after post-result audits",
    ),
    RegistryItem(
        "vis_scale_full",
        "VisDrone2019-DET",
        "enabled scale target list",
        "960",
        "full scale-wise analysis",
        "tools/evaluate_scale_groups.py --targets-csv paper/tables/ieee_scale_eval_targets.csv",
        "",
        "paper/tables/ieee_scale_results_visdrone.csv",
        "locked until full scale-wise table and figure exist",
        kind="analysis",
    ),
]


def count_epochs(run_dir: str) -> int:
    results = ROOT / run_dir / "results.csv"
    if not results.exists():
        return 0
    with results.open(newline="", encoding="utf-8-sig") as f:
        return max(0, sum(1 for _ in csv.DictReader(f)))


def status_for(item: RegistryItem) -> tuple[str, int, str]:
    if item.kind == "analysis":
        artifact = ROOT / item.primary_artifact
        if artifact.exists():
            return "complete", 0, f"found {item.primary_artifact}"
        return "pending", 0, f"missing {item.primary_artifact}"

    run_dir = ROOT / item.run_dir
    results = run_dir / "results.csv"
    args = run_dir / "args.yaml"
    best = ROOT / item.primary_artifact
    epochs = count_epochs(item.run_dir)
    missing = [
        rel
        for rel, path in [
            ("run_dir", run_dir),
            ("results.csv", results),
            ("args.yaml", args),
            ("best.pt", best),
        ]
        if not path.exists()
    ]
    if missing:
        return "pending", epochs, "missing " + ",".join(missing)
    if epochs < MIN_EPOCHS:
        return "partial", epochs, f"{epochs}/{MIN_EPOCHS} epochs"
    return "complete", epochs, f"{epochs}/{MIN_EPOCHS} epochs and core artifacts present"


def build_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item in ITEMS:
        status, epochs, evidence = status_for(item)
        rows.append(
            {
                "experiment_id": item.experiment_id,
                "dataset": item.dataset,
                "model": item.model,
                "input_size": item.input_size,
                "role": item.role,
                "config_or_command": item.config_or_command,
                "run_dir": item.run_dir,
                "primary_artifact": item.primary_artifact,
                "status": status,
                "epochs": str(epochs),
                "evidence_summary": evidence,
                "paper_use": item.paper_use,
            }
        )
    return rows


def write_registry(rows: list[dict[str, str]]) -> None:
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "experiment_id",
        "dataset",
        "model",
        "input_size",
        "role",
        "config_or_command",
        "run_dir",
        "primary_artifact",
        "status",
        "epochs",
        "evidence_summary",
        "paper_use",
    ]
    with REGISTRY_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_audit(rows: list[dict[str, str]]) -> None:
    total = len(rows)
    complete = sum(1 for row in rows if row["status"] == "complete")
    partial = sum(1 for row in rows if row["status"] == "partial")
    pending = sum(1 for row in rows if row["status"] == "pending")

    lines = [
        "# IEEE Experiment Registry Audit",
        "",
        "This report is generated by `tools/build_ieee_experiment_registry.py`. It records experiment evidence status without copying metric values into the registry.",
        "",
        "## Summary",
        "",
        f"- Total entries: {total}",
        f"- Complete: {complete}",
        f"- Partial: {partial}",
        f"- Pending: {pending}",
        "",
        "## Entries",
        "",
        "| Experiment | Dataset | Model | Role | Status | Epochs | Evidence |",
        "| --- | --- | --- | --- | --- | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['experiment_id']} | {row['dataset']} | {row['model']} | {row['role']} | {row['status']} | {row['epochs']} | `{row['evidence_summary']}` |"
        )
    lines.extend(
        [
            "",
            "## Evidence Rule",
            "",
            "Only `complete` entries can be used as manuscript evidence. `partial` and `pending` entries may appear in planning documents but must not support final IEEE claims.",
        ]
    )
    AUDIT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = build_rows()
    write_registry(rows)
    write_audit(rows)
    print(f"Wrote {REGISTRY_PATH.relative_to(ROOT)}")
    print(f"Wrote {AUDIT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
