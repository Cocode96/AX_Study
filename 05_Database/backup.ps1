param(
    [string]$PgDump = 'C:\Program Files\PostgreSQL\18\bin\pg_dump.exe',
    [string]$DbHost = 'localhost',
    [int]$Port = 5432,
    [string]$DbUser = 'postgres',
    [string]$Database = 'postgres'
)
$ErrorActionPreference = 'Stop'
$backupDir = Join-Path $PSScriptRoot 'backup'
New-Item -ItemType Directory -Force $backupDir | Out-Null
$pending = Join-Path $backupDir 'postgres.pending.sql'
$destination = Join-Path $backupDir 'postgres.sql'
try {
    & $PgDump -h $DbHost -p $Port -U $DbUser -d $Database -W --no-owner --no-privileges -f $pending
    if ($LASTEXITCODE -ne 0) { throw 'pg_dump failed. Existing backup was preserved.' }
    Move-Item -LiteralPath $pending -Destination $destination -Force
    Write-Host "Backup saved: $destination"
} finally {
    if (Test-Path -LiteralPath $pending) { Remove-Item -LiteralPath $pending }
}
