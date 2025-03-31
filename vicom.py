import serial
import serial.tools.list_ports
import sys
import threading
import time

# Значения по умолчанию
DEFAULT_SETTINGS = {
    "baudrate": 38400,
    "bytesize": serial.EIGHTBITS,
    "parity": serial.PARITY_NONE,
    "stopbits": serial.STOPBITS_ONE
}

POLYNOMIAL = 0xA001  # Стандартный полином для CRC16-MODBUS

def calculate_crc16(data: bytes) -> int:
    """
    Вычисляет CRC16 для переданных данных.
    Аналог алгоритма из C-кода.
    """
    crc = 0xFFFF

    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ POLYNOMIAL
            else:
                crc >>= 1

    return crc

def receive_data(ser):
    """Функция для приема и обработки данных в отдельном потоке"""
    while ser.is_open:
        try:
            if ser.in_waiting:
                request = ser.read(ser.in_waiting)
                print(f"\n📥 Получен запрос: {' '.join(f'{b:02X}' for b in request)}")
                response = process_request(request)
                if response:
                    ser.write(response)
                    print(f"📤 Отправлен ответ: {' '.join(f'{b:02X}' for b in response)}")
                print("\nВыберите действие (1-4): ", end='', flush=True)
            time.sleep(0.1)
        except Exception as e:
            print(f"\n⚠️ Ошибка при приеме данных: {e}")
            break

def send_hex_data(ser, hex_string: str):
    """Отправка HEX данных в порт"""
    try:
        hex_string = hex_string.replace(" ", "")
        if not all(c in '0123456789ABCDEFabcdef' for c in hex_string):
            print("❌ Ошибка: неверный формат HEX данных")
            return
        
        data = bytes.fromhex(hex_string)
        ser.write(data)
        print(f"📤 Отправлено (HEX): {' '.join(f'{b:02X}' for b in data)}")
    except ValueError:
        print("❌ Ошибка: неверный формат HEX данных")

def send_hex_data_with_crc(ser, hex_string: str):
    """Отправка HEX данных в порт с добавлением CRC16"""
    try:
        hex_string = hex_string.replace(" ", "")
        if not all(c in '0123456789ABCDEFabcdef' for c in hex_string):
            print("❌ Ошибка: неверный формат HEX данных")
            return
        
        data = bytes.fromhex(hex_string)
        crc = calculate_crc16(data)
        
        # Добавляем CRC к данным (младший байт первый)
        final_data = data + bytes([crc & 0xFF, (crc >> 8) & 0xFF])
        
        ser.write(final_data)
        print(f"📤 Отправлено (HEX+CRC): {' '.join(f'{b:02X}' for b in data)} | CRC: {crc & 0xFF:02X} {(crc >> 8) & 0xFF:02X}")
        
    except ValueError:
        print("❌ Ошибка: неверный формат HEX данных")

def send_text_message(ser, message: str):
    """Отправка текстового сообщения в порт"""
    data = message.encode('utf-8')
    ser.write(data)
    print(f"📤 Отправлено (текст): {message}")

def show_menu():
    """Отображение меню команд"""
    print("\n=== 📋 Меню команд ===")
    print("1. Отправить текстовое сообщение")
    print("2. Отправить HEX данные")
    print("3. Отправить HEX данные с CRC16")
    print("4. Очистить экран")
    print("5. Выход")
    print("\nВыберите действие (1-5): ", end='', flush=True)

def list_available_ports():
    """Возвращает список доступных COM-портов и выводит их на экран."""
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("❌ Нет доступных последовательных портов!")
        return []

    print("\n🔌 Доступные порты:")
    for i, port in enumerate(ports, start=1):
        print(f"  {i}. {port.device}")

    return ports

def select_port():
    """Позволяет выбрать COM-порт по номеру."""
    ports = list_available_ports()
    if not ports:
        return None

    while True:
        try:
            selected_index = int(input("\nВведите номер порта: ")) - 1
            if 0 <= selected_index < len(ports):
                return ports[selected_index].device
            print("⚠️ Ошибка: введите корректный номер порта!")
        except ValueError:
            print("⚠️ Ошибка: введите число!")

def choose_configuration_mode():
    """Выбор режима настройки порта"""
    print("\n=== ⚙  Настройка последовательного порта ===")
    print("1. Использовать настройки по умолчанию")
    print("   (38400 бод, 8 бит, без паритета, 1 стоп-бит)")
    print("2. Ручная настройка параметров")

    while True:
        choice = input("Выберите режим настройки (1/2): ").strip()
        if choice == '1':
            return DEFAULT_SETTINGS
        elif choice == '2':
            return None
        else:
            print("⚠️ Некорректный выбор. Пожалуйста, введите 1 или 2.")

def choose_option(prompt, options):
    """Позволяет выбрать один из предложенных вариантов."""
    print(f"\n{prompt}")
    for i, option in enumerate(options, start=1):
        print(f"  {i}. {option}")

    while True:
        try:
            selected_index = int(input("Выберите номер: ")) - 1
            if 0 <= selected_index < len(options):
                return options[selected_index]
            print("⚠️ Ошибка: выберите корректный номер!")
        except ValueError:
            print("⚠️ Ошибка: введите число!")

