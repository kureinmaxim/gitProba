# Путь к приложению
$AppPath = "C:\Project\Project_Rust\VirtualComR\target\release\VirtualComR.exe"

# Проверяем существование файла
if (-not (Test-Path $AppPath)) {
    Write-Host "❌ Файл не найден: $AppPath" -ForegroundColor Red
    exit 1
}

# Создаем временную директорию для Dependencies
$ToolsDir = "$env:TEMP\Dependencies"
New-Item -ItemType Directory -Path $ToolsDir -Force | Out-Null

# Скачиваем Dependencies
Write-Host "📥 Скачивание Dependencies..." -ForegroundColor Green
$DependenciesUrl = "https://github.com/lucasg/Dependencies/releases/download/v1.11/Dependencies_x64_Release.zip"
$DependenciesZip = "$ToolsDir\Dependencies.zip"
try {
    Invoke-WebRequest -Uri $DependenciesUrl -OutFile $DependenciesZip
    Expand-Archive -Path $DependenciesZip -DestinationPath $ToolsDir -Force
    Write-Host "✅ Dependencies скачан и распакован" -ForegroundColor Green
} catch {
    Write-Host "❌ Ошибка при скачивании Dependencies: $_" -ForegroundColor Red
    exit 1
}

# Запускаем Dependencies с параметрами для анализа
Write-Host "`n🔍 Запуск анализа зависимостей..." -ForegroundColor Green
$DependenciesExe = "$ToolsDir\Dependencies.exe"
$OutputFile = "$ToolsDir\dependencies_output.txt"

# Запускаем Dependencies с параметрами для анализа и сохранения в файл
Start-Process -FilePath $DependenciesExe -ArgumentList "-chain", $AppPath, "-output", $OutputFile -Wait

# Читаем результаты
if (Test-Path $OutputFile) {
    $Dlls = Get-Content $OutputFile | Where-Object { $_ -match '\.dll$' } | ForEach-Object { $_.Trim() }
    
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

    $NonSystemDlls = $Dlls | Where-Object { $_ -notin $SystemDlls } | Select-Object -Unique

    # Сохраняем результаты в файл на рабочем столе
    $DesktopPath = [Environment]::GetFolderPath("Desktop")
    $outputPath = Join-Path $DesktopPath "dll2rust_dependencies.txt"
    $NonSystemDlls | Out-File $outputPath -Encoding utf8

    Write-Host "`n📋 Найденные DLL (исключая системные):" -ForegroundColor Cyan
    $NonSystemDlls | ForEach-Object { Write-Host $_ }

    Write-Host "`n💾 Список сохранен в файл: $outputPath" -ForegroundColor Green

    # Открываем файл в блокноте
    notepad.exe $outputPath
} else {
    Write-Host "❌ Не удалось получить результаты анализа" -ForegroundColor Red
}

# Очищаем временные файлы
Write-Host "`n🧹 Очистка временных файлов..." -ForegroundColor Green
Remove-Item -Path $ToolsDir -Recurse -Force
Write-Host "✅ Временные файлы удалены" -ForegroundColor Green 