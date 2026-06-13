$base = "C:\Users\Hare Ram\Desktop\cywallearn-unhacked"
$items = @(
    @{path="cywallearn.py"},
    @{path="modules/generator.py"},
    @{path="modules/analyzer.py"},
    @{path="modules/__init__.py"}
)

$lines = @()
$lines += "#!/data/data/com.termux/files/usr/bin/bash"
$lines += "# Cywallearn Unhacked - Regenerate clean files"
$lines += "# Save this script and run: bash repair.sh"
$lines += ""
$lines += 'DIR="$(cd "$(dirname "$0")" && pwd)"'
$lines += "cd $DIR"
$lines += "mkdir -p modules 2>/dev/null"
$lines += ""

foreach ($item in $items) {
    $fullPath = Join-Path $base $item.path
    $b64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes($fullPath))
    $lines += "cat > '$($item.path)' << 'CYWEOF'"
    $lines += $b64
    $lines += "CYWEOF"
    $lines += ""
}

$lines += "chmod +x cywallearn.py"
$lines += ""
$lines += "# Decode files from base64"
$lines += "for f in cywallearn.py modules/generator.py modules/analyzer.py modules/__init__.py; do"
$lines += '  if [ -f "$f" ]; then'
$lines += '    mv "$f" "$f.b64"'
$lines += '    base64 -d "$f.b64" > "$f" 2>/dev/null || python3 -c "import base64,sys; sys.stdout.write(base64.b64decode(open(chr(34)+sys.argv[1]+chr(34)).read()).decode())" "$f.b64" > "$f" 2>/dev/null || openssl base64 -d -in "$f.b64" -out "$f" 2>/dev/null'
$lines += '    rm -f "$f.b64"'
$lines += '    echo "  OK: $f"'
$lines += '  fi'
$lines += "done"
$lines += ""
$lines += "chmod +x cywallearn.py"
$lines += 'echo "[+] Done! Run: python3 cywallearn.py"'

$outPath = Join-Path $base "repair.sh"
[IO.File]::WriteAllLines($outPath, $lines)
Write-Host "Repair script generated: $outPath ($($lines.Count) lines)"
