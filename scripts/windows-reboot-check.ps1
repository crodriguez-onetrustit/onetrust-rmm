# Windows Reboot Check Script
# Check if system needs reboot

$rebootRequired = $false

# Check pending file rename operations
$Pending = Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager" -Name "PendingFileRenameOperations" -ErrorAction SilentlyContinue
if ($Pending) { $rebootRequired = $true }

# Check Windows Update
$UpdateSession = New-Object -ComObject Microsoft.Update.Session
$UpdateSearcher = $UpdateSession.CreateUpdateSearcher()
$SearchResult = $UpdateSearcher.Search("IsInstalled=0 and Type='Software'")
if ($SearchResult.Updates.Count -gt 0) { $rebootRequired = $true }

Write-Output "Reboot Required: $rebootRequired"
