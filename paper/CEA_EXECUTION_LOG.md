# CEA Execution Log

This file records execution status for the `Computer Engineering and Applications`
submission-strengthening stage. It is an audit log, not a manuscript source.

## 2026-06-13

- Active server run: `YOLO11n-960`.
- Run directory: `runs/detect/baseline_yolo11n_960_visdrone`.
- Server log: `runs/logs/train_baseline_yolo11n_960_20260613_220108.log`.
- Server PID observed: `43554`.
- A sequential server queue has been started with `tools/run_cea_server_queue.sh`.
- Queue PID observed: `43842`.
- Queue log: `runs/logs/cea_server_queue_.log`.
- Queued experiments:
  - `YOLO11n-P2-960`
  - `YOLOv8n-960`
  - `YOLO11s-960`
  - `YOLOv5n-640`
- Scale-distribution evidence generated from real YOLO-format VisDrone labels:
  - `paper/tables/object_scale_distribution.csv`
  - `paper/tables/class_scale_distribution.csv`
  - `paper/figures/scale_analysis/object_scale_distribution.png`
- Scale-group prediction matching has been generated from existing validation
  weights:
  - `paper/tables/scale_group_results.csv`
  - `paper/figures/scale_analysis/scale_group_recall.png`
  - command: `python tools/evaluate_scale_groups.py --device 0 --output paper/tables/scale_group_results.csv`
  - default protocol: `conf=0.25`, `IoU=0.5`
- Server-result synchronization script added:
  - `tools/sync_cea_server_results.ps1`
  - command: `.\tools\sync_cea_server_results.ps1 -MinEpochs 100`
  - verified behavior: skips partial runs such as `PARTIAL:3` and regenerates
    paper tables only from local completed artifacts.
- Later status check:
  - `baseline_yolo11n_960_visdrone/results.csv` recorded 6 completed epochs.
  - Last recorded row timestamp on the server: `2026-06-13 22:47:56`.
  - Training PID `43554` was still active and the queue PID `43842` was still
    waiting for subsequent experiments.
  - No 960 fair-comparison result has been copied into paper tables yet because
    the run is still partial.
- Follow-up status check:
  - `baseline_yolo11n_960_visdrone/results.csv` recorded 8 completed epochs.
  - Last recorded row timestamp on the server: `2026-06-13 23:02:19`.
  - Training PID `43554` was still active.
- Follow-up status check:
  - `baseline_yolo11n_960_visdrone/results.csv` recorded 10 completed epochs.
  - Last recorded result row: epoch 10, `mAP50=0.0294104`, `mAP50-95=0.00980345`.
  - Training PID `43554` was still active with elapsed time about 1 hour 22 minutes.
  - Queue PID `43842` was still waiting for subsequent experiments.
  - This is still a partial run and has not been synchronized into paper tables.
- Local paper-material update:
  - Added `paper/CEA_FULL_SUBMISSION_EXECUTION_PLAN.md` as the acceptance-oriented execution plan for the 《计算机工程与应用》 submission track.
  - Updated `paper/README.md` to index the new plan.
  - Replaced stale speed values in Markdown drafts and regenerated HTML previews so they match `paper/tables/speed_results.csv`.
  - Verified that the previously stale latency/FPS values no longer appear in Markdown, LaTeX, or HTML paper files.
  - Ran `python tools/audit_submission_readiness.py`; the audit report was regenerated successfully.
  - Pushed GitHub commit `e1e4b0f` with message `Add CEA full submission execution plan`.
- Latest server status check:
  - `baseline_yolo11n_960_visdrone/results.csv` recorded 11 completed epochs.
  - Training PID `43554` was still active with elapsed time about 1 hour 29 minutes.
  - Queue PID `43842` was still waiting for subsequent experiments.
  - This remains a partial run and has not been synchronized into paper tables.
- Latest server status check:
  - `baseline_yolo11n_960_visdrone/results.csv` recorded 12 completed epochs.
  - Training PID `43554` was still active with elapsed time about 1 hour 32 minutes.
  - Queue PID `43842` was still waiting for subsequent experiments.
  - This remains a partial run and has not been synchronized into paper tables.
- Local integration safeguard update:
  - Added `paper/CEA_RESULT_INTEGRATION_PROTOCOL.md` to define the evidence gate for server results.
  - Updated `tools/audit_submission_readiness.py` so the full submission execution plan, execution log, and integration protocol are part of the readiness audit.
  - Updated `tools/sync_cea_server_results.ps1` so a successful guarded sync also regenerates the readiness audit.
- Latest server status check:
  - `baseline_yolo11n_960_visdrone/results.csv` still recorded 12 completed epochs.
  - Training PID `43554` was still active with elapsed time about 1 hour 34 minutes.
  - Queue PID `43842` was still waiting for subsequent experiments.
  - This remains a partial run and has not been synchronized into paper tables.
