#!/usr/bin/env bash
set -uo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/root/autodl-tmp/yolo-visdrone-project}"
PYTHON_BIN="${PYTHON_BIN:-/root/miniconda3/bin/python}"
RUN_TRAINING="${RUN_TRAINING:-0}"
RUN_UAVDT="${RUN_UAVDT:-0}"
RUN_SCALE="${RUN_SCALE:-1}"
RUN_SCALEGATE="${RUN_SCALEGATE:-0}"
RUN_CSGATE="${RUN_CSGATE:-0}"

if [[ ! -d "$PROJECT_ROOT" && -f "tools/run_ieee_server_queue.sh" ]]; then
    PROJECT_ROOT="$(pwd)"
fi

cd "$PROJECT_ROOT" || exit 1
mkdir -p runs/logs

if [[ "$RUN_TRAINING" != "1" ]]; then
    echo "Dry-run only. Set RUN_TRAINING=1 to launch IEEE training jobs."
    echo "Available actions:"
    echo "  RUN_TRAINING=1 RUN_SCALE=1 ./tools/run_ieee_server_queue.sh"
    echo "  RUN_TRAINING=1 RUN_UAVDT=1 RUN_SCALE=1 ./tools/run_ieee_server_queue.sh"
    echo "  RUN_TRAINING=1 RUN_SCALEGATE=1 ./tools/run_ieee_server_queue.sh"
    echo "  RUN_TRAINING=1 RUN_SCALEGATE=1 RUN_UAVDT=1 ./tools/run_ieee_server_queue.sh"
    echo "  RUN_TRAINING=1 RUN_CSGATE=1 ./tools/run_ieee_server_queue.sh"
    echo "  RUN_TRAINING=1 RUN_CSGATE=1 RUN_UAVDT=1 ./tools/run_ieee_server_queue.sh"
    exit 0
fi

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

run_scale_eval() {
    local output_path="paper/tables/ieee_scale_results_visdrone.csv"
    if [[ "$RUN_SCALE" != "1" ]]; then
        echo "Skip scale evaluation: RUN_SCALE=$RUN_SCALE"
        return 0
    fi
    if [[ -f "$output_path" ]]; then
        echo "Skip scale evaluation: found $output_path"
        return 0
    fi
    "$PYTHON_BIN" tools/evaluate_scale_groups.py \
        --dataset-root data/processed/visdrone_yolo \
        --dataset-name VisDrone2019-DET \
        --split val \
        --targets-csv paper/tables/ieee_scale_eval_targets.csv \
        --output "$output_path" \
        --plot-output paper/figures/scale_analysis/ieee_scale_recall_visdrone.png \
        --device 0
}

run_train \
    "yolo11n_p2_tofc_960_visdrone" \
    "configs/train/yolo11n_p2_tofc_960.yaml" \
    "runs/detect/yolo11n_p2_tofc_960_visdrone/weights/best.pt" \
    --pretrained-weights yolo11n.pt \
    --pretrained-mode p2 \
    --init-output weights/yolo11n_p2_tofc_960_pretrained_init.pt || exit $?

run_scale_eval || exit $?

if [[ "$RUN_SCALEGATE" == "1" ]]; then
    run_train \
        "yolo11n_p2_scalegate_960_visdrone" \
        "configs/train/yolo11n_p2_scalegate_960.yaml" \
        "runs/detect/yolo11n_p2_scalegate_960_visdrone/weights/best.pt" \
        --pretrained-weights yolo11n.pt \
        --pretrained-mode p2 \
        --init-output weights/yolo11n_p2_scalegate_960_pretrained_init.pt || exit $?
fi

if [[ "$RUN_CSGATE" == "1" ]]; then
    run_train \
        "yolo11n_p2_csgate_960_visdrone" \
        "configs/train/yolo11n_p2_csgate_960.yaml" \
        "runs/detect/yolo11n_p2_csgate_960_visdrone/weights/best.pt" \
        --pretrained-weights yolo11n.pt \
        --pretrained-mode p2 \
        --init-output weights/yolo11n_p2_csgate_960_pretrained_init.pt || exit $?
fi

if [[ "$RUN_UAVDT" == "1" ]]; then
    if [[ ! -d "data/processed/uavdt_yolo/images/train" ]]; then
        echo "Missing converted UAVDT dataset. Run scripts/convert_uavdt_to_yolo.py first."
        exit 1
    fi

    run_train \
        "baseline_yolo11n_960_uavdt" \
        "configs/train/baseline_yolo11n_960_uavdt.yaml" \
        "runs/detect/baseline_yolo11n_960_uavdt/weights/best.pt" || exit $?

    run_train \
        "yolo11n_p2_960_uavdt" \
        "configs/train/yolo11n_p2_960_uavdt.yaml" \
        "runs/detect/yolo11n_p2_960_uavdt/weights/best.pt" \
        --pretrained-weights yolo11n.pt \
        --pretrained-mode p2 \
        --init-output weights/yolo11n_p2_960_uavdt_pretrained_init.pt || exit $?

    if [[ "$RUN_SCALEGATE" == "1" ]]; then
        run_train \
            "yolo11n_p2_scalegate_960_uavdt" \
            "configs/train/yolo11n_p2_scalegate_960_uavdt.yaml" \
            "runs/detect/yolo11n_p2_scalegate_960_uavdt/weights/best.pt" \
            --pretrained-weights yolo11n.pt \
            --pretrained-mode p2 \
            --init-output weights/yolo11n_p2_scalegate_960_uavdt_pretrained_init.pt || exit $?
    fi

    if [[ "$RUN_CSGATE" == "1" ]]; then
        run_train \
            "yolo11n_p2_csgate_960_uavdt" \
            "configs/train/yolo11n_p2_csgate_960_uavdt.yaml" \
            "runs/detect/yolo11n_p2_csgate_960_uavdt/weights/best.pt" \
            --pretrained-weights yolo11n.pt \
            --pretrained-mode p2 \
            --init-output weights/yolo11n_p2_csgate_960_uavdt_pretrained_init.pt || exit $?
    fi

    run_train \
        "baseline_yolov8n_960_uavdt" \
        "configs/train/baseline_yolov8n_960_uavdt.yaml" \
        "runs/detect/baseline_yolov8n_960_uavdt/weights/best.pt" || exit $?

    run_train \
        "baseline_yolo11s_960_uavdt" \
        "configs/train/baseline_yolo11s_960_uavdt.yaml" \
        "runs/detect/baseline_yolo11s_960_uavdt/weights/best.pt" || exit $?
fi

echo "IEEE server experiment queue finished."
