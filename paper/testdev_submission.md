# VisDrone Test-Dev Submission Notes

## Official Submission Route

The VisDrone evaluation page states that participants need to register an account, download the dataset/toolkit, and upload result files through the VisDrone website evaluation server.

Source:

```text
https://aiskyeye.com/evaluate/
```

The same page states that result files must follow a predefined format and that the format description is available on the submission/results-format page.

## Official Detection Result Format

For object detection in images, each test image should have one corresponding `.txt` file. All `.txt` files should be placed in the root of a single `.zip` archive.

Each line should be:

```text
<bbox_left>,<bbox_top>,<bbox_width>,<bbox_height>,<score>,<object_category>,<truncation>,<occlusion>
```

For detection results, `truncation` and `occlusion` should be set to `-1`.

Source:

```text
https://aiskyeye.com/evaluate/results-format/
```

## Generated Local Submission

Generated command:

```powershell
python tools/export_visdrone_testdev.py --weights runs/detect/yolo11n_p2_coordatt_960_visdrone_full/weights/best.pt --source data/processed/visdrone_yolo/images/test --imgsz 960 --conf 0.001 --iou 0.7 --max-det 500 --device 0 --output-dir runs/testdev_submit/yolo11n_p2_coordatt_960 --zip-name visdrone_testdev_submit.zip
```

Output:

```text
runs/testdev_submit/yolo11n_p2_coordatt_960/visdrone_testdev_submit.zip
runs/testdev_submit/yolo11n_p2_coordatt_960/manifest.csv
runs/testdev_submit/yolo11n_p2_coordatt_960/txt/
```

Export summary:

```text
Images: 1580
Prediction txt files: 1580
Total detections: 716506
Zip entries: 1580
Nested paths in zip: 0
```

## Important Paper Rule

This local export is only a submission package. It is not an official test-dev metric.

Paper-facing test-dev AP values can be reported only after uploading the zip to the official VisDrone evaluation server and receiving official results. Until then, the paper should report validation-set metrics and describe the test-dev submission package as prepared but not officially evaluated.

## Current Official Platform Status

The official upload/evaluation step is currently blocked by account email verification. Because no official server result has been returned, the paper should not include official test-dev or test-challenge AP values at this stage.
