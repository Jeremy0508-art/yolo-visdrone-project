#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/root/autodl-tmp/yolo-visdrone-project}"
cd "$PROJECT_ROOT"
mkdir -p runs/logs

if pgrep -af "RUN_CSGATE=1|run_ieee_server_queue.sh" | grep -v grep >/dev/null 2>&1; then
    echo "An IEEE queue already appears to be running."
    pgrep -af "RUN_CSGATE=1|run_ieee_server_queue.sh" | grep -v grep || true
    exit 1
fi

stamp="$(date +%Y%m%d_%H%M%S)"
log_path="runs/logs/ieee_csgate_queue_${stamp}.log"
latest_log="runs/logs/ieee_csgate_queue_latest.log"
pid_path="runs/logs/ieee_csgate_queue_latest.pid"

(
    export RUN_TRAINING=1
    export RUN_CSGATE=1
    export RUN_UAVDT=1
    export RUN_SCALE=0
    bash tools/run_ieee_server_queue.sh
) >"$log_path" 2>&1 &

pid=$!
ln -sfn "$(basename "$log_path")" "$latest_log"
printf "%s\n" "$pid" >"$pid_path"

echo "Started CSGate IEEE queue. PID=$pid"
echo "Log: $log_path"
