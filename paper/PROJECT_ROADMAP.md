# YOLO VisDrone Journal Submission Roadmap

## Goal

Prepare this YOLO VisDrone project for a Chinese journal submission, with 《计算机工程与应用》 as the target journal. The work should remain reproducible, evidence-based, and compatible with the existing training, validation, inference, and web demo workflows.

## Non-Negotiable Rules

- Do not invent metrics. Every number used in the paper must come from `runs/`, logs, generated validation outputs, or official VisDrone test-dev feedback.
- Keep existing training, validation, inference, and web workflows runnable.
- Treat smoke tests as engineering checks only. Do not use them as paper conclusions.
- Record every paper-facing experiment with its config, command, output directory, weights, and metric source.

## Confirmed Paper Direction

- Target: 《计算机工程与应用》 journal submission.
- Dataset: VisDrone2019-DET.
- Base model: Ultralytics YOLO11n.
- Main task: UAV aerial small-object detection.
- Main completed comparison chain:
  - YOLO11n baseline.
  - YOLO11n-P2.
  - YOLO11n-P2-CoordAttention.
  - YOLO11n-P2-CoordAttention-960.
- Completed augmentation ablation:
  - Small-object-friendly augmentation based on earlier mosaic closing and smaller scale range.
  - Current config: `configs/train/yolo11n_p2_coordatt_smallobj_aug.yaml`.
  - Key parameters: `close_mosaic: 20`, `scale: 0.35`, plus `copy_paste: 0.1`, `erasing: 0.0`.
  - Best mAP50: 0.32780 at epoch 80.
  - Best mAP50-95: 0.18699 at epoch 74.
- Desired additional evaluation:
  - Speed/latency/FPS benchmark. Completed at `paper/tables/speed_results.csv`.
  - Model complexity table.
  - Per-class metrics. Completed at `paper/tables/per_class_results.csv`.
  - Qualitative and failure-case figures. Figure assets assembled under `paper/figures/` and indexed in `paper/figure_index.md`.
  - VisDrone test-dev official submission if the official evaluation channel is available. Local submission zip prepared; official upload is optional/pending because account email verification is currently unavailable.

## Current Evidence Status

