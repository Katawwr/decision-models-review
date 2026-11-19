# Runs every planned call set in order. Keys come from the user's environment variables and are never printed.
#   .\src\run_all.ps1            # A1 A2 A3 A4 B1 B2 C1
#   .\src\run_all.ps1 B2 C1      # a subset
$ErrorActionPreference = 'Continue'
Set-Location (Join-Path $PSScriptRoot '..')
$env:OPENROUTER_API_KEY = [Environment]::GetEnvironmentVariable('OPENROUTER_API_KEY', 'User')
$env:GEMINI_API_KEY = [Environment]::GetEnvironmentVariable('GEMINI_API_KEY', 'User')
$runs = if ($args.Count -gt 0) { $args } else { @('A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'C1') }
# Ask Windows not to idle-sleep while this script runs. Released when the script ends.
Add-Type -Namespace Win32 -Name Power -MemberDefinition '[DllImport("kernel32.dll")] public static extern uint SetThreadExecutionState(uint esFlags);'
[void][Win32.Power]::SetThreadExecutionState([uint32]2147483651)
foreach ($run in $runs) {
    "=== $run start $(Get-Date -Format o) ==="
    python -I -u src\run_main.py $run --max-cost 10
    "=== $run exit $LASTEXITCODE $(Get-Date -Format o) ==="
}
[void][Win32.Power]::SetThreadExecutionState([uint32]2147483648)
"=== all done $(Get-Date -Format o) ==="
