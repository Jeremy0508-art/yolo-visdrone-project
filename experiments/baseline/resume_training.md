# Resume Baseline Training

If training needs to stop because of power loss or shutdown, resume from the last checkpoint:

```powershell
python tools/train_baseline.py --config configs/train/baseline_yolo11n.yaml --resume runs/detect/baseline_yolo11n_visdrone/weights/last.pt
```

Before shutting down, prefer stopping after an epoch has finished. Check the latest checkpoint time:

```powershell
Get-ChildItem runs\detect\baseline_yolo11n_visdrone\weights
```

If the run was started in the background, check whether it is still running:

```powershell
Get-Process -Id 25000
```

To stop the background process before shutdown:

```powershell
Stop-Process -Id 25000
```

At worst, progress within the current unfinished epoch may be lost, but completed epochs are saved in `last.pt`.

