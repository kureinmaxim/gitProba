import serial
import serial.tools.list_ports
import sys

# Значения по умолчанию
DEFAULT_SETTINGS = {
    "baudrate": 38400,
    "bytesize": serial.EIGHTBITS,
    "parity": serial.PARITY_NONE,
    "stopbits": serial.STOPBITS_ONE
}


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
    print(f"Получен запрос: {request.hex()}")
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
    try:
        port = select_port()
        if not port:
            print("❌ Выход: последовательный порт не выбран!")
            sys.exit(0)

        settings = choose_configuration_mode()
        if settings is None:
            settings = full_port_configuration()

        ser = serial.Serial(
            port=port,
            baudrate=settings["baudrate"],
            bytesize=settings["bytesize"],
            parity=settings["parity"],
            stopbits=settings["stopbits"],
            timeout=1
        )

        print(f"\n✅ Соединение установлено: Порт 📌: {ser.port} @ {ser.baudrate} бод @ {ser.bytesize} @ {ser.parity} @ {ser.stopbits}" )
        print("\n🔄 Эмулятор готов к работе. 📍 Используйте Ctrl+C для остановки.")

        try:
            while True:
                if ser.in_waiting:
                    request = ser.read(ser.in_waiting)
                    response = process_request(request)
                    if response:
                        ser.write(response)
                        print(f"📤 Отправлен ответ: {response.hex()}")

        except KeyboardInterrupt:
            print("\n ⏹  Остановка эмуляции")
        finally:
            ser.close()

    except KeyboardInterrupt:
        print("\n🚪 Завершение работы по Ctrl + C")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
