param(
    [string]$HostName = "connect.bjb2.seetacloud.com",
    [int]$Port = 44733,
    [string]$User = "root",
    [string]$IdentityFile = "$env:USERPROFILE\.ssh\autodl_yolo_visdrone",
    [string]$RemoteRoot = "/root/autodl-tmp/yolo-visdrone-project",
    [int]$MinEpochs = 100,
    [string[]]$RunNames = @(
        "baseline_yolo11n_960_visdrone",
        "yolo11n_p2_960_visdrone",
        "baseline_yolov8n_960_visdrone",
        "baseline_yolo11s_960_visdrone",
        "baseline_yolov5n_visdrone"
    )
)

$ErrorActionPreference = "Stop"

function Invoke-Checked {
    param([string[]]$Command)
    & $Command[0] $Command[1..($Command.Length - 1)]
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code $LASTEXITCODE`: $($Command -join ' ')"
    }
}

function Sync-RemoteGlob {
    param([string]$RemotePattern, [string]$LocalDirectory)

    $listCommand = "ls -1 $RemotePattern 2>/dev/null || true"
    $remoteFiles = & $sshBase[0] $sshBase[1..($sshBase.Length - 1)] $listCommand
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to list remote files: $RemotePattern"
    }
    foreach ($remoteFile in $remoteFiles) {
        if ([string]::IsNullOrWhiteSpace($remoteFile)) {
            continue
        }
        Write-Host "Sync log: $remoteFile"
        Invoke-Checked ($scpBase + @("${sshTarget}:$remoteFile", $LocalDirectory))
    }
}

$sshTarget = "$User@$HostName"
$sshBase = @(
    "ssh",
    "-i", $IdentityFile,
    "-p", "$Port",
    "-o", "StrictHostKeyChecking=no",
    $sshTarget
)
$scpBase = @(
    "scp",
    "-i", $IdentityFile,
    "-P", "$Port",
    "-o", "StrictHostKeyChecking=no"
)

New-Item -ItemType Directory -Force -Path "runs\detect" | Out-Null
New-Item -ItemType Directory -Force -Path "runs\logs" | Out-Null

foreach ($runName in $RunNames) {
    $remoteRun = "$RemoteRoot/runs/detect/$runName"
    $checkCommand = @"
if [ -f '$remoteRun/results.csv' ]; then
  lines=`$(wc -l < '$remoteRun/results.csv')
  epochs=`$((lines - 1))
  if [ "`$epochs" -ge "$MinEpochs" ]; then
    echo READY
  else
    echo PARTIAL:`$epochs
  fi
else
  echo MISSING
fi
"@
    $status = & $sshBase[0] $sshBase[1..($sshBase.Length - 1)] $checkCommand
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to check remote run: $runName"
    }

    if (($status | Select-Object -Last 1) -ne "READY") {
        Write-Host "Skip ${runName}: $($status | Select-Object -Last 1)."
        continue
    }

    Write-Host "Sync run: $runName"
    Invoke-Checked ($scpBase + @("-r", "${sshTarget}:$remoteRun", "runs\detect\"))
}

Write-Host "Sync matching server logs."
Sync-RemoteGlob "$RemoteRoot/runs/logs/train_*_960*.log" "runs\logs\"
Sync-RemoteGlob "$RemoteRoot/runs/logs/train_baseline_yolov5n*.log" "runs\logs\"
Sync-RemoteGlob "$RemoteRoot/runs/logs/cea_server_queue_.log" "runs\logs\"

Write-Host "Regenerate paper tables from local artifacts."
Invoke-Checked @("python", "tools\export_paper_tables.py")

Write-Host "Done."
