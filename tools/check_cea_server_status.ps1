param(
    [string]$HostName = "connect.bjb2.seetacloud.com",
    [int]$Port = 44733,
    [string]$User = "root",
    [string]$IdentityFile = "$env:USERPROFILE\.ssh\autodl_yolo_visdrone",
    [string]$RemoteRoot = "/root/autodl-tmp/yolo-visdrone-project",
    [int]$MinEpochs = 100,
    [int]$TrainPid = 43554,
    [int]$QueuePid = 43842,
    [string[]]$RunNames = @(
        "baseline_yolo11n_960_visdrone",
        "yolo11n_p2_960_visdrone",
        "baseline_yolov8n_960_visdrone",
        "baseline_yolo11s_960_visdrone",
        "baseline_yolov5n_visdrone"
    )
)

$ErrorActionPreference = "Stop"

$sshTarget = "$User@$HostName"
$sshArgs = @(
    "-i", $IdentityFile,
    "-p", "$Port",
    "-o", "StrictHostKeyChecking=no",
    "-o", "ConnectTimeout=10",
    $sshTarget
)
$scpArgs = @(
    "-i", $IdentityFile,
    "-P", "$Port",
    "-o", "StrictHostKeyChecking=no",
    "-o", "ConnectTimeout=10"
)

$remoteScript = @'
remote_root="$1"
min_epochs="$2"
train_pid="$3"
queue_pid="$4"
shift 4

cd "$remote_root" || exit 1

printf "REMOTE_ROOT|%s\n" "$remote_root"
printf "MIN_EPOCHS|%s\n" "$min_epochs"

for run_name in "$@"; do
  run_dir="runs/detect/$run_name"
  results="$run_dir/results.csv"
  args="$run_dir/args.yaml"
  best="$run_dir/weights/best.pt"

  if [ ! -f "$results" ]; then
    printf "RUN|%s|MISSING|0||||%s|%s\n" "$run_name" "$args" "$best"
    continue
  fi

  lines=$(wc -l < "$results")
  epochs=$((lines - 1))
  last=$(tail -1 "$results")
  last_epoch=$(printf "%s" "$last" | cut -d, -f1)
  final_map50=$(printf "%s" "$last" | cut -d, -f13)
  final_map5095=$(printf "%s" "$last" | cut -d, -f14)
  if [ "$epochs" -ge "$min_epochs" ]; then
    status="READY"
  else
    status="PARTIAL"
  fi

  printf "RUN|%s|%s|%s|%s|%s|%s|%s|%s\n" "$run_name" "$status" "$epochs" "$last_epoch" "$final_map50" "$final_map5095" "$args" "$best"
done

train_state=$(ps -p "$train_pid" -o pid=,stat=,etime=,pcpu= 2>/dev/null || true)
queue_state=$(ps -p "$queue_pid" -o pid=,stat=,etime=,pcpu= 2>/dev/null || true)

if [ -n "$train_state" ]; then
  printf "PROC|train|%s\n" "$train_state"
else
  printf "PROC|train|STOPPED pid=%s\n" "$train_pid"
fi

if [ -n "$queue_state" ]; then
  printf "PROC|queue|%s\n" "$queue_state"
else
  printf "PROC|queue|STOPPED pid=%s\n" "$queue_pid"
fi
'@

$tmpLocal = [System.IO.Path]::GetTempFileName()
$remoteTmp = "/tmp/cea_check_server_status_$PID.sh"

try {
    $scriptForSsh = ($remoteScript -replace "`r", "") + "`n"
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($tmpLocal, $scriptForSsh, $utf8NoBom)

    & scp @scpArgs $tmpLocal "${sshTarget}:$remoteTmp" | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to copy temporary status script to server."
    }

    $runArgs = $RunNames -join " "
    $remoteRunCommand = "bash '$remoteTmp' '$RemoteRoot' '$MinEpochs' '$TrainPid' '$QueuePid' $runArgs; status=`$?; rm -f '$remoteTmp'; exit `$status"
    $rawLines = & ssh @sshArgs $remoteRunCommand
    if ($LASTEXITCODE -ne 0) {
        throw "SSH status check failed with exit code $LASTEXITCODE"
    }
}
finally {
    if (Test-Path -LiteralPath $tmpLocal) {
        Remove-Item -LiteralPath $tmpLocal -Force
    }
}

foreach ($line in $rawLines) {
    if ([string]::IsNullOrWhiteSpace($line)) {
        continue
    }

    $parts = $line -split "\|"
    switch ($parts[0]) {
        "REMOTE_ROOT" {
            Write-Host "Remote root: $($parts[1])"
        }
        "MIN_EPOCHS" {
            Write-Host "Completion gate: $($parts[1]) epochs"
            Write-Host ""
        }
        "RUN" {
            $runName = $parts[1]
            $status = $parts[2]
            $epochs = $parts[3]
            $lastEpoch = $parts[4]
            $map50 = $parts[5]
            $map5095 = $parts[6]
            $argsPath = $parts[7]
            $bestPath = $parts[8]

            if ($status -eq "READY") {
                Write-Host "[READY]   $runName epochs=$epochs last_epoch=$lastEpoch mAP50=$map50 mAP50-95=$map5095"
            }
            elseif ($status -eq "PARTIAL") {
                Write-Host "[PARTIAL] $runName epochs=$epochs last_epoch=$lastEpoch mAP50=$map50 mAP50-95=$map5095"
            }
            else {
                Write-Host "[MISSING] $runName"
            }
            Write-Host "          args=$argsPath"
            Write-Host "          best=$bestPath"
        }
        "PROC" {
            Write-Host "Process $($parts[1]): $($parts[2])"
        }
    }
}
