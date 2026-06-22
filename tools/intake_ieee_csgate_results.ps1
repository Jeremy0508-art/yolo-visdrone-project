param(
    [string]$HostName = "connect.bjb3.seetacloud.com",
    [int]$Port = 24476,
    [string]$User = "root",
    [string]$IdentityFile = "$env:USERPROFILE\.ssh\autodl_yolo_visdrone",
    [string]$RemoteRoot = "/root/autodl-tmp/yolo-visdrone-project",
    [int]$MinEpochs = 100,
    [string]$Device = "0",
    [switch]$CheckOnly,
    [switch]$RequireReady,
    [switch]$RunDiagnostics,
    [switch]$CompileDraft
)

$ErrorActionPreference = "Stop"

$VisRun = "yolo11n_p2_csgate_960_visdrone"
$UavdtRun = "yolo11n_p2_csgate_960_uavdt"

function Invoke-Checked {
    param([string[]]$Command)

    Write-Host ""
    Write-Host ">> $($Command -join ' ')"
    & $Command[0] $Command[1..($Command.Length - 1)]
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code $LASTEXITCODE`: $($Command -join ' ')"
    }
}

function Get-LatestRunStatus {
    param([string]$RunName)

    $history = "paper\tables\ieee_server_status_history.csv"
    if (!(Test-Path -LiteralPath $history)) {
        return $null
    }
    $rows = Import-Csv -LiteralPath $history | Where-Object { $_.run -eq $RunName }
    if (!$rows) {
        return $null
    }
    return $rows | Select-Object -Last 1
}

function Refresh-StatusAndAudits {
    Invoke-Checked @(
        "powershell", "-ExecutionPolicy", "Bypass", "-File", ".\tools\check_ieee_server_status.ps1",
        "-HostName", $HostName,
        "-Port", "$Port",
        "-User", $User,
        "-IdentityFile", $IdentityFile,
        "-RemoteRoot", $RemoteRoot,
        "-MinEpochs", "$MinEpochs"
    )
    Invoke-Checked @("python", "tools\build_ieee_server_progress_report.py")
    Invoke-Checked @("python", "tools\check_ieee_goal_readiness.py")
    Invoke-Checked @("python", "tools\build_ieee_submission_dashboard.py")
}

function Get-IntakeStatus {
    $vis = Get-LatestRunStatus -RunName $VisRun
    $uav = Get-LatestRunStatus -RunName $UavdtRun

    Write-Host ""
    foreach ($entry in @(@($VisRun, $vis), @($UavdtRun, $uav))) {
        $name = $entry[0]
        $row = $entry[1]
        if ($null -eq $row) {
            Write-Host "${name}: no server-history row"
            continue
        }
        Write-Host ("{0}: status={1}; epochs={2}/{3}; mAP50={4}; mAP50-95={5}; timestamp={6}" -f `
            $name, $row.status, $row.epochs, $row.completion_gate_epochs, $row.last_map50, $row.last_map50_95, $row.timestamp)
    }

    if ($null -eq $vis -or $null -eq $uav) {
        return "WAITING_FOR_REMOTE_COMPLETION"
    }
    if ($vis.status -eq "READY" -and $uav.status -eq "READY" -and [int]$vis.epochs -ge $MinEpochs -and [int]$uav.epochs -ge $MinEpochs) {
        return "REMOTE_COMPLETE_READY_TO_SYNC"
    }
    return "WAITING_FOR_REMOTE_COMPLETION"
}

function Run-GuardedSync {
    Invoke-Checked @(
        "powershell", "-ExecutionPolicy", "Bypass", "-File", ".\tools\sync_ieee_server_results.ps1",
        "-HostName", $HostName,
        "-Port", "$Port",
        "-User", $User,
        "-IdentityFile", $IdentityFile,
        "-RemoteRoot", $RemoteRoot,
        "-MinEpochs", "$MinEpochs"
    )
    Invoke-Checked @("python", "tools\run_ieee_audits.py")
}

function Run-Diagnostics {
    Invoke-Checked @(
        "python", "tools\set_ieee_scale_target.py",
        "--model", "YOLO11n-P2-CSGate-960",
        "--run-dir", "runs\detect\yolo11n_p2_csgate_960_visdrone",
        "--note", "enabled after completed CSGate VisDrone weights were synced",
        "--apply"
    )
    Invoke-Checked @(
        "python", "tools\evaluate_scale_groups.py",
        "--targets-csv", "paper\tables\ieee_scale_eval_targets.csv",
        "--output", "paper\tables\ieee_scale_results_visdrone.csv",
        "--plot-output", "paper\figures\scale_analysis\ieee_scale_recall_visdrone.png",
        "--device", $Device
    )
    Invoke-Checked @(
        "python", "tools\evaluate_scale_ap.py",
        "--targets-csv", "paper\tables\ieee_scale_eval_targets.csv",
        "--output", "paper\tables\ieee_scale_ap_results_visdrone.csv",
        "--plot-output", "paper\figures\scale_analysis\ieee_scale_ap50_visdrone.png",
        "--device", $Device
    )
    Invoke-Checked @("python", "tools\benchmark_speed.py", "--warmup", "10", "--samples", "100", "--output", "paper\tables\speed_results.csv", "--device", $Device)
    Invoke-Checked @("python", "tools\export_paper_tables.py")
    Invoke-Checked @("python", "tools\export_ieee_uavdt_results.py")
    Invoke-Checked @("python", "tools\export_ieee_tables.py")
    Invoke-Checked @("python", "tools\run_ieee_audits.py")
}

function Compile-Draft {
    Invoke-Checked @(
        "powershell", "-ExecutionPolicy", "Bypass", "-File", ".\tools\build_paper_pdf.ps1",
        "-TexFile", "paper\ieee_trans\main_draft.tex",
        "-OutDir", "paper\ieee_trans"
    )
    Invoke-Checked @("python", "tools\run_ieee_audits.py")
}

Refresh-StatusAndAudits
$status = Get-IntakeStatus
Write-Host ""
Write-Host "CSGate intake status: $status"

if ($CheckOnly) {
    Write-Host "CheckOnly requested; no sync, diagnostics, or manuscript build was run."
    exit 0
}

if ($status -eq "WAITING_FOR_REMOTE_COMPLETION") {
    Write-Host "CSGate is not remotely complete. No files were synced."
    if ($RequireReady) {
        exit 2
    }
    exit 0
}

if ($status -eq "REMOTE_COMPLETE_READY_TO_SYNC") {
    Run-GuardedSync
    if ($RunDiagnostics) {
        Run-Diagnostics
    }
    else {
        Write-Host "CSGate complete runs were synced if local artifacts passed the guarded sync. Re-run with -RunDiagnostics after confirming local artifacts if diagnostics are needed."
    }
    if ($CompileDraft) {
        Compile-Draft
    }
    exit 0
}

Write-Host "Unhandled intake status: $status"
exit 1
