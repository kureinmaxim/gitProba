# Путь к приложению
$AppPath = "C:\Project\Project_Rust\VirtualComR\target\release\VirtualComR.exe"

# Проверяем существование файла
if (-not (Test-Path $AppPath)) {
    Write-Host "❌ Файл не найден: $AppPath" -ForegroundColor Red
    exit 1
}

# Расширенный список путей для поиска dumpbin.exe
$DumpbinPaths = @(
    # Visual Studio 2022
    "${env:ProgramFiles(x86)}\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\*\bin\Hostx64\x64",
    "${env:ProgramFiles(x86)}\Microsoft Visual Studio\2022\Professional\VC\Tools\MSVC\*\bin\Hostx64\x64",
    "${env:ProgramFiles(x86)}\Microsoft Visual Studio\2022\Enterprise\VC\Tools\MSVC\*\bin\Hostx64\x64",
    # Visual Studio 2019
    "${env:ProgramFiles(x86)}\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\*\bin\Hostx64\x64",
    "${env:ProgramFiles(x86)}\Microsoft Visual Studio\2019\Professional\VC\Tools\MSVC\*\bin\Hostx64\x64",
    "${env:ProgramFiles(x86)}\Microsoft Visual Studio\2019\Enterprise\VC\Tools\MSVC\*\bin\Hostx64\x64",
    # Windows SDK
    "${env:ProgramFiles(x86)}\Windows Kits\10\bin\*\x64",
    # Дополнительные пути
    "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Shared\VC\Tools\MSVC\*\bin\Hostx64\x64",
    "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Shared\Tools\MSVC\*\bin\Hostx64\x64"
)

# Ищем dumpbin.exe
$DumpbinPath = $null
foreach ($path in $DumpbinPaths) {
    $possiblePaths = Get-ChildItem -Path $path -Filter "dumpbin.exe" -Recurse -ErrorAction SilentlyContinue
    if ($possiblePaths) {
        $DumpbinPath = $possiblePaths[0].FullName
        Write-Host "✅ Найден dumpbin.exe: $DumpbinPath" -ForegroundColor Green
        break
    }
}

if (-not $DumpbinPath) {
    Write-Host "❌ Не найден dumpbin.exe. Попробуем альтернативный метод..." -ForegroundColor Yellow
    
    # Пробуем найти через where.exe
    $whereResult = where.exe dumpbin.exe 2>$null
    if ($whereResult) {
        $DumpbinPath = $whereResult[0]
        Write-Host "✅ Найден dumpbin.exe через where.exe: $DumpbinPath" -ForegroundColor Green
    } else {
        Write-Host "❌ Не удалось найти dumpbin.exe. Убедитесь, что:" -ForegroundColor Red
        Write-Host "1. Установлен Visual Studio с компонентами для разработки на C++" -ForegroundColor Yellow
        Write-Host "2. Установлен Windows SDK" -ForegroundColor Yellow
        Write-Host "3. Компоненты добавлены в PATH" -ForegroundColor Yellow
        Write-Host "`nПопробуйте:" -ForegroundColor Cyan
        Write-Host "1. Открыть Visual Studio Installer" -ForegroundColor White
        Write-Host "2. Изменить установку Visual Studio" -ForegroundColor White
        Write-Host "3. Убедиться, что установлен компонент 'Средства сборки C++'" -ForegroundColor White
        exit 1
    }
}

Write-Host "`n🔍 Анализ зависимостей для $AppPath..." -ForegroundColor Green

# Получаем список зависимостей
$dependencies = & $DumpbinPath /dependents $AppPath | Select-String -Pattern "\.dll$"

# Фильтруем и выводим только DLL
Write-Host "`n📋 Список зависимых DLL:" -ForegroundColor Cyan
$dependencies | ForEach-Object {
    $dll = $_.Line.Trim()
    if ($dll -match '\.dll$') {
        Write-Host $dll
    }
}

# Сохраняем список в файл
$outputPath = "$env:USERPROFILE\Desktop\dll2rust.txt"
$dependencies | Where-Object { $_.Line -match '\.dll$' } | ForEach-Object { $_.Line.Trim() } | Out-File $outputPath -Encoding utf8
Write-Host "`n💾 Список сохранен в файл: $outputPath" -ForegroundColor Green

# Открываем файл в блокноте
notepad.exe $outputPath