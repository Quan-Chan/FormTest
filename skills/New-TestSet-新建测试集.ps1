$base = "测试集"
$dir = $base
$n = 0
while (Test-Path (Join-Path $pwd $dir)) {
    $n++
    $dir = "$base$n"
}
$root = Join-Path $pwd $dir
$qDir = Join-Path $root "测试问题"
$pDir = Join-Path $root "测试系统提示词"
$rDir = Join-Path $root "测试结果"
New-Item -ItemType Directory -Path $qDir -Force | Out-Null
New-Item -ItemType Directory -Path $pDir -Force | Out-Null
New-Item -ItemType Directory -Path $rDir -Force | Out-Null
Set-Content -Path (Join-Path $qDir ".test-set-part") -Value "questions" -NoNewline -Encoding UTF8
Set-Content -Path (Join-Path $pDir ".test-set-part") -Value "prompts" -NoNewline -Encoding UTF8
Set-Content -Path (Join-Path $rDir ".test-set-part") -Value "results" -NoNewline -Encoding UTF8
Write-Host "已创建: $root"