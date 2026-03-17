# Clear Temp Files Script

$TempPaths = @(
    "$env:TEMP\*",
    "$env:LOCALAPPDATA\Temp\*",
    "C:\Windows\Temp\*"
)

$TotalFreed = 0

foreach ($path in $TempPaths) {
    try {
        $files = Get-ChildItem -Path $path -Recurse -ErrorAction SilentlyContinue
        $size = ($files | Measure-Object -Property Length -Sum).Sum
        Remove-Item -Path $path -Recurse -Force -ErrorAction SilentlyContinue
        $TotalFreed += $size
    } catch { }
}

Write-Output "Freed $([math]::Round($TotalFreed/1MB, 2)) MB"
