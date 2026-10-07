# Crea el .env de produccion con un token y una clave de base de datos aleatorios.
# No imprime los secretos: quedan solo en el archivo .env (ignorado por git).
# Si el .env ya existe no lo toca (usa -Rotar para generar uno nuevo).
param([switch]$Rotar)

$ErrorActionPreference = "Stop"
# Fuera del repositorio y de OneDrive: el repositorio se sincroniza a la nube y los secretos no deben ir alli.
$envDir = Join-Path $env:USERPROFILE ".hab-icf"
$envFile = Join-Path $envDir ".env"
New-Item -ItemType Directory -Force -Path $envDir | Out-Null

function New-Secret([int]$length) {
    $chars = [char[]]"ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789"
    $bytes = New-Object byte[] $length
    [System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
    -join ($bytes | ForEach-Object { $chars[$_ % $chars.Length] })
}

if ((Test-Path $envFile) -and -not $Rotar) {
    Write-Host ".env ya existe; no se modifica. Usa -Rotar para generar secretos nuevos."
    exit 0
}

$lines = @(
    "ICF_TOKEN=$(New-Secret 48)",
    "ICF_DB_PASSWORD=$(New-Secret 32)",
    "ICF_LLM_MODEL=gemma4:e4b",
    "ICF_MODE=calidad"
)
Set-Content -Path $envFile -Value $lines -Encoding ascii
Write-Host ".env creado en $envFile (token de 48 caracteres y clave de base de datos de 32; no se muestran)."
