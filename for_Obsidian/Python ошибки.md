[[Python]]

### Если проблема с установкой какой-либо библиотеки сохраняется, попробуйте пересоздать виртуальное окружение:

```bash
 python3.13 -m venv venv
 source venv/bin/activate
 pip install -r requirements.txt
 pip3 install -r requirements.txt
```

Проблема в том, что скрипт run_remote_test.sh запускает прокси через sudo, но при этом не активирует виртуальное окружение. Давайте исправим это в функции start_proxy:
```bash
# Функция для запуска прокси
start_proxy() {
    print_message "🚀 Запуск прокси..." "$YELLOW"

    # Останавливаем старые процессы
    if ! stop_processes; then
        print_message "❌ Не удалось освободить порт 9999" "$RED"
        return 1
    fi
    
    # Проверяем наличие файла proxyCrypto.py
    if [ ! -f "proxyCrypto.py" ]; then
        print_message "❌ Файл proxyCrypto.py не найден" "$RED"
        return 1
    fi
    
    # Создаем директорию для логов если её нет
    mkdir -p ./logs
    chmod 777 ./logs
    
    # Даем права на запись в лог-файл
    touch ./logs/proxy_crypto.log
    chmod 666 ./logs/proxy_crypto.log
    
    # Проверяем наличие виртуального окружения
    if [ ! -d "venv" ]; then
        print_message "❌ Виртуальное окружение не найдено" "$RED"
        return 1
    fi
    
    # Активируем виртуальное окружение
    source venv/bin/activate
    
    # Проверяем установленные пакеты
    print_message "🔍 Проверяем установленные пакеты..." "$YELLOW"
    pip list | grep -E "cryptography|pycryptodome"
    
    # Запускаем прокси в фоновом режиме
    print_message "📤 Запуск прокси с параметрами:" "$YELLOW"
    print_message "   - listen-ip: 127.0.0.1" "$BLUE"
    print_message "   - listen-port: 9999" "$BLUE"
    print_message "   - target-ip: 138.124.19.67" "$BLUE"
    print_message "   - target-port: 8888" "$BLUE"
    print_message "   - timeout: 300" "$BLUE"
    
    # Запускаем прокси с использованием Python из виртуального окружения
    nohup python3 proxyCrypto.py \
        --listen-ip 127.0.0.1 \
        --listen-port 9999 \
        --target-ip 138.124.19.67 \
        --target-port 8888 \
        --key V1Q4dnRvH-2wdZpERkbW4GdpeX_vdfbWHGHiw_6sx18= \
        --timeout 300 \
        > ./logs/proxy_crypto.log 2>&1 &
    
    PROXY_PID=$!
    
    # Ждем запуска
    sleep 5
        
    # Проверяем, что процесс запустился
    if ! ps -p $PROXY_PID > /dev/null; then
        print_message "❌ Прокси не запустился. Проверяем логи..." "$RED"
        if [ -f "./logs/proxy_crypto.log" ]; then
            tail -n 50 ./logs/proxy_crypto.log
        else
            print_message "❌ Файл логов не создан" "$RED"
        fi
        return 1
    fi
    
    # Проверяем, что порт открыт (UDP)
    if ! lsof -i :9999 -P -n | grep "UDP" > /dev/null; then
        print_message "❌ Прокси запущен, но порт 9999 не открыт" "$RED"
        print_message "📋 Проверяем логи..." "$YELLOW"
        if [ -f "./logs/proxy_crypto.log" ]; then
            tail -n 50 ./logs/proxy_crypto.log
        fi
        return 1
    fi
    
    print_message "✅ Прокси успешно запущен (PID: $PROXY_PID)" "$GREEN"
    return 0
}

```
