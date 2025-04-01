# Определяем пути
$SourceExe = "C:\Project\Project_Rust\VirtualComR\target\release\VirtualComR.exe"
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$DestDir = "$DesktopPath\VirtualComR_USB"

# Создаем директорию на рабочем столе
Write-Host "📁 Создание директории $DestDir..." -ForegroundColor Green
New-Item -ItemType Directory -Path $DestDir -Force

# Копируем exe файл
Write-Host "📦 Копирование VirtualComR.exe..." -ForegroundColor Green
Copy-Item $SourceExe $DestDir

# Список действительно необходимых DLL (те, которые нужно распространять)
$RequiredDlls = @(
    "vcruntime140.dll",
    "vcruntime140_1.dll",
    "msvcp140.dll",
    "msvcp140_1.dll",
    "msvcp140_2.dll",
    "concrt140.dll"
)

# Пути для поиска DLL
$SearchPaths = @(
    "${env:SystemRoot}\System32",
    "${env:SystemRoot}\SysWOW64",
    "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Shared\VC\redist\x64\Microsoft.VC143.CRT",
    "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Shared\VC\redist\x86\Microsoft.VC143.CRT",
    "${env:ProgramFiles(x86)}\Windows Kits\10\Redist\ucrt\DLLs\x64",
    "${env:ProgramFiles(x86)}\Windows Kits\10\Redist\ucrt\DLLs\x86"
)

# Копируем только необходимые DLL
Write-Host "📚 Копирование необходимых DLL..." -ForegroundColor Green
foreach ($dll in $RequiredDlls) {
    $found = $false
    foreach ($path in $SearchPaths) {
        $fullPath = Join-Path $path $dll
        if (Test-Path $fullPath) {
            try {
                Copy-Item $fullPath $DestDir -ErrorAction Stop
                Write-Host "  ✅ Скопирован: $dll" -ForegroundColor Cyan
                $found = $true
                break
            } catch {
                Write-Host "  ⚠️ Ошибка копирования: $dll - $($_.Exception.Message)" -ForegroundColor Yellow
            }
        }
    }
    if (-not $found) {
        Write-Host "  ⚠️ Не найден: $dll" -ForegroundColor Yellow
    }
}

# Скачиваем Visual C++ Redistributable
Write-Host "📥 Скачивание Visual C++ Redistributable..." -ForegroundColor Green
$vcRedistUrl = "https://aka.ms/vs/17/release/vc_redist.x64.exe"
$vcRedistPath = "$DestDir\vc_redist.x64.exe"
try {
    Invoke-WebRequest -Uri $vcRedistUrl -OutFile $vcRedistPath
    Write-Host "  ✅ VC++ Redistributable скачан" -ForegroundColor Cyan
} catch {
    Write-Host "  ⚠️ Не удалось скачать VC++ Redistributable" -ForegroundColor Yellow
}

# Создаем batch-файл для запуска
$batchContent = @"
@echo off
chcp 65001 > nul
echo ====================================
echo    Эмулятор COM-портов
echo ====================================
echo.
echo Проверка наличия Visual C++ Redistributable...
if not exist "%SystemRoot%\System32\vcruntime140.dll" (
    echo Установка Visual C++ Redistributable...
    start /wait vc_redist.x64.exe /quiet
    if errorlevel 1 (
        echo Ошибка установки Visual C++ Redistributable
        pause
        exit /b 1
    )
)
echo.
echo Запуск программы...
start "" "%~dp0VirtualComR.exe"
"@

$batchContent | Out-File -FilePath "$DestDir\run.bat" -Encoding utf8
Write-Host "📝 Создан файл запуска run.bat" -ForegroundColor Green

# Создаем README
$readmeContent = @"
Эмулятор COM-портов
===================

Инструкция по запуску:
1. Убедитесь, что на компьютере установлен Microsoft Visual C++ Redistributable 2015-2022
   - Если не установлен, запустите vc_redist.x64.exe из этой папки
2. Запустите run.bat для старта программы

При возникновении проблем:
- Убедитесь, что все файлы находятся в одной папке
- Проверьте, что Microsoft Visual C++ Redistributable установлен
- Попробуйте запустить от имени администратора

Системные требования:
- Windows 10 или новее
- 64-битная операционная система

Примечание: Системные DLL (kernel32.dll, user32.dll и т.д.) являются частью Windows
и не требуют копирования. Они присутствуют на всех системах Windows.
"@

$readmeContent | Out-File -FilePath "$DestDir\README.txt" -Encoding utf8
Write-Host "📝 Создан файл README.txt" -ForegroundColor Green

Write-Host "`n✨ Готово! Все файлы скопированы в папку $DestDir" -ForegroundColor Green
Write-Host "📋 Теперь вы можете скопировать эту папку на USB-накопитель" -ForegroundColor Yellow

# Открываем папку в проводнике
explorer.exe $DestDir