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

function Invoke-Checked {
    param([string[]]$Command)

    Write-Host ""
    Write-Host ">> $($Command -join ' ')"
    & $Command[0] $Command[1..($Command.Length - 1)]
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code $LASTEXITCODE`: $($Command -join ' ')"
    }
}

function Get-SummaryValue {
    param(
        [string]$Path,
        [string]$Key
    )

    if (!(Test-Path -LiteralPath $Path)) {
        return ""
    }
    foreach ($line in Get-Content -LiteralPath $Path) {
        if ($line -match ("^- " + [regex]::Escape($Key) + ": (.+)$")) {
            return $Matches[1].Trim()
        }
    }
    return ""
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
    Invoke-Checked @("python", "tools\run_ieee_audits.py")
}

function Print-RunbookState {
    $runbook = "paper\ieee_scalegate_post_result_runbook.md"
    $status = Get-SummaryValue -Path $runbook -Key "Intake status"
    $remoteComplete = Get-SummaryValue -Path $runbook -Key "Remote complete ScaleGate runs"
    $localGate = Get-SummaryValue -Path $runbook -Key "Local result gate"
    $methodDecision = Get-SummaryValue -Path $runbook -Key "Method decision"
    $nextAction = Get-SummaryValue -Path $runbook -Key "Next action"

    Write-Host ""
    Write-Host "ScaleGate intake status: $status"
    Write-Host "Remote complete runs: $remoteComplete"
    Write-Host "Local result gate: $localGate"
    Write-Host "Method decision: $methodDecision"
    Write-Host "Next action: $nextAction"

    return $status
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
    Invoke-Checked @("python", "tools\set_ieee_scalegate_scale_target.py", "--apply")
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
$status = Print-RunbookState

if ($CheckOnly) {
    Write-Host "CheckOnly requested; no sync, diagnostics, or manuscript build was run."
    exit 0
}

if ($status -eq "WAITING_FOR_REMOTE_COMPLETION") {
    Write-Host "ScaleGate is not remotely complete. No files were synced."
    if ($RequireReady) {
        exit 2
    }
    exit 0
}

if ($status -eq "REMOTE_COMPLETE_READY_TO_SYNC") {
    Run-GuardedSync
    $status = Print-RunbookState
}

if ($status -eq "LOCAL_RESULTS_READY_FOR_DIAGNOSTICS") {
    if ($RunDiagnostics) {
        Run-Diagnostics
        $status = Print-RunbookState
    }
    else {
        Write-Host "Local result gate is open. Re-run with -RunDiagnostics to refresh scale, AP, speed, tables, and method-decision audits."
        exit 0
    }
}

if ($status -eq "READY_FOR_MANUSCRIPT_DECISION") {
    Write-Host "ScaleGate evidence is ready for method-selection review. Apply paper/ieee_method_selection_protocol.md before editing manuscript claims."
    if ($CompileDraft) {
        Compile-Draft
    }
    exit 0
}

Write-Host "Unhandled intake status: $status"
exit 1