- Local manuscript-planning update:
  - Added `paper/CEA_MANUSCRIPT_UPDATE_QUEUE.md` to define the exact manuscript update order after fair-comparison results finish.
  - Updated `tools/audit_submission_readiness.py` so the manuscript update queue is audited.
  - Regenerated `paper/submission_readiness_audit.md`; the audit now checks 39 items, with 5 pending fair experiments and 0 missing items.
- Local server-monitoring update:
  - Added `tools/check_cea_server_status.ps1` to check server-side fair-comparison progress without copying partial runs.
  - Verified the script against the server. It reported `baseline_yolo11n_960_visdrone` as `PARTIAL` with 13 completed epochs, while subsequent queued run directories had not started yet.
  - Training PID `43554` and queue PID `43842` were both still active.
  - No partial metrics were synchronized into paper tables.
- Server status snapshot update:
  - Extended `tools/check_cea_server_status.ps1` to write `paper/cea_server_status_snapshot.md`.
  - Latest generated snapshot reports `baseline_yolo11n_960_visdrone` as `PARTIAL` with 15 completed epochs.
  - Subsequent fair-comparison run directories had not started yet.
  - The snapshot explicitly states that partial or missing runs are progress information only and must not be copied into paper tables.
- Local consistency-audit update:
  - Added `tools/check_paper_consistency.py` to scan manuscript-facing files and paper tables for stale speed values, placeholders, missing table rows, and traceability gaps.
  - Generated `paper/paper_consistency_audit.md`.
  - Current consistency audit result: 13 checks, 13 ready, 0 partial, 0 missing.
  - Updated `tools/audit_submission_readiness.py` so the consistency audit script is included in readiness checks.
  - Current readiness audit result: 44 checks, 5 pending fair experiments, 0 missing items.
- Local PDF-build update:
  - Added `tools/build_paper_pdf.ps1` to compile `paper/manuscript_submission_candidate.tex` with the bundled Tectonic engine when available, falling back to `xelatex` if installed.
  - Rebuilt `paper/manuscript_submission_candidate.pdf` successfully.
  - Extended `tools/check_paper_consistency.py` with a PDF freshness check so the compiled PDF must not be older than the LaTeX source.
  - Current consistency audit result: 14 checks, 14 ready, 0 partial, 0 missing.
  - Current readiness audit result: 45 checks, 5 pending fair experiments, 0 missing items.
- Submission-readiness planning update:
  - Added `paper/CEA_SUBMISSION_READINESS_100_PLAN.md` as the active execution plan for reaching formal 《计算机工程与应用》 submission readiness.
  - The plan defines submission-readiness as complete materials, fair experiments, traceable evidence, journal-style manuscript structure, and GitHub presentation quality; it does not promise journal acceptance.
  - Updated `paper/README.md` so the new plan is visible in the paper workspace index.
  - Updated `tools/audit_submission_readiness.py` so the new plan is checked in every readiness audit.
- Latest server status check:
  - `baseline_yolo11n_960_visdrone/results.csv` recorded 16 completed epochs.
  - Latest partial row: epoch 16, `mAP50=0.0283814`, `mAP50-95=0.00946048`.
  - Training PID `43554` and queue PID `43842` were still active.
  - This remains a partial run and has not been synchronized into paper tables.
- Journal-style benchmark update:
  - Added `paper/CEA_JOURNAL_STYLE_BENCHMARK.md` to translate CEA-style YOLO small-object paper patterns into manuscript and experiment requirements.
  - Added Chinese-journal candidate references to `paper/reference_verification_matrix.md`.
  - Updated `paper/README.md` and `tools/audit_submission_readiness.py` so the benchmark checklist is indexed and audited.
- Latest server status check:
  - `baseline_yolo11n_960_visdrone/results.csv` recorded 17 completed epochs.
  - Latest partial row: epoch 17, `mAP50=0.0281632`, `mAP50-95=0.00938772`.
  - Training PID `43554` and queue PID `43842` were still active.
  - This remains a partial run and has not been synchronized into paper tables.
- Journal manuscript rewrite blueprint update:
  - Added `paper/CEA_MANUSCRIPT_REWRITE_BLUEPRINT.md` to map the current LaTeX candidate into a full journal manuscript structure.
  - The blueprint defines section expansion, figure/table placement, result-dependent rewrite order, and statements that must wait for fair-comparison evidence.
  - Updated `paper/README.md` and `tools/audit_submission_readiness.py` so the blueprint is indexed and audited.

## Evidence Rules

- Do not copy queued experiment values into the manuscript until `results.csv`,
  `args.yaml`, weights and logs have been copied back and audited.
- Do not use official VisDrone test-dev numbers unless they come from a returned
  official evaluation result.
- Do not describe `scale_group_results.csv` as official AP; it is a thresholded
  prediction-matching analysis by GT object scale.
