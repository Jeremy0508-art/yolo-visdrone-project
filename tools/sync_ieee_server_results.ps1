param(
    [string]$HostName = "connect.bjb2.seetacloud.com",
    [int]$Port = 44733,
    [string]$User = "root",
    [string]$IdentityFile = "$env:USERPROFILE\.ssh\autodl_yolo_visdrone",
    [string]$RemoteRoot = "/root/autodl-tmp/yolo-visdrone-project",
    [int]$MinEpochs = 100,
    [string[]]$RunNames = @(
        "yolo11n_p2_tofc_960_visdrone",
        "baseline_yolo11n_960_uavdt",
        "yolo11n_p2_960_uavdt",
        "baseline_yolov8n_960_uavdt",
        "baseline_yolo11s_960_uavdt"
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
        Write-Host "Sync file: $remoteFile"
        Invoke-Checked ($scpBase + @("${sshTarget}:$remoteFile", $LocalDirectory))
    }
}

function Sync-RemoteFileIfExists {
    param([string]$RemotePath, [string]$LocalDirectory)

    $checkCommand = "test -f '$RemotePath' && echo READY || echo MISSING"
    $status = & $sshBase[0] $sshBase[1..($sshBase.Length - 1)] $checkCommand
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to check remote file: $RemotePath"
    }
    if (($status | Select-Object -Last 1) -eq "READY") {
        New-Item -ItemType Directory -Force -Path $LocalDirectory | Out-Null
        Write-Host "Sync file: $RemotePath"
        Invoke-Checked ($scpBase + @("${sshTarget}:$RemotePath", $LocalDirectory))
    }
    else {
        Write-Host "Skip missing remote file: $RemotePath"
    }
}

$sshTarget = "$User@$HostName"
$sshBase = @(
    "ssh",
    "-i", $IdentityFile,
    "-p", "$Port",
    "-o", "StrictHostKeyChecking=no",
    "-o", "ConnectTimeout=10",
    "-o", "BatchMode=yes",
    $sshTarget
)
$scpBase = @(
    "scp",
    "-i", $IdentityFile,
    "-P", "$Port",
    "-o", "StrictHostKeyChecking=no",
    "-o", "ConnectTimeout=10",
    "-o", "BatchMode=yes"
)

New-Item -ItemType Directory -Force -Path "runs\detect" | Out-Null
New-Item -ItemType Directory -Force -Path "runs\logs" | Out-Null
New-Item -ItemType Directory -Force -Path "paper\tables" | Out-Null
New-Item -ItemType Directory -Force -Path "paper\figures\scale_analysis" | Out-Null

foreach ($runName in $RunNames) {
    $remoteRun = "$RemoteRoot/runs/detect/$runName"
    $checkCommand = @"
if [ -f '$remoteRun/results.csv' ]; then
  lines=`$(wc -l < '$remoteRun/results.csv')
  epochs=`$((lines - 1))
  if [ "`$epochs" -ge "$MinEpochs" ]; then
    if [ -f '$remoteRun/args.yaml' ] && [ -f '$remoteRun/weights/best.pt' ]; then
      echo READY
    else
      echo PARTIAL_ARTIFACTS:`$epochs
    fi
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

Write-Host "Sync IEEE server logs."
Sync-RemoteGlob "$RemoteRoot/runs/logs/train_yolo11n_p2_tofc_960_visdrone*.log" "runs\logs\"
Sync-RemoteGlob "$RemoteRoot/runs/logs/train_*_uavdt*.log" "runs\logs\"
Sync-RemoteGlob "$RemoteRoot/runs/logs/*ieee*queue*.log" "runs\logs\"
Sync-RemoteGlob "$RemoteRoot/runs/logs/*evaluate_scale*.log" "runs\logs\"

Write-Host "Sync full scale-wise outputs if present."
Sync-RemoteFileIfExists "$RemoteRoot/paper/tables/ieee_scale_results_visdrone.csv" "paper\tables\"
Sync-RemoteFileIfExists "$RemoteRoot/paper/figures/scale_analysis/ieee_scale_recall_visdrone.png" "paper\figures\scale_analysis\"

Write-Host "Refresh IEEE status and audits."
Invoke-Checked @("python", "tools\check_ieee_claims.py")
Invoke-Checked @("python", "tools\check_ieee_phase1_artifacts.py")
Invoke-Checked @("python", "tools\build_ieee_server_progress_report.py")

Write-Host "Done."
