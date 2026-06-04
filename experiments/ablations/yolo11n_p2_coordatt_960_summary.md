# YOLO11n-P2-CoordAttention 960 Summary

## Goal

Evaluate whether increasing the input size from `640` to `960` improves VisDrone small-object detection for the current strongest architecture, `YOLO11n-P2-CoordAttention`.

## Configuration

| Item | Value |
| --- | --- |
| Model config | `configs/models/yolo11n_p2_coordatt.yaml` |
| Train config | `configs/train/yolo11n_p2_coordatt_960.yaml` |
| Dataset | `configs/dataset/visdrone.yaml` |
| Epochs | 100 |
| Image size | 960 |
| Batch size | 4 |
| Device | CUDA device 0 |
| Run directory | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full` |
| Best weights | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full/weights/best.pt` |

## Training

Initial full training started on 2026-05-23 and was resumed on 2026-06-04 from:

```text
runs/detect/yolo11n_p2_coordatt_960_visdrone_full/weights/last.pt
```

Resume command:

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_p2_coordatt_960.yaml --model runs/detect/yolo11n_p2_coordatt_960_visdrone_full/weights/last.pt --resume runs/detect/yolo11n_p2_coordatt_960_visdrone_full/weights/last.pt
```

The resumed run continued from epoch 82 to epoch 100 and completed final validation successfully.

## Final Epoch Metrics

| Epoch | Precision | Recall | mAP50 | mAP50-95 |
| ---: | ---: | ---: | ---: | ---: |
| 100 | 0.53390 | 0.42849 | 0.41732 | 0.24945 |

## Best Metrics

| Metric | Value | Epoch |
| --- | ---: | ---: |
| Best mAP50 | 0.41996 | 90 |
| Best mAP50-95 | 0.25174 | 90 |

## Comparison

| Model | Best mAP50 | Best mAP50-95 |
| --- | ---: | ---: |
| YOLO11n baseline | 0.32153 | 0.18238 |
| YOLO11n-P2 | 0.33013 | 0.19012 |
| YOLO11n-P2-CoordAttention 640 | 0.33073 | 0.19044 |
| YOLO11n-P2-CoordAttention 960 | 0.41996 | 0.25174 |

Compared with the 640 P2+CoordAttention run, the 960 run improves Best mAP50 by `+0.08923` and Best mAP50-95 by `+0.06130`.

## Conclusion

Increasing input size to 960 gives a clear accuracy improvement for VisDrone small-object detection. The tradeoff is higher GPU memory usage, so the 960 checkpoint is the best accuracy-oriented model while the 640 checkpoint remains lighter for constrained deployment.
