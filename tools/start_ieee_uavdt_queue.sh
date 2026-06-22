#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/root/autodl-tmp/yolo-visdrone-project}"
PYTHON_BIN="${PYTHON_BIN:-/root/miniconda3/bin/python}"
LOG_PATH="${LOG_PATH:-runs/logs/ieee_uavdt_queue_latest.log}"
PID_PATH="${PID_PATH:-runs/logs/ieee_uavdt_queue_latest.pid}"

cd "$PROJECT_ROOT"
mkdir -p runs/logs

if pgrep -af "tools/run_ieee_server_queue.sh" | grep -q "RUN_UAVDT=1"; then
    echo "A UAVDT IEEE queue already appears to be running."
    pgrep -af "tools/run_ieee_server_queue.sh"
    exit 0
fi

nohup env \
    PROJECT_ROOT="$PROJECT_ROOT" \
    PYTHON_BIN="$PYTHON_BIN" \
    RUN_TRAINING=1 \
    RUN_UAVDT=1 \
    RUN_SCALE=0 \
    bash tools/run_ieee_server_queue.sh >"$LOG_PATH" 2>&1 &

pid=$!
echo "$pid" >"$PID_PATH"
echo "Started UAVDT IEEE queue. PID=$pid"
echo "Log: $PROJECT_ROOT/$LOG_PATH"