def full_port_configuration():
    """Полная ручная настройка порта"""
    baudrate = choose_option("Выберите скорость передачи (бод):",
                             [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200])

    bytesize_options = {
        "5 бит": serial.FIVEBITS,
        "6 бит": serial.SIXBITS,
        "7 бит": serial.SEVENBITS,
        "8 бит (стандарт)": serial.EIGHTBITS
    }
    bytesize = choose_option("Выберите размер байта:", list(bytesize_options.keys()))
    bytesize = bytesize_options[bytesize]

    parity_options = {
        "Нет": serial.PARITY_NONE,
        "Четный (Even)": serial.PARITY_EVEN,
        "Нечетный (Odd)": serial.PARITY_ODD,
        "Маркер (Mark)": serial.PARITY_MARK,
        "Пробел (Space)": serial.PARITY_SPACE
    }
    parity = choose_option("Выберите паритет:", list(parity_options.keys()))
    parity = parity_options[parity]

    stopbits = choose_option("Выберите количество стоп-битов:",
                             [serial.STOPBITS_ONE, serial.STOPBITS_ONE_POINT_FIVE, serial.STOPBITS_TWO])

    return {
        "baudrate": baudrate,
        "bytesize": bytesize,
        "parity": parity,
        "stopbits": stopbits
    }

def process_request(request):
    """Логика обработки запросов."""
    if request == bytes([0x01, 0x02, 0x03]):
        return bytes([0x01, 0x0C])
    elif request == bytes([0x41]):
        return bytes([0x20, 0x00])
    elif request == bytes([0xAA, 0xBB, 0xCC]):
        return bytes([0xDD, 0xEE])
    elif len(request) == 3 and request[0] == 0x01:
        return bytes([request[0], request[1] + 10])
    return None

def main():
    while True:  # Цикл для повторного выбора порта
        try:
            port = select_port()
            if not port:
                print("❌ Выход: последовательный порт не выбран!")
                sys.exit(0)

            settings = choose_configuration_mode()
            if settings is None:
                settings = full_port_configuration()

            ser = None
            try:
                ser = serial.Serial(
                    port=port,
                    baudrate=settings["baudrate"],
                    bytesize=settings["bytesize"],
                    parity=settings["parity"],
                    stopbits=settings["stopbits"],
                    timeout=1
                )
            except serial.SerialException as e:
                print(f"\n❌ Ошибка открытия порта {port}: {str(e)}")
                print("💡 Возможные причины:")
                print("   - Порт используется другой программой")
                print("   - Недостаточно прав доступа")
                print("   - Устройство было отключено")
                
                while True:
                    retry = input("\nПопробовать выбрать другой порт? (y/n): ").lower().strip()
                    if retry in ['y', 'n']:
                        break
                    print("Пожалуйста, введите 'y' или 'n'")
                
                if retry == 'n':
                    print("\n👋 До свидания!")
                    sys.exit(0)
                continue

            if not ser or not ser.is_open:
                continue

            print(f"\n✅ Соединение установлено: Порт 📌: {ser.port} @ {ser.baudrate} бод @ {ser.bytesize} @ {ser.parity} @ {ser.stopbits}")
            print("\n🔄 Эмулятор готов к работе.")

            # Запускаем поток приема данных
            receiver_thread = threading.Thread(target=receive_data, args=(ser,), daemon=True)
            receiver_thread.start()

            try:
                while True:
                    show_menu()
                    choice = input().strip()

                    if choice == '1':
                        message = input("Введите текстовое сообщение: ")
                        send_text_message(ser, message)
                    elif choice == '2':
                        hex_data = input("Введите HEX данные (например: FF 00 AB или FF00AB): ")
                        send_hex_data(ser, hex_data)
                    elif choice == '3':
                        hex_data = input("Введите HEX данные для отправки с CRC16: ")
                        send_hex_data_with_crc(ser, hex_data)
                    elif choice == '4':
                        # Очистка экрана
                        import os
                        os.system('cls' if os.name == 'nt' else 'clear')
                    elif choice == '5':
                        print("\n👋 До свидания!")
                        break
                    else:
                        print("⚠️ Неверный выбор. Пожалуйста, выберите 1-5")

            except KeyboardInterrupt:
                print("\n⏹ Остановка эмуляции")
            finally:
                if ser and ser.is_open:
                    ser.close()
                if 'receiver_thread' in locals():
                    receiver_thread.join(timeout=1.0)
                break  # Выходим из внешнего цикла

        except KeyboardInterrupt:
            print("\n🚪 Завершение работы по Ctrl + C")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Неожиданная ошибка: {e}")
            retry = input("\nПопробовать снова? (y/n): ").lower().strip()
            if retry != 'y':
                sys.exit(1)
            continue

if __name__ == "__main__":
    main()
