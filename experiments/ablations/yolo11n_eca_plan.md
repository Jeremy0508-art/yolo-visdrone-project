# YOLO11n-ECA Experiment Plan

## Goal

Evaluate whether adding Efficient Channel Attention improves VisDrone small-object detection compared with the YOLO11n baseline.

## Baseline

- Model: YOLO11n
- Final mAP50: 0.31985
- Final mAP50-95: 0.18066
- Best mAP50: 0.32153
- Best mAP50-95: 0.18238

## Variant

- Model config: `configs/models/yolo11n_eca.yaml`
- Train config: `configs/train/yolo11n_eca.yaml`
- Added modules: `ECAAttention`
- Insert positions: before Detect on P3, P4, and P5 feature maps

## Command

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_eca.yaml
```

## Comparison Metrics

- Precision
- Recall
- mAP50
- mAP50-95
- Per-class AP, especially pedestrian, people, bicycle, tricycle, motor

## Notes

This first ECA variant trains from the YAML architecture. If needed, a later experiment can add partial pretrained weight transfer from the baseline YOLO11n checkpoint.
The ECA experiment uses `optimizer: AdamW` because Ultralytics `optimizer=auto` may select MuSGD, which is incompatible with the ECA Conv1d parameter shape in this environment.

## Smoke Test

The ECA model build and training pipeline have been verified.

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_eca.yaml --epochs 1 --fraction 0.01 --batch 8 --workers 0 --device 0 --name smoke_yolo11n_eca_visdrone
```

- Output: `runs/detect/smoke_yolo11n_eca_visdrone`
- Result: completed successfully
- Note: metrics are zero because this is a 1-epoch, 1%-data smoke test from a newly initialized architecture.

## Full Training Command

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_eca.yaml --pretrained-weights yolo11n.pt --init-output weights/yolo11n_eca_pretrained_init.pt --name yolo11n_eca_pretrained_adamw_visdrone
```

This command first remaps compatible YOLO11n pretrained tensors into the YOLO11n-ECA architecture, saves the initialization checkpoint, and then starts training from that checkpoint.

## Pretrained Smoke Test

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_eca.yaml --pretrained-weights yolo11n.pt --init-output weights/yolo11n_eca_pretrained_init.pt --epochs 1 --fraction 0.01 --batch 8 --workers 0 --device 0 --name smoke_yolo11n_eca_pretrained_init_visdrone
```

- Transferred tensors from YOLO11n: 448
- Loaded tensors from remapped initialization checkpoint: 502/502
- Output: `runs/detect/smoke_yolo11n_eca_pretrained_init_visdrone`
- Result: completed successfully

## Full Training Result

- Run directory: `runs/detect/yolo11n_eca_pretrained_adamw_visdrone`
- Weights: `runs/detect/yolo11n_eca_pretrained_adamw_visdrone/weights/best.pt`
- Epochs completed: 100
- Final precision: 0.43047
- Final recall: 0.32856
- Final mAP50: 0.30236
- Final mAP50-95: 0.17121
- Best mAP50: 0.30417 at epoch 78
- Best mAP50-95: 0.17239 at epoch 88

## Ablation Conclusion

The standalone ECA variant did not outperform the YOLO11n baseline on VisDrone.

Compared with the baseline best metrics:

- Best mAP50 changed from 0.32153 to 0.30417.
- Best mAP50-95 changed from 0.18238 to 0.17239.

This result suggests that channel attention alone is not the most effective first improvement for VisDrone small-object detection. The next experiment should prioritize a P2 small-object detection head.
