# Путь к приложению
$AppPath = "C:\Project\Project_Rust\VirtualComR\target\release\VirtualComR.exe"

# Проверяем существование файла
if (-not (Test-Path $AppPath)) {
    Write-Host "❌ Файл не найден: $AppPath" -ForegroundColor Red
    exit 1
}

Write-Host "🔍 Анализ зависимостей для $AppPath..." -ForegroundColor Green

# Получаем список DLL через where.exe
$Dlls = @()
$Process = Start-Process -FilePath $AppPath -PassThru -WindowStyle Hidden
Start-Sleep -Seconds 2

# Получаем список загруженных DLL
$Modules = Get-Process -Id $Process.Id | Select-Object -ExpandProperty Modules
$Dlls = $Modules | Select-Object -ExpandProperty FileName | Where-Object { $_ -match '\.dll$' } | ForEach-Object { Split-Path $_ -Leaf }

# Останавливаем процесс
Stop-Process -Id $Process.Id -Force

# Фильтруем системные DLL
$SystemDlls = @(
    "kernel32.dll",
    "user32.dll",
    "gdi32.dll",
    "win32u.dll",
    "advapi32.dll",
    "sechost.dll",
    "rpcrt4.dll",
    "ntdll.dll",
    "combase.dll",
    "ucrtbase.dll",
    "bcrypt.dll",
    "cryptbase.dll",
    "kernelbase.dll",
    "windows.storage.dll",
    "wldp.dll",
    "shlwapi.dll",
    "shcore.dll",
    "ole32.dll",
    "oleaut32.dll",
    "msvcrt.dll"
)

$NonSystemDlls = $Dlls | Where-Object { $_ -notin $SystemDlls }

# Создаем директорию на рабочем столе, если она не существует
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$outputPath = Join-Path $DesktopPath "dll2rust_simple.txt"

# Сохраняем результаты в файл
$NonSystemDlls | Out-File $outputPath -Encoding utf8

Write-Host "`n📋 Найденные DLL (исключая системные):" -ForegroundColor Cyan
$NonSystemDlls | ForEach-Object { Write-Host $_ }

Write-Host "`n💾 Список сохранен в файл: $outputPath" -ForegroundColor Green

# Открываем файл в блокноте
notepad.exe $outputPath 