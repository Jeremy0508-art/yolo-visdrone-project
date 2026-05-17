# Baseline vs YOLO11n-ECA Comparison

## Experiment Setup

| Item | Baseline | ECA Variant |
| --- | --- | --- |
| Model | YOLO11n | YOLO11n + ECAAttention |
| Dataset | VisDrone DET | VisDrone DET |
| Epochs | 100 | 100 |
| Image size | 640 | 640 |
| Batch size | 8 | 8 |
| Optimizer | Ultralytics baseline config | AdamW |
| Run directory | `runs/detect/baseline_yolo11n_visdrone` | `runs/detect/yolo11n_eca_pretrained_adamw_visdrone` |
| Best weights | `weights/best.pt` | `weights/best.pt` |

## Final Epoch Metrics

| Metric | Baseline | ECA | Delta |
| --- | ---: | ---: | ---: |
| Precision | 0.45440 | 0.43047 | -0.02393 |
| Recall | 0.33922 | 0.32856 | -0.01066 |
| mAP50 | 0.31985 | 0.30236 | -0.01749 |
| mAP50-95 | 0.18066 | 0.17121 | -0.00945 |

## Best Metrics

| Metric | Baseline | ECA | Delta |
| --- | ---: | ---: | ---: |
| Best mAP50 | 0.32153 | 0.30417 | -0.01736 |
| Best mAP50-95 | 0.18238 | 0.17239 | -0.00999 |
| Best mAP50 epoch | 80 | 78 | - |
| Best mAP50-95 epoch | 79 | 88 | - |

## Conclusion

The standalone ECA insertion did not improve the YOLO11n baseline on VisDrone under the current training setup. The final and best metrics are consistently lower than the baseline, especially on mAP50 and mAP50-95.

This is still a useful ablation result: channel attention alone is not enough for this small-object-heavy aerial detection task. The next improvement should focus on preserving and detecting higher-resolution features.

## Next Experiment

Recommended next variant:

- Add a P2 small-object detection head.
- Keep the current VisDrone conversion and training pipeline unchanged.
- Compare `YOLO11n`, `YOLO11n-ECA`, and `YOLO11n-P2` under the same metric table.

Optional later variants:

- `YOLO11n-P2-ECA`
- Higher input size, such as 960 or 1024, if GPU memory allows.
- Small-object-focused augmentation tuning.

