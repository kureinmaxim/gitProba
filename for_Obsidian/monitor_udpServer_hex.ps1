# 1. Узнай имя/номер loopback интерфейса: tshark -D
# 2. Замени <LoopbackInterface> на правильное значение.
# 3. Запускай эту команду в PowerShell от имени Администратора.

# --- Начало скрипта ---
# Изменено: Название отображает вывод HEX
Write-Host "Запуск мониторинга UDP порта 8888 на loopback интерфейсе (вывод HEX)..."
Write-Host "Для остановки нажмите Ctrl+C"

# !!! ВАЖНО: Замените <LoopbackInterface> ниже на реальный номер или имя !!!
# !!!      (полученное из вывода команды 'tshark -D')                !!!
# $loopbackInterface = "<LoopbackInterface>"
$loopbackInterface = "\Device\NPF_Loopback" # Оставляем как есть, раз работало
$udpPort = 8888

# Проверяем, что tshark доступен
if (-not (Get-Command tshark.exe -ErrorAction SilentlyContinue)) {
    Write-Error "Команда tshark.exe не найдена. Убедитесь, что Wireshark установлен и его директория добавлена в PATH."
    exit 1 # Выходим из скрипта
}

# Удалено: Проверка jq больше не нужна
# # Проверяем, что jq доступен
# if (-not (Get-Command jq -ErrorAction SilentlyContinue)) {
#     Write-Error "Команда jq не найдена. Убедитесь, что jq установлен и доступен в PATH."
#     exit 1 # Выходим из скрипта
# }

# Проверяем, что интерфейс был указан
if ($loopbackInterface -eq "<LoopbackInterface>") {
     Write-Error "Необходимо указать правильный loopback интерфейс в переменной `$loopbackInterface внутри скрипта. Запустите 'tshark -D' для его определения."
     exit 1
}


Write-Host "Используется интерфейс: $loopbackInterface"
Write-Host "Прослушивается порт: $udpPort"
Write-Host "--- Начало вывода данных ---"

# Основная команда
try {
    # Изменено: Добавлен флаг -q tshark для подавления сообщения "Capturing on..."
    tshark.exe -i $loopbackInterface -l -q -Y "udp.port == $udpPort" -T fields -e data | ForEach-Object {
        $hexString = $_.Trim()

        if ($hexString.Length -gt 0 -and $hexString -match '^[0-9a-fA-F]+$') {
            # Изменено: Убрана обработка JSON, просто выводим HEX
            # try {
            #     # Конвертируем HEX в байты
            #     $bytes = [System.Convert]::FromHexString($hexString)
            #     # Конвертируем байты в строку (предполагаем UTF-8)
            #     $text = [System.Text.Encoding]::UTF8.GetString($bytes)
            #
            #     # Передаем содержимое переменной $text на стандартный ввод jq.exe
            #     $text | jq.exe '.'
            #
            # } catch [System.FormatException] {
            #      Write-Warning "Пропущена невалидная hex-строка: $hexString"
            # } catch [System.ArgumentException] {
            #      Write-Warning "Пропущена невалидная hex-строка (нечетная длина?): $hexString"
            # } catch {
            #      # Эта ошибка теперь будет ловить проблемы при выполнении jq или если $text невалиден для jq
            #      Write-Warning "Ошибка обработки строки '$hexString' или выполнения jq: $($_.Exception.Message)"
            #      # Если хочешь видеть не-JSON данные, раскомментируй строку ниже:
            #      Write-Host "Необработанные данные для jq: $text"
            # }
            Write-Host "HEX Data: $hexString" # Просто выводим HEX
        } elseif ($hexString.Length -gt 0) {
             # Строка не пустая, но не является валидным hex
             Write-Warning "Пропущена строка, не содержащая только hex символы: $hexString"
        }
        # Пустые строки просто игнорируются
    }
} finally {
     Write-Host "--- Мониторинг остановлен ---"
}

# --- Конец скрипта ---
