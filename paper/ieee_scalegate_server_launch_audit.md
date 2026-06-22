# ScaleGate Server Launch Audit

Generated: 2026-06-21 21:14:41 +08:00

This audit records the launch of the new adaptive P2 candidate experiments for
the IEEE route. It contains no passwords, private keys, or account tokens.

## Purpose

The completed UAVDT evidence blocks a static P2 generalization claim. The next
experiment tests whether an identity-initialized adaptive P2 gate can preserve
the useful VisDrone high-resolution behavior while reducing the UAVDT
degradation observed for YOLO11n-P2-960.

## Remote Launch

| Item | Value |
| --- | --- |
| Remote root | `/root/autodl-tmp/yolo-visdrone-project` |
| Queue script | `tools/start_ieee_scalegate_queue.sh` |
| Queue PID | `79864` |
| Queue log | `runs/logs/ieee_scalegate_queue_latest.log` |
| First run log | `runs/logs/train_yolo11n_p2_scalegate_960_visdrone_20260621_211050.log` |
| First run | `yolo11n_p2_scalegate_960_visdrone` |
| Second run | `yolo11n_p2_scalegate_960_uavdt` |

## Preflight Checks

| Check | Status | Evidence |
| --- | --- | --- |
| SSH access with local key | Passed | `hostname && echo ok` returned the AutoDL container name |
| Remote GPU idle before launch | Passed | RTX 4090 reported 0 MiB used and 0% utilization |
| VisDrone processed data | Passed | `data/processed/visdrone_yolo/images/train` exists |
| UAVDT processed data | Passed | `data/processed/uavdt_yolo/images/train` exists |
| `yolo11n.pt` | Passed | Remote root contains `yolo11n.pt` |
| ScaleGate model build | Passed | `configs/models/yolo11n_p2_scalegate.yaml` builds with 2,895,715 parameters |
| Server queue dry-run | Passed | Queue printed dry-run actions before training |

## Launch Behavior

The queue skips completed TOFC and prior UAVDT baseline runs, then launches:

1. `python tools/train_baseline.py --config configs/train/yolo11n_p2_scalegate_960.yaml --pretrained-weights yolo11n.pt --pretrained-mode p2 --init-output weights/yolo11n_p2_scalegate_960_pretrained_init.pt`
2. `python tools/train_baseline.py --config configs/train/yolo11n_p2_scalegate_960_uavdt.yaml --pretrained-weights yolo11n.pt --pretrained-mode p2 --init-output weights/yolo11n_p2_scalegate_960_uavdt_pretrained_init.pt`

## Initial Runtime Check

The first run started successfully. The log confirms:

- YOLO11-to-P2 compatible pretrained tensors were transferred.
- AMP checks passed.
- VisDrone train/val caches were scanned.
- Training began for 100 epochs.

## Evidence Rule

These runs are progress only until synced back to the local workspace and
audited. ScaleGate must not enter manuscript result tables, abstract,
conclusion, or contribution claims until:

1. `results.csv`, `args.yaml`, and `weights/best.pt` exist for the run.
2. The run reaches 100 epochs.
3. `tools/sync_ieee_server_results.ps1` syncs the completed artifacts.
4. `python tools/run_ieee_audits.py` passes.
5. Speed, complexity, scale-wise recall/precision, and local scale-bin AP are
   refreshed if the run is considered for final-method claims.
