# VisDrone Ablation Summary

## Experiment Matrix

| Model | Main Change | Run Directory | Best Weights |
| --- | --- | --- | --- |
| YOLO11n baseline | Original YOLO11n | `runs/detect/baseline_yolo11n_visdrone` | `weights/best.pt` |
| YOLO11n-P2 | Add P2 small-object detection head | `runs/detect/yolo11n_p2_pretrained_visdrone` | `weights/best.pt` |
| YOLO11n-P2-CoordAttention | Add CoordAttention on P4/P5 of P2 model | `runs/detect/yolo11n_p2_coordatt_visdrone` | `weights/best.pt` |

## Final Epoch Metrics

| Model | Precision | Recall | mAP50 | mAP50-95 |
| --- | ---: | ---: | ---: | ---: |
| YOLO11n baseline | 0.45440 | 0.33922 | 0.31985 | 0.18066 |
| YOLO11n-P2 | 0.44771 | 0.35475 | 0.32695 | 0.18689 |
| YOLO11n-P2-CoordAttention | 0.45375 | 0.34961 | 0.32709 | 0.18764 |

## Best Metrics

| Model | Best mAP50 | Best mAP50 Epoch | Best mAP50-95 | Best mAP50-95 Epoch |
| --- | ---: | ---: | ---: | ---: |
| YOLO11n baseline | 0.32153 | 80 | 0.18238 | 79 |
| YOLO11n-P2 | 0.33013 | 86 | 0.19012 | 89 |
| YOLO11n-P2-CoordAttention | 0.33073 | 90 | 0.19044 | 89 |

## Deltas vs Baseline

| Model | Best mAP50 Delta | Best mAP50-95 Delta |
| --- | ---: | ---: |
| YOLO11n-P2 | +0.00860 | +0.00774 |
| YOLO11n-P2-CoordAttention | +0.00920 | +0.00806 |

## Deltas vs YOLO11n-P2

| Model | Best mAP50 Delta | Best mAP50-95 Delta |
| --- | ---: | ---: |
| YOLO11n-P2-CoordAttention | +0.00060 | +0.00032 |

## Conclusion

The P2 detection head is the strongest structural improvement for VisDrone small-object detection. Adding CoordAttention on top of P2 gives a small positive gain over the P2-only model, so it is the current best checkpoint by Best mAP50 and Best mAP50-95.

For the application demo and Flask Web interface, use:

```text
runs/detect/yolo11n_p2_coordatt_visdrone/weights/best.pt
```

## Suggested Next Experiments

- Try a larger input size, such as 960, if GPU memory allows.
- Tune augmentations for VisDrone small objects, especially mosaic closing schedule, copy-paste, and scale range.

CoordAttention experiment details are documented in `experiments/ablations/yolo11n_p2_coordatt_visdrone_summary.md`.
