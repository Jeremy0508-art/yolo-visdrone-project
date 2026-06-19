from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

import yaml
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "paper/datasets/uavdt_conversion_readiness_audit.md"


@dataclass(frozen=True)
class Check:
    area: str
    item: str
    status: str
    evidence: str
    action: str = ""


def read_text(rel_path: str) -> str:
    path = ROOT / rel_path
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def status_label(status: str) -> str:
    return {
        "ready": "READY",
        "pending": "PENDING",
        "missing": "MISSING",
    }[status]


def check_yaml() -> list[Check]:
    path = ROOT / "configs/dataset/uavdt.yaml"
    if not path.exists():
        return [
            Check(
                "Dataset config",
                "UAVDT YAML exists",
                "missing",
                "configs/dataset/uavdt.yaml",
                "Create the UAVDT YOLO data YAML before conversion/training.",
            )
        ]

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    checks = [
        Check(
            "Dataset config",
            "UAVDT YAML exists",
            "ready",
            "configs/dataset/uavdt.yaml",
        )
    ]
    expected_paths = {
        "path": "data/processed/uavdt_yolo",
        "train": "images/train",
        "val": "images/val",
        "test": "images/test",
    }
    for key, expected in expected_paths.items():
        actual = str(data.get(key, ""))
        checks.append(
            Check(
                "Dataset config",
                f"YAML `{key}` path",
                "ready" if actual == expected else "missing",
                actual or "not found",
                "" if actual == expected else f"Set `{key}` to `{expected}`.",
            )
        )

    names = data.get("names", {})
    expected_names = {0: "car", 1: "truck", 2: "bus"}
    normalized = {int(k): str(v) for k, v in names.items()} if isinstance(names, dict) else {}
    checks.append(
        Check(
            "Dataset config",
            "YAML class names",
            "ready" if normalized == expected_names else "missing",
            str(normalized),
            "" if normalized == expected_names else "Use the current UAVDT car/truck/bus class map.",
        )
    )
    return checks


def check_converter_static() -> list[Check]:
    text = read_text("scripts/convert_uavdt_to_yolo.py")
    if not text:
        return [
            Check(
                "Converter",
                "Converter script exists",
                "missing",
                "scripts/convert_uavdt_to_yolo.py",
                "Restore the UAVDT converter.",
            )
        ]
    static_tokens = [
        ("Class map car/truck/bus", "UAVDT_CLASS_MAP"),
        ("Raw ID 1 mapping", "1: 0"),
        ("Raw ID 2 mapping", "2: 1"),
        ("Raw ID 3 mapping", "3: 2"),
        ("Common image folder img1", '"img1"'),
        ("Common annotation gt_whole", '"gt_whole.txt"'),
        ("Unknown class option documented in code", "--include-unknown-classes"),
        ("Fallback split logic", "infer_split"),
    ]
    checks = [
        Check("Converter", "Converter script exists", "ready", "scripts/convert_uavdt_to_yolo.py")
    ]
    for item, token in static_tokens:
        checks.append(
            Check(
                "Converter",
                item,
                "ready" if token in text else "missing",
                token if token in text else "not found",
                "" if token in text else "Update the converter before running UAVDT training.",
            )
        )
    return checks


