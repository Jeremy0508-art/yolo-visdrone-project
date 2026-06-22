# IEEE CSGate Server Launch Audit

Generated after the ScaleGate post-result decision rejected ScaleGate as the
main method. This file records the second-cycle CSGate launch evidence only; it
does not contain completed metrics and must not be used as a result source.

## Summary

- Candidate: `YOLO11n-P2-CSGate-960`
- Method source: `src/models/attention/cross_scale_p2_p3_gate.py`
- Model config: `configs/models/yolo11n_p2_csgate.yaml`
- VisDrone config: `configs/train/yolo11n_p2_csgate_960.yaml`
- UAVDT config: `configs/train/yolo11n_p2_csgate_960_uavdt.yaml`
- Remote root: `/root/autodl-tmp/yolo-visdrone-project`
- Server: `connect.bjb3.seetacloud.com:24476`
- Launch script: `tools/start_ieee_csgate_queue.sh`
- Queue PID at launch: `110612`
- Queue log: `runs/logs/ieee_csgate_queue_20260622_152856.log`
- First run log: `runs/logs/train_yolo11n_p2_csgate_960_visdrone_20260622_152856.log`

## Remote Build Smoke Test

The remote model parser successfully built `configs/models/yolo11n_p2_csgate.yaml`.

```text
YOLO11n_p2_csgate summary: 399 layers, 3,036,185 parameters, 3,036,169 gradients, 14.6 GFLOPs
params 3036185
```

## Launch Evidence

The guarded queue skipped the completed TOFC run and started the missing
VisDrone CSGate run:

```text
Skip yolo11n_p2_tofc_960_visdrone: found runs/detect/yolo11n_p2_tofc_960_visdrone/weights/best.pt
Skip scale evaluation: RUN_SCALE=0
Start yolo11n_p2_csgate_960_visdrone
Config: configs/train/yolo11n_p2_csgate_960.yaml
Log: runs/logs/train_yolo11n_p2_csgate_960_visdrone_20260622_152856.log
```

The first training log confirms pretrained remapping and a normal training
start:

```text
Transferred 288 tensors from /root/autodl-tmp/yolo-visdrone-project/yolo11n.pt with YOLO11-to-P2 remapping.
Saved remapped initialization checkpoint to /root/autodl-tmp/yolo-visdrone-project/weights/yolo11n_p2_csgate_960_pretrained_init.pt
YOLO11n_p2_csgate summary: 399 layers, 3,036,185 parameters, 3,036,169 gradients, 14.6 GFLOPs
Transferred 619/619 items from pretrained weights
Starting training for 100 epochs...
```

## Claim Boundary

- CSGate has no VisDrone or UAVDT performance claim yet.
- Partial epochs are progress evidence only.
- Paper-facing tables may include CSGate only after complete synced runs,
  refreshed diagnostics, and audits.
