# Verifica el servicio ICF de produccion sin imprimir el token.
#   .\check.ps1                 # contra Caddy local (127.0.0.1:11435)
#   .\check.ps1 -Public         # ademas, por la URL publica de Tailscale Funnel
#   .\check.ps1 -Suggest        # ademas, pide una sugerencia sintetica y mide la latencia
param([switch]$Public, [switch]$Suggest)

$envFile = Join-Path $env:USERPROFILE ".hab-icf\.env"
$token = (Get-Content $envFile | Where-Object { $_ -like "ICF_TOKEN=*" }) -replace "^ICF_TOKEN=", ""
$ts = "C:\Program Files\Tailscale\tailscale.exe"
$publicUrl = $null
if ($Public) {
    $dns = (& $ts status --json | ConvertFrom-Json).Self.DNSName.TrimEnd(".")
    $publicUrl = "https://$dns"
}

function Call($base, $path, $auth, $method = "GET", $body = $null) {
    $args = @("-s", "-o", "NUL", "-w", "%{http_code}", "-X", $method, "$base$path")
    if ($auth) { $args += @("-H", "Authorization: Bearer $auth") }
    if ($body) { $args += @("-H", "Content-Type: application/json", "-d", $body) }
    & curl.exe @args
}

function Check($label, $actual, $expected) {
    $ok = "$actual" -eq "$expected"
    Write-Host ("{0,-52} {1}  {2}" -f $label, $actual, $(if ($ok) { "OK" } else { "FALLA (esperado $expected)" }))
    return $ok
}

$bases = @(@{ name = "local"; url = "http://127.0.0.1:11435" })
if ($publicUrl) { $bases += @{ name = "publica"; url = $publicUrl } }

$allOk = $true
foreach ($b in $bases) {
    Write-Host "== $($b.name): $($b.url -replace 'https://[^.]+\.', 'https://<nodo>.')"
    $allOk = (Check "/health sin token" (Call $b.url "/health" $null) 401) -and $allOk
    $allOk = (Check "/health con token falso" (Call $b.url "/health" "token-falso") 401) -and $allOk
    $allOk = (Check "/health con token correcto" (Call $b.url "/health" $token) 200) -and $allOk
    $allOk = (Check "/api/tags con token correcto (Ollama)" (Call $b.url "/api/tags" $token) 200) -and $allOk
    $allOk = (Check "/api/generate con token correcto (bloqueado)" (Call $b.url "/api/generate" $token "POST" "{}") 404) -and $allOk
}

if ($Suggest) {
    Write-Host "== sugerencia sintetica (caso de prueba, no es una persona real)"
    $payload = '{"age":34,"gender":"Femenino","cause":"Alteración genética o hereditaria","cat_fisica":"Severa","cat_psicosocial":"Leve","levels":{"D1":10,"D2":20,"D3":15,"D4":80,"D5":65,"D6":70},"diag_cie":"G80 Paralisis cerebral","clinical_notes":"Espastica"}'
    $tmp = New-TemporaryFile
    Set-Content -Path $tmp -Value $payload -Encoding utf8
    $sw = [Diagnostics.Stopwatch]::StartNew()
    $json = & curl.exe -s -X POST "http://127.0.0.1:11435/suggest" -H "Authorization: Bearer $token" -H "Content-Type: application/json" --data-binary "@$tmp"
    $sw.Stop()
    Remove-Item $tmp -Force
    $r = $json | ConvertFrom-Json
    Write-Host ("modelo={0} llm_used={1} total={2:N1}s (servicio: {3} ms)" -f $r.model, $r.llm_used, $sw.Elapsed.TotalSeconds, $r.latency_ms)
    Write-Host ("b: " + (($r.functions | ForEach-Object { $_.code }) -join " ") + " | s: " + (($r.structures | ForEach-Object { $_.code }) -join " ") + " | d: " + (($r.activities | ForEach-Object { $_.code }) -join " "))
    if ($r.llm_error) { Write-Host "llm_error: $($r.llm_error)"; $allOk = $false }
}

if ($allOk) { Write-Host "`nTodo correcto." } else { Write-Host "`nHay comprobaciones que fallan."; exit 1 }
