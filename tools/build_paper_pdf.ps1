param(
    [string]$TexFile = "paper\manuscript_submission_candidate.tex",
    [string]$OutDir = "paper",
    [switch]$KeepIntermediates
)

$ErrorActionPreference = "Stop"

function Invoke-Checked {
    param([string[]]$Command, [string]$WorkingDirectory = ".")

    Push-Location $WorkingDirectory
    $previousErrorActionPreference = $ErrorActionPreference
    try {
        $ErrorActionPreference = "Continue"
        & $Command[0] $Command[1..($Command.Length - 1)] 2>&1 | Tee-Object -Variable output
        if ($LASTEXITCODE -ne 0) {
            $joined = $Command -join " "
            throw "Command failed with exit code $LASTEXITCODE`: $joined"
        }
        return $output
    }
    finally {
        $ErrorActionPreference = $previousErrorActionPreference
        Pop-Location
    }
}

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$texPath = Resolve-Path (Join-Path $root $TexFile)
$outPath = Join-Path $root $OutDir
New-Item -ItemType Directory -Force -Path $outPath | Out-Null

$tectonic = Join-Path $root ".tools\tectonic\tectonic.exe"
$xelatex = Get-Command xelatex -ErrorAction SilentlyContinue

$logPath = Join-Path $outPath "tectonic_build.log"
if (Test-Path $tectonic) {
    $args = @(
        $tectonic,
        "--keep-logs",
        "--outdir", $outPath,
        $texPath
    )
    if ($KeepIntermediates) {
        $args = @($tectonic, "--keep-logs", "--keep-intermediates", "--outdir", $outPath, $texPath)
    }
    $output = Invoke-Checked $args
    $output | Set-Content -Path $logPath -Encoding UTF8
}
elseif ($xelatex) {
    $paperDir = Split-Path $texPath -Parent
    $texName = Split-Path $texPath -Leaf
    $output1 = Invoke-Checked @($xelatex.Source, "-interaction=nonstopmode", $texName) -WorkingDirectory $paperDir
    $output2 = Invoke-Checked @($xelatex.Source, "-interaction=nonstopmode", $texName) -WorkingDirectory $paperDir
    @($output1 + $output2) | Set-Content -Path (Join-Path $outPath "xelatex_build.log") -Encoding UTF8
}
else {
    throw "No LaTeX engine found. Install TeX Live/MiKTeX or keep .tools\tectonic\tectonic.exe available."
}

$pdfName = [System.IO.Path]::GetFileNameWithoutExtension($texPath) + ".pdf"
$pdfPath = Join-Path $outPath $pdfName
if (!(Test-Path $pdfPath)) {
    throw "Build finished but PDF was not found: $pdfPath"
}

Write-Host "Built PDF: $pdfPath"

if (!$KeepIntermediates) {
    $stem = [System.IO.Path]::GetFileNameWithoutExtension($texPath)
    foreach ($ext in @(".aux", ".out", ".toc", ".xdv")) {
        $candidate = Join-Path $outPath ($stem + $ext)
        if (Test-Path $candidate) {
            Remove-Item -LiteralPath $candidate -Force
        }
    }
}
