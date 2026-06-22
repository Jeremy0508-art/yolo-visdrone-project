# IEEE Server Resume and Experiment Runbook

Status: operational runbook. Use this only after the server is opened and the current login information is confirmed.

This document defines the safe sequence for resuming IEEE-route experiments on the rented GPU server. It does not contain passwords, keys, or private tokens. Do not commit credentials to the repository.

## Current Experiment Gates

The active IEEE route still needs these server-side or dataset-side gates:

| Gate | Required Artifact | Current Use in Paper |
| --- | --- | --- |
| TOFC VisDrone full training | `runs/detect/yolo11n_p2_tofc_960_visdrone/weights/best.pt` | Candidate method evidence only after complete |
| UAVDT raw dataset placement | `data/raw/UAVDT/` | Cross-dataset validation input |
| UAVDT converted YOLO dataset | `data/processed/uavdt_yolo/images/train` | Required before any UAVDT training |
| UAVDT YOLO11n-960 | `runs/detect/baseline_yolo11n_960_uavdt/weights/best.pt` | Cross-dataset baseline |
| UAVDT YOLO11n-P2-960 | `runs/detect/yolo11n_p2_960_uavdt/weights/best.pt` | Cross-dataset P2 validation |
| UAVDT YOLOv8n-960 | `runs/detect/baseline_yolov8n_960_uavdt/weights/best.pt` | External lightweight reference |
| UAVDT YOLO11s-960 | `runs/detect/baseline_yolo11s_960_uavdt/weights/best.pt` | Capacity reference |
| VisDrone ScaleGate | `runs/detect/yolo11n_p2_scalegate_960_visdrone/weights/best.pt` | New adaptive P2 candidate only after complete |
| UAVDT ScaleGate | `runs/detect/yolo11n_p2_scalegate_960_uavdt/weights/best.pt` | Cross-dataset adaptive P2 candidate only after complete |

No pending gate above can support manuscript claims until the full evidence gate in `paper/IEEE_RESULT_INTEGRATION_PROTOCOL.md` passes.

## Before Opening the Server

Local preflight:

```powershell
git status --short
python tools\run_ieee_audits.py
```

Expected local state before remote work:

- `paper/ieee_submission_dashboard.md` has no missing audit items.
- Pending gates are only dataset/training gates, not broken local files.
- The server queue remains dry-run by default.

## First Server Check After Opening

After the server is opened, confirm the new SSH host, port, user, and preferred authentication method. Then check status before launching anything:

```powershell
.\tools\check_ieee_server_status.ps1 -HostName <host> -Port <port> -User root
python tools\build_ieee_server_progress_report.py
```

If password login is used, run the equivalent SSH command manually or configure a temporary SSH key outside the repository. Never write passwords into scripts or committed files.

## Remote Project Sanity Check

On the server:

```bash
cd /root/autodl-tmp/yolo-visdrone-project
git status --short
git pull
python -m py_compile tools/train_baseline.py tools/evaluate_scale_groups.py tools/evaluate_scale_ap.py
bash tools/run_ieee_server_queue.sh
```

The last command should print dry-run instructions and exit without training. If it starts training, stop and inspect the environment variables.

## Recommended Launch Order

### Step 1: VisDrone TOFC Only

Use this first because it does not depend on UAVDT conversion:

```bash
cd /root/autodl-tmp/yolo-visdrone-project
mkdir -p runs/logs
nohup env RUN_TRAINING=1 RUN_SCALE=1 RUN_UAVDT=0 \
  bash tools/run_ieee_server_queue.sh \
  > runs/logs/ieee_queue_tofc_$(date +%Y%m%d_%H%M%S).log 2>&1 &
```

Monitor:

```bash
tail -f runs/logs/ieee_queue_tofc_*.log
```

This queue should create or skip:

- `runs/detect/yolo11n_p2_tofc_960_visdrone`
- `paper/tables/ieee_scale_results_visdrone.csv` if missing

### Step 2: UAVDT Conversion

Run only after raw UAVDT files are present under `data/raw/UAVDT/`:

```bash
cd /root/autodl-tmp/yolo-visdrone-project
python scripts/convert_uavdt_to_yolo.py
python scripts/check_dataset.py --data-yaml configs/dataset/uavdt.yaml
```

If the converter fails, fix the raw-layout assumption before launching any UAVDT training.

### Step 3: UAVDT Training Queue

Run only after `data/processed/uavdt_yolo/images/train` exists and the dataset checker passes:

```bash
cd /root/autodl-tmp/yolo-visdrone-project
mkdir -p runs/logs
nohup env RUN_TRAINING=1 RUN_UAVDT=1 RUN_SCALE=1 \
  bash tools/run_ieee_server_queue.sh \
  > runs/logs/ieee_queue_uavdt_$(date +%Y%m%d_%H%M%S).log 2>&1 &
```

Expected UAVDT run directories:

- `runs/detect/baseline_yolo11n_960_uavdt`
- `runs/detect/yolo11n_p2_960_uavdt`
- `runs/detect/baseline_yolov8n_960_uavdt`
- `runs/detect/baseline_yolo11s_960_uavdt`

### Step 4: ScaleGate Adaptive P2 Queue

Run only after the current code has been synced to the server and the model
construction check passes. This queue adds the new adaptive P2 candidate and
does not overwrite completed baseline runs:

```bash
cd /root/autodl-tmp/yolo-visdrone-project
bash tools/start_ieee_scalegate_queue.sh
```

To run only the VisDrone ScaleGate experiment and skip UAVDT:

```bash
cd /root/autodl-tmp/yolo-visdrone-project
RUN_UAVDT=0 bash tools/start_ieee_scalegate_queue.sh
```

Expected ScaleGate run directories:

- `runs/detect/yolo11n_p2_scalegate_960_visdrone`
- `runs/detect/yolo11n_p2_scalegate_960_uavdt`

## Local Sync After Completion

Do not sync partial runs into manuscript-facing tables. After a run is expected to be complete:

```powershell
.\tools\sync_ieee_server_results.ps1 -HostName <host> -Port <port> -User root -MinEpochs 100
python tools\run_ieee_audits.py
```

The sync script skips runs that do not meet the completion gate.

## Evidence Intake Order

After a completed sync:

1. Check `paper/ieee_server_progress_report.md`.
2. Check `paper/tables/ieee_experiment_registry.csv`.
3. Regenerate speed/complexity for any new final-model weights.
4. Re-run scale-wise diagnostics for any new final-method candidate.
5. Update result interpretation only after audits pass.
6. Update abstract, title, and conclusion last.

## Stop Conditions

Stop and do not use the result as paper evidence if:

- `results.csv` has fewer than 100 epochs.
- `args.yaml` or `weights/best.pt` is missing.
- The queue log reports a failed experiment.
- UAVDT class mapping or dataset checker output is suspicious.
- TOFC does not improve the relevant evidence over the corresponding P2 baseline and is being considered as positive method evidence.
- ScaleGate has not completed both required runs but is being used for a robustness or accuracy claim.

## What to Ask the User For

Ask the user before server-side work if any of these are missing:

- Current server host and port.
- Authentication method.
- Whether the server has the full project and VisDrone data.
- Whether UAVDT raw data has been uploaded.
- Whether the user approves launching a long-running training queue.
