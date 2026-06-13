param(
    [string]$HostName = "connect.bjb2.seetacloud.com",
    [int]$Port = 44733,
    [string]$User = "root",
    [string]$IdentityFile = "$env:USERPROFILE\.ssh\autodl_yolo_visdrone",
    [string]$RemoteRoot = "/root/autodl-tmp/yolo-visdrone-project",
    [int]$MinEpochs = 100,
    [int]$TrainPid = 43554,
    [int]$QueuePid = 43842,
    [string]$OutputPath = "paper\cea_server_status_snapshot.md",
    [string]$HistoryPath = "paper\tables\cea_server_status_history.csv",
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

$displayLines = New-Object System.Collections.Generic.List[string]
$runRows = New-Object System.Collections.Generic.List[object]
$procRows = New-Object System.Collections.Generic.List[object]
$remoteRootValue = ""
$minEpochsValue = "$MinEpochs"

foreach ($line in $rawLines) {
    if ([string]::IsNullOrWhiteSpace($line)) {
        continue
    }

    $parts = $line -split "\|"
    switch ($parts[0]) {
        "REMOTE_ROOT" {
            $remoteRootValue = $parts[1]
            $displayLines.Add("Remote root: $($parts[1])")
        }
        "MIN_EPOCHS" {
            $minEpochsValue = $parts[1]
            $displayLines.Add("Completion gate: $($parts[1]) epochs")
            $displayLines.Add("")
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
                $displayLines.Add("[READY]   $runName epochs=$epochs last_epoch=$lastEpoch mAP50=$map50 mAP50-95=$map5095")
            }
            elseif ($status -eq "PARTIAL") {
                $displayLines.Add("[PARTIAL] $runName epochs=$epochs last_epoch=$lastEpoch mAP50=$map50 mAP50-95=$map5095")
            }
            else {
                $displayLines.Add("[MISSING] $runName")
            }
            $displayLines.Add("          args=$argsPath")
            $displayLines.Add("          best=$bestPath")
            $runRows.Add([pscustomobject]@{
                Run = $runName
                Status = $status
                Epochs = $epochs
                LastEpoch = $lastEpoch
                LastMap50 = $map50
                LastMap5095 = $map5095
                Args = $argsPath
                Best = $bestPath
            })
        }
        "PROC" {
            $displayLines.Add("Process $($parts[1]): $($parts[2])")
            $procRows.Add([pscustomobject]@{
                Name = $parts[1]
                State = $parts[2]
            })
        }
    }
}

foreach ($displayLine in $displayLines) {
    Write-Host $displayLine
}

if (![string]::IsNullOrWhiteSpace($OutputPath)) {
    $outputFullPath = Join-Path (Resolve-Path (Join-Path $PSScriptRoot "..")) $OutputPath
    $outputDir = Split-Path $outputFullPath -Parent
    New-Item -ItemType Directory -Force -Path $outputDir | Out-Null

    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
    $report = New-Object System.Collections.Generic.List[string]
    $report.Add("# CEA Server Status Snapshot")
    $report.Add("")
    $report.Add("Generated by ``tools/check_cea_server_status.ps1`` at " + $timestamp + ".")
    $report.Add("")
    $report.Add("- Remote root: ``" + $remoteRootValue + "``")
    $report.Add("- Completion gate: ``" + $minEpochsValue + "`` epochs")
    $report.Add("- Evidence rule: partial or missing runs are progress information only and must not be copied into paper tables.")
    $report.Add("")
    $report.Add("## Runs")
    $report.Add("")
    $report.Add("| Run | Status | Epochs | Last Epoch | Last mAP50 | Last mAP50-95 | Args | Best |")
    $report.Add("| --- | --- | ---: | ---: | ---: | ---: | --- | --- |")
    foreach ($row in $runRows) {
        $report.Add(
            "| " + $row.Run +
            " | " + $row.Status +
            " | " + $row.Epochs +
            " | " + $row.LastEpoch +
            " | " + $row.LastMap50 +
            " | " + $row.LastMap5095 +
            " | ``" + $row.Args + "``" +
            " | ``" + $row.Best + "`` |"
        )
    }
    $report.Add("")
    $report.Add("## Processes")
    $report.Add("")
    $report.Add("| Process | State |")
    $report.Add("| --- | --- |")
    foreach ($row in $procRows) {
        $report.Add("| " + $row.Name + " | ``" + $row.State + "`` |")
    }
    $report.Add("")

    $report | Set-Content -Path $outputFullPath -Encoding UTF8
    Write-Host ""
    Write-Host "Wrote status snapshot: $outputFullPath"
}

if (![string]::IsNullOrWhiteSpace($HistoryPath)) {
    $historyFullPath = Join-Path (Resolve-Path (Join-Path $PSScriptRoot "..")) $HistoryPath
    $historyDir = Split-Path $historyFullPath -Parent
    New-Item -ItemType Directory -Force -Path $historyDir | Out-Null

    $trainState = ($procRows | Where-Object { $_.Name -eq "train" } | Select-Object -First 1).State
    $queueState = ($procRows | Where-Object { $_.Name -eq "queue" } | Select-Object -First 1).State
    $historyRows = foreach ($row in $runRows) {
        [pscustomobject]@{
            timestamp = $timestamp
            remote_root = $remoteRootValue
            completion_gate_epochs = $minEpochsValue
            run = $row.Run
            status = $row.Status
            epochs = $row.Epochs
            last_epoch = $row.LastEpoch
            last_map50 = $row.LastMap50
            last_map50_95 = $row.LastMap5095
            args = $row.Args
            best = $row.Best
            train_process = $trainState
            queue_process = $queueState
        }
    }
    if (Test-Path -LiteralPath $historyFullPath) {
        $historyRows | Export-Csv -Path $historyFullPath -NoTypeInformation -Encoding UTF8 -Append
    }
    else {
        $historyRows | Export-Csv -Path $historyFullPath -NoTypeInformation -Encoding UTF8
    }
    Write-Host "Appended status history: $historyFullPath"
}
