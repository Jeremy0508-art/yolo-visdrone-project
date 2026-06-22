# ScaleGate Post-Result Integration Protocol

This protocol defines the exact steps to follow after the server finishes the
ScaleGate VisDrone and UAVDT experiments. It is a guardrail: no ScaleGate
accuracy, robustness, or IEEE contribution claim is allowed before these steps
produce complete audited evidence.

For the current state, use the generated dynamic runbook:

```powershell
python tools\build_ieee_scalegate_post_result_runbook.py
```

The generated file is `paper/ieee_scalegate_post_result_runbook.md`. It reports
whether the next allowed action is monitoring, guarded sync, diagnostics, or
manuscript decision. It never authorizes partial-result manuscript use.

The safest single entry point is:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\intake_ieee_scalegate_results.ps1
```

Before the two remote ScaleGate runs are complete, this script exits without
syncing files. After remote completion, it performs guarded sync and refreshes
audits. Add `-RunDiagnostics` only after the local result gate opens.

## Completion Gate

A ScaleGate run is complete only when all of the following are true locally
after synchronization:

| Run | Required artifacts |
| --- | --- |
| `runs/detect/yolo11n_p2_scalegate_960_visdrone` | `results.csv`, `args.yaml`, `weights/best.pt`, 100 epochs |
| `runs/detect/yolo11n_p2_scalegate_960_uavdt` | `results.csv`, `args.yaml`, `weights/best.pt`, 100 epochs |

Partial rows in `results.csv` are progress evidence only. They must not enter
the abstract, conclusion, contribution list, final comparison table, or cover
letter.

## Step 1: Check Server Status

```powershell
.\tools\check_ieee_server_status.ps1 `
  -HostName connect.bjb3.seetacloud.com `
  -Port 24476 `
  -User root `
  -IdentityFile "$env:USERPROFILE\.ssh\autodl_yolo_visdrone"
```

Expected before sync:

- `yolo11n_p2_scalegate_960_visdrone` is `READY`.
- `yolo11n_p2_scalegate_960_uavdt` is `READY`.
- No connection failure is reported.

## Step 2: Sync Complete Runs

```powershell
.\tools\sync_ieee_server_results.ps1 `
  -HostName connect.bjb3.seetacloud.com `
  -Port 24476 `
  -User root `
  -IdentityFile "$env:USERPROFILE\.ssh\autodl_yolo_visdrone" `
  -MinEpochs 100
```

The sync script copies only complete runs. If either ScaleGate run remains
partial, do not manually copy it into `runs/detect/`.

The wrapper `tools/intake_ieee_scalegate_results.ps1` calls the same guarded
sync script only after the generated runbook allows it.

## Step 3: Refresh Result Tables

```powershell
python tools\export_paper_tables.py
python tools\export_ieee_uavdt_results.py
python tools\check_ieee_scalegate_result_gate.py
python tools\check_ieee_scalegate_method_decision.py
python tools\run_ieee_audits.py
```

Expected after this step:

- `paper/tables/main_comparison_for_paper.csv` contains a ScaleGate VisDrone
  row only if the VisDrone run is complete.
- `paper/tables/ieee_uavdt_results_status.csv` contains the ScaleGate UAVDT
  status.
- `paper/tables/ieee_uavdt_results_for_paper.csv` contains the ScaleGate UAVDT
  row only if the UAVDT run is complete.
- `paper/ieee_scalegate_result_gate_audit.md` reports
  `OPEN_FOR_POST_RESULT_INTEGRATION` only after the local completion gate has
  opened. If it remains locked, do not update the abstract, conclusion, final
  comparison table, or cover letter with ScaleGate performance claims.
- `paper/ieee_scalegate_method_decision_audit.md` applies the pre-result A/B/C
  acceptance routes. If no route passes, do not promote ScaleGate into the
  title, abstract, contribution list, or conclusion as the main proposed
  method.

## Step 4: Enable Scale Diagnostics

Enable the ScaleGate row in `paper/tables/ieee_scale_eval_targets.csv` only
after the complete VisDrone `best.pt` has been synced. Use the guarded helper
instead of editing the CSV by hand:

Then run:

```powershell
python tools\set_ieee_scalegate_scale_target.py --apply

python tools\evaluate_scale_groups.py `
  --targets-csv paper/tables/ieee_scale_eval_targets.csv `
  --output paper/tables/ieee_scale_results_visdrone.csv `
  --plot-output paper/figures/scale_analysis/ieee_scale_recall_visdrone.png `
  --device 0

python tools\evaluate_scale_ap.py `
  --targets-csv paper/tables/ieee_scale_eval_targets.csv `
  --output paper/tables/ieee_scale_ap_results_visdrone.csv `
  --plot-output paper/figures/scale_analysis/ieee_scale_ap50_visdrone.png `
  --device 0
```

These diagnostics are local scale-bin measurements. They must not be described
as official COCO AP-small or official VisDrone small-object AP.

## Step 5: Refresh Speed And Complexity

Run the speed benchmark on one consistent hardware setup:

```powershell
python tools\benchmark_speed.py `
  --warmup 10 `
  --samples 100 `
  --output paper/tables/speed_results.csv
```

The benchmark script skips ScaleGate until its VisDrone `best.pt` exists. Once
the weight is synced, it will include the ScaleGate row automatically.

## Step 6: Apply Method Selection Rules

After tables and diagnostics are refreshed, apply
`paper/ieee_method_selection_protocol.md`.

ScaleGate can become the final proposed method only if the completed evidence
supports one of the documented acceptance routes. If it fails these routes, it
must remain an exploratory or negative ablation and the paper should be
redesigned again rather than forcing an unsupported contribution.

The generated companion check is:

```powershell
python tools\check_ieee_scalegate_method_decision.py
```

Use `paper/ieee_scalegate_method_decision_audit.md` as the decision record.

## Step 7: Manuscript Update Lock

Only after Steps 1-6 pass:

- update `paper/ieee_trans/section_draft_pack.md`;
- update `paper/ieee_trans/main_draft.tex`;
- regenerate IEEE tables with `python tools\export_ieee_tables.py`;
- compile `paper/ieee_trans/main_draft.pdf`;
- run `python tools\run_ieee_audits.py`.

Do not create final `paper/ieee_trans/main.tex` until advisor metadata, target
journal, reference metadata, and code/data release boundaries are confirmed.
