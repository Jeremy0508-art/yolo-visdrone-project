#!/usr/bin/env bash
set -uo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/root/autodl-tmp/yolo-visdrone-project}"
PYTHON_BIN="${PYTHON_BIN:-/root/miniconda3/bin/python}"
WAIT_PID="${WAIT_PID:-}"

cd "$PROJECT_ROOT" || exit 1
mkdir -p runs/logs

wait_for_existing_run() {
    if [[ -z "$WAIT_PID" ]]; then
        return 0
    fi
    if kill -0 "$WAIT_PID" 2>/dev/null; then
        echo "Waiting for existing training process PID=$WAIT_PID"
        wait "$WAIT_PID" 2>/dev/null || while kill -0 "$WAIT_PID" 2>/dev/null; do sleep 60; done
    else
        echo "WAIT_PID=$WAIT_PID is not running; continuing queue."
    fi
}

run_train() {
    local name="$1"
    local config="$2"
    local weights_path="$3"
    shift 3

    if [[ -f "$weights_path" ]]; then
        echo "Skip $name: found $weights_path"
        return 0
    fi

    local stamp
    local log_path
    stamp="$(date +%Y%m%d_%H%M%S)"
    log_path="runs/logs/train_${name}_${stamp}.log"
    echo "Start $name"
    echo "Config: $config"
    echo "Log: $log_path"

    "$PYTHON_BIN" tools/train_baseline.py --config "$config" "$@" >"$log_path" 2>&1
    local status=$?
    if [[ $status -ne 0 ]]; then
        echo "Experiment failed: $name, status=$status, log=$log_path"
        return $status
    fi
    echo "Finished $name"
}

wait_for_existing_run

run_train \
    "yolo11n_p2_960" \
    "configs/train/yolo11n_p2_960.yaml" \
    "runs/detect/yolo11n_p2_960_visdrone/weights/best.pt" \
    --pretrained-weights yolo11n.pt \
    --pretrained-mode p2 \
    --init-output weights/yolo11n_p2_960_pretrained_init.pt || exit $?

run_train \
    "baseline_yolov8n_960" \
    "configs/train/baseline_yolov8n_960.yaml" \
    "runs/detect/baseline_yolov8n_960_visdrone/weights/best.pt" || exit $?

run_train \
    "baseline_yolo11s_960" \
    "configs/train/baseline_yolo11s_960.yaml" \
    "runs/detect/baseline_yolo11s_960_visdrone/weights/best.pt" || exit $?

run_train \
    "baseline_yolov5n" \
    "configs/train/baseline_yolov5n.yaml" \
    "runs/detect/baseline_yolov5n_visdrone/weights/best.pt" || exit $?

echo "CEA server experiment queue finished."