| Experiment | Run Directory | Status | Paper Use |
| --- | --- | --- | --- |
| YOLO11n baseline | `runs/detect/baseline_yolo11n_visdrone` | 100 epochs completed | Main baseline |
| YOLO11n-P2 | `runs/detect/yolo11n_p2_pretrained_visdrone` | 100 epochs completed | Ablation |
| YOLO11n-P2-CoordAttention | `runs/detect/yolo11n_p2_coordatt_visdrone` | 100 epochs completed | Ablation |
| YOLO11n-P2-CoordAttention-960 | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full` | 100 epochs completed | Best completed model |
| YOLO11n-P2-CoordAttention small-object aug | `runs/detect/yolo11n_p2_coordatt_smallobj_aug_visdrone` | 100 epochs completed | Ablation |

## Phases

### Phase 0: Freeze Existing Evidence

- Create `paper/` working area.
- Export current metrics from real `results.csv` files.
- Record experiment protocol and reproducibility commands.

### Phase 1: Complete Paper Tables

- Generate main result table.
- Generate ablation table.
- Generate model complexity table where logs provide parameter/GFLOP evidence.
- Keep source paths beside every table row.

### Phase 2: Run Small-Object Augmentation Experiment

- Train `configs/train/yolo11n_p2_coordatt_smallobj_aug.yaml` for 100 epochs.
- Save logs under `runs/logs/`.
- Add the completed run to paper tables only after `results.csv` exists.
- Status: completed. The run improves over the YOLO11n baseline but does not surpass the YOLO11n-P2 or YOLO11n-P2-CoordAttention best checkpoints.

### Phase 3: Add Speed and Per-Class Evaluation

- Add a speed benchmark script.
- Run all main models under consistent settings.
- Collect per-class validation metrics from logs or new validation runs.
- Speed benchmark status: completed with `tools/benchmark_speed.py`.
- Per-class metric collection status: completed with `tools/collect_per_class_metrics.py`.

### Phase 4: Prepare VisDrone Test-Dev Submission

- Check the current official submission/evaluation process.
- Export predictions in official VisDrone test-dev format.
- Use official metrics only if the official server returns them.
- Status: local zip package generated at `runs/testdev_submit/yolo11n_p2_coordatt_960/visdrone_testdev_submit.zip`.
- Official AP status: optional/pending. The official website currently cannot be used because account email verification is not completing, so no official AP can be reported yet.

### Phase 4.5: Assemble Paper Figures

- Copy training curves, PR curves, normalized confusion matrices, qualitative examples, and failure-case assets into `paper/figures/`.
- Record figure provenance and suggested paper use in `paper/figure_index.md`.
- Status: completed.

### Phase 5: Paper Draft

- Build Chinese paper draft from verified material.
- Include method, experiment setup, ablation analysis, speed/complexity analysis, visualization, and reproducibility.
- Experiment section draft status: first draft completed at `paper/draft_experiment_section.md`.
- Method section draft status: first draft completed at `paper/draft_method_section.md`.
- Manuscript table draft status: first draft completed at `paper/manuscript_tables.md`.
- Introduction and related-work draft status: first draft completed at `paper/draft_intro_related_work.md`.
- Full manuscript skeleton status: first draft completed at `paper/manuscript_draft.md`.
- Reference draft status: first draft completed at `paper/references.md`.
- Manuscript revision notes status: completed at `paper/manuscript_revision_notes.md`.
- Selected figure list status: completed at `paper/selected_figures.md`.
- Polished manuscript draft status: completed at `paper/manuscript_polished.md`.
- Paper workspace README status: completed at `paper/README.md`.
- Evidence audit status: completed at `paper/evidence_audit.md`.
- Submission checklist status: completed at `paper/submission_checklist.md`.
- HTML preview render script status: completed at `tools/render_markdown_preview.py`.
- Figure embedding status: recommended figures embedded in `paper/manuscript_polished.md`; HTML renderer supports image preview.
- Short submission candidate status: completed at `paper/manuscript_submission_candidate.md`.
- Generic LaTeX migration status: completed at `paper/manuscript_submission_candidate.tex`.
- Local LaTeX PDF preview status: completed at `paper/manuscript_submission_candidate.pdf` using `.tools/tectonic/tectonic.exe`.

### Phase 6: Strengthen for Submission

- Reassess the current draft as a starting manuscript rather than a finished submission.
- Add external baseline comparisons and stronger literature positioning.
- Expand discussion around method advantages, failure modes, and accuracy-speed trade-offs.
- Status: started. Plan recorded at `paper/research_strengthening_plan.md`.
- Literature comparison seed table status: completed at `paper/literature_comparison_seed.md`.
- External baseline configs added:
  - `configs/train/baseline_yolov8n.yaml`
  - `configs/train/baseline_yolo11s.yaml`
- Server-side external baseline status:
  - YOLOv8n baseline has completed 100 epochs on the rented GPU server.
  - YOLOv8n logs, weights metadata, per-class metrics, model complexity, and speed benchmark have been copied back and exported into `paper/tables/`.
  - YOLO11s baseline has completed 100 epochs on the rented GPU server.
  - YOLO11s logs, weights metadata, per-class metrics, model complexity, and speed benchmark have been copied back and exported into `paper/tables/`.
  - Current external baselines are recorded as reference comparisons, not as YOLO11n module ablations.

## Immediate Next Actions

1. Follow the master journal plan in `paper/CEA_JOURNAL_MASTER_PLAN.md`.
2. Monitor the server queue and sync only complete 100-epoch fair-comparison results.
3. Audit how YOLOv8n, YOLO11s, YOLO11n-960, and YOLO11n-P2-960 should be discussed fairly against the YOLO11n mainline experiments.
4. Update the manuscript comparison/discussion only with completed and audited results.
5. Expand `paper/manuscript_submission_candidate.tex` into a journal-length submission draft after the fair-comparison results are available.

## Current Run Notes

Small-object augmentation training was launched on 2026-06-08 with:

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_p2_coordatt_smallobj_aug.yaml --pretrained-weights yolo11n.pt --pretrained-mode p2 --init-output weights/yolo11n_p2_coordatt_smallobj_aug_init.pt
```

Initial log files:

```text
runs/logs/yolo11n_p2_coordatt_smallobj_aug_full_20260608_171712.stdout.log
runs/logs/yolo11n_p2_coordatt_smallobj_aug_full_20260608_171712.stderr.log
```

The completed run is recorded at:

```text
runs/detect/yolo11n_p2_coordatt_smallobj_aug_visdrone
```

Paper-facing metrics are generated from:

```text
runs/detect/yolo11n_p2_coordatt_smallobj_aug_visdrone/results.csv
```
