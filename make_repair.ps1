$ErrorActionPreference = "Stop"
$base = "C:\Users\Hare Ram\Desktop\cywallearn-unhacked"
$files = @('cywallearn.py','modules/generator.py','modules/analyzer.py','modules/__init__.py')

$lines = @()
$lines += '#!/data/data/com.termux/files/usr/bin/bash'
$lines += '# Cywallearn Unhacked - Repair Script'
$lines += '# Run this in ~/cywallearn-unhacked to fix corrupted files'
$lines += '#'
$lines += '# Usage: cd ~/cywallearn-unhacked && bash repair.sh'
$lines += ''
$lines += 'echo "[+] Regenerating Cywallearn Unhacked files..."'
$lines += ''

foreach ($f in $files) {
    $contentBytes = [IO.File]::ReadAllBytes((Join-Path $base $f))
    $b64 = [Convert]::ToBase64String($contentBytes)
    $lines += "echo '--- Writing $f ---'"
    $lines += "base64 -d > '$f' << 'CYWEOF'"
    $lines += $b64
    $lines += 'CYWEOF'
    $lines += ''
}

$lines += 'chmod +x cywallearn.py'
$lines += ''
$lines += 'echo "[+] Repair complete. Run: python3 cywallearn.py"'
$lines += 'echo "[+] Stay Unhackable. Stay Cywallearn."'

[IO.File]::WriteAllLines("$base\repair.sh", $lines, [System.Text.UTF8Encoding]::new($false))
Write-Host "repair.sh created successfully!"
