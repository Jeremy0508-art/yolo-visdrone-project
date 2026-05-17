# VisDrone Ablation Summary

## Experiment Matrix

| Model | Main Change | Run Directory | Best Weights |
| --- | --- | --- | --- |
| YOLO11n baseline | Original YOLO11n | `runs/detect/baseline_yolo11n_visdrone` | `weights/best.pt` |
| YOLO11n-ECA | Add ECA attention on P3/P4/P5 | `runs/detect/yolo11n_eca_pretrained_adamw_visdrone` | `weights/best.pt` |
| YOLO11n-P2 | Add P2 small-object detection head | `runs/detect/yolo11n_p2_pretrained_visdrone` | `weights/best.pt` |

## Final Epoch Metrics

| Model | Precision | Recall | mAP50 | mAP50-95 |
| --- | ---: | ---: | ---: | ---: |
| YOLO11n baseline | 0.45440 | 0.33922 | 0.31985 | 0.18066 |
| YOLO11n-ECA | 0.43047 | 0.32856 | 0.30236 | 0.17121 |
| YOLO11n-P2 | 0.44771 | 0.35475 | 0.32695 | 0.18689 |

## Best Metrics

| Model | Best mAP50 | Best mAP50 Epoch | Best mAP50-95 | Best mAP50-95 Epoch |
| --- | ---: | ---: | ---: | ---: |
| YOLO11n baseline | 0.32153 | 80 | 0.18238 | 79 |
| YOLO11n-ECA | 0.30417 | 78 | 0.17239 | 88 |
| YOLO11n-P2 | 0.33013 | 86 | 0.19012 | 89 |

## Deltas vs Baseline

| Model | Best mAP50 Delta | Best mAP50-95 Delta |
| --- | ---: | ---: |
| YOLO11n-ECA | -0.01736 | -0.00999 |
| YOLO11n-P2 | +0.00860 | +0.00774 |

## Conclusion

The P2 detection head is the strongest current improvement. It improves both mAP50 and mAP50-95 over the YOLO11n baseline, while the standalone ECA attention variant reduces performance under the current training setup.

For the application demo and Flask Web interface, use:

```text
runs/detect/yolo11n_p2_pretrained_visdrone/weights/best.pt
```

## Suggested Next Experiments

- Combine P2 with ECA to test whether channel attention helps after adding the high-resolution detection head.
- Try a larger input size, such as 960, if GPU memory allows.
- Tune augmentations for VisDrone small objects, especially mosaic closing schedule, copy-paste, and scale range.