def run_synthetic_smoke() -> list[Check]:
    with tempfile.TemporaryDirectory(prefix="uavdt_smoke_") as temp:
        temp_root = Path(temp)
        raw_seq = temp_root / "raw" / "UAV0001"
        image_dir = raw_seq / "img1"
        image_dir.mkdir(parents=True)
        for frame in (1, 2):
            Image.new("RGB", (100, 50), color=(32, 64, 96)).save(image_dir / f"{frame:06d}.jpg")
        # frame, target_id, x, y, w, h, out_of_view, class, occlusion...
        (raw_seq / "gt_whole.txt").write_text(
            "\n".join(
                [
                    "1,1,10,5,20,10,0,1,0",
                    "1,2,30,15,10,10,0,2,0",
                    "2,1,40,20,30,15,0,3,0",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        output_root = temp_root / "out"
        result = subprocess.run(
            [
                sys.executable,
                "scripts/convert_uavdt_to_yolo.py",
                "--raw-root",
                str(temp_root / "raw"),
                "--output-root",
                str(output_root),
                "--overwrite",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
            timeout=60,
        )
        if result.returncode != 0:
            return [
                Check(
                    "Synthetic smoke",
                    "Temporary UAVDT conversion",
                    "missing",
                    (result.stdout + "\n" + result.stderr).strip(),
                    "Fix the converter before using real UAVDT data.",
                )
            ]

        label_files = sorted(output_root.glob("labels/*/*.txt"))
        image_files = sorted(output_root.glob("images/*/*.jpg"))
        rows: list[str] = []
        for path in label_files:
            rows.extend(line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
        valid_classes = all(row.split()[0] in {"0", "1", "2"} for row in rows)
        valid_widths = all(len(row.split()) == 5 for row in rows)
        checks = [
            Check(
                "Synthetic smoke",
                "Temporary UAVDT conversion",
                "ready",
                f"{len(image_files)} images, {len(label_files)} labels, {len(rows)} boxes",
            ),
            Check(
                "Synthetic smoke",
                "Converted class IDs stay within car/truck/bus map",
                "ready" if valid_classes else "missing",
                ", ".join(sorted({row.split()[0] for row in rows})) if rows else "no boxes",
                "" if valid_classes else "Check UAVDT class mapping before real conversion.",
            ),
            Check(
                "Synthetic smoke",
                "YOLO label rows have five fields",
                "ready" if valid_widths else "missing",
                "all rows have five fields" if valid_widths else "malformed rows found",
                "" if valid_widths else "Fix YOLO label serialization.",
            ),
        ]
        return checks


def check_docs() -> list[Check]:
    docs = {
        "paper/datasets/uavdt_setup.md": [
            "data/raw/UAVDT",
            "data/processed/uavdt_yolo",
            "configs/dataset/uavdt.yaml",
            "Do not silently merge classes",
        ],
        "paper/datasets/uavdt_operational_checklist.md": [
            "--include-unknown-classes",
            "Class IDs valid",
            "Preview correct",
            "Do not write \"cross-dataset generalization\"",
        ],
        "paper/ieee_server_resume_runbook.md": [
            "UAVDT Conversion",
            "data/raw/UAVDT",
            "data/processed/uavdt_yolo/images/train",
        ],
    }
    checks: list[Check] = []
    for rel_path, tokens in docs.items():
        text = read_text(rel_path)
        checks.append(
            Check(
                "Documentation",
                f"{rel_path} exists",
                "ready" if text else "missing",
                rel_path,
                "" if text else "Restore this UAVDT preparation document.",
            )
        )
        for token in tokens:
            checks.append(
                Check(
                    "Documentation",
                    f"{rel_path} mentions `{token}`",
                    "ready" if token in text else "missing",
                    token if token in text else "not found",
                    "" if token in text else "Add this required UAVDT preparation detail.",
                )
            )
    return checks


def check_current_data_gates() -> list[Check]:
    raw_root = ROOT / "data/raw/UAVDT"
    converted_train = ROOT / "data/processed/uavdt_yolo/images/train"
    return [
        Check(
            "Current data gate",
            "Raw UAVDT root available",
            "ready" if raw_root.exists() else "pending",
            "data/raw/UAVDT",
            "" if raw_root.exists() else "Place or mount the raw UAVDT dataset before conversion.",
        ),
        Check(
            "Current data gate",
            "Converted UAVDT train images available",
            "ready" if converted_train.exists() else "pending",
            "data/processed/uavdt_yolo/images/train",
            "" if converted_train.exists() else "Run conversion and dataset integrity check after raw data is available.",
        ),
    ]


def audit() -> list[Check]:
    checks: list[Check] = []
    checks.extend(check_yaml())
    checks.extend(check_converter_static())
    checks.extend(run_synthetic_smoke())
    checks.extend(check_docs())
    checks.extend(check_current_data_gates())
    return checks


def write_report(checks: list[Check]) -> None:
    total = len(checks)
    ready = sum(1 for c in checks if c.status == "ready")
    pending = sum(1 for c in checks if c.status == "pending")
    missing = sum(1 for c in checks if c.status == "missing")
    lines = [
        "# UAVDT Conversion Readiness Audit",
        "",
        "This report is generated by `tools/check_uavdt_conversion_readiness.py`. It checks the local UAVDT conversion chain without requiring the real UAVDT dataset.",
        "",
        "The synthetic smoke test creates temporary images and annotations outside the repository, runs the converter, and verifies the generated YOLO labels. It does not launch training.",
        "",
        "## Summary",
        "",
        f"- Total checks: {total}",
        f"- Ready: {ready}",
        f"- Pending: {pending}",
        f"- Missing: {missing}",
        "",
        "## Checks",
        "",
        "| Area | Item | Status | Evidence | Action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for check in checks:
        evidence = check.evidence.replace("\n", "<br>")
        lines.append(
            f"| {check.area} | {check.item} | {status_label(check.status)} | `{evidence}` | {check.action} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `READY` means the local configuration, converter, documentation, or smoke test passed.",
            "- `PENDING` means real UAVDT data is still needed before conversion/training can proceed.",
            "- `MISSING` means a local preparation artifact or converter behavior should be fixed before the server queue is used for UAVDT.",
        ]
    )
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks = audit()
    write_report(checks)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
