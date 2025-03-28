import serial
import serial.tools.list_ports
import sys


class DeviceEmulator:
    def __init__(self):
        self.default_settings = {
            'baudrate': 38400,
            'bytesize': serial.EIGHTBITS,
            'parity': serial.PARITY_NONE,
            'stopbits': serial.STOPBITS_ONE
        }
        self.port_settings = self.configure_port_settings()
        self.serial_connection = None

    @staticmethod
    def select_port():
        """Интерактивный выбор последовательного порта"""
        ports = list(serial.tools.list_ports.comports())

        if not ports:
            print("Нет доступных последовательных портов!")
            return None

        print("\n=== Доступные последовательные порты ===")
        for i, port in enumerate(ports, 1):
            print(f"{i}. {port.device} - {port.description}")

        while True:
            try:
                choice = input("\nВведите номер порта (или 'q' для выхода): ").strip()

                if choice.lower() == 'q':
                    print("Выход из программы.")
                    sys.exit(0)

                choice = int(choice)

                if 1 <= choice <= len(ports):
                    return ports[choice - 1]
                else:
                    print("Некорректный номер порта. Попробуйте снова.")

            except ValueError:
                print("Пожалуйста, введите корректный номер порта или 'q' для выхода.")

    def choose_configuration_mode(self):
        """Выбор режима настройки порта"""
        print("\n=== Настройка последовательного порта ===")
        print("1. Использовать настройки по умолчанию")
        print("   (38400 бод, 8 бит, без паритета, 1 стоп-бит)")
        print("2. Ручная настройка параметров")

        while True:
            try:
                choice = input("Выберите режим настройки (1/2): ").strip()

                if choice == '1':
                    return self.default_settings
                elif choice == '2':
                    return None
                else:
                    print("Некорректный выбор. Пожалуйста, введите 1 или 2.")

            except ValueError:
                print("Пожалуйста, введите корректный номер.")

    def full_port_configuration(self):
        """Полная ручная настройка порта"""
        # Выбор порта
        selected_port = self.select_port()
        if not selected_port:
            sys.exit(1)

        # Настройки по умолчанию
        settings = {
            'port': selected_port.device,
            'baudrate': 9600,
            'bytesize': serial.EIGHTBITS,
            'parity': serial.PARITY_NONE,
            'stopbits': serial.STOPBITS_ONE,
            'timeout': 1
        }

        # Настройка baudrate
        print("\n=== Настройка baudrate ===")
        common_baudrates = [9600, 19200, 38400, 57600, 115200]
        print("Стандартные скорости:")
        for i, rate in enumerate(common_baudrates, 1):
            print(f"{i}. {rate}")
        print("0. Ввести другое значение")

        while True:
            try:
                rate_choice = input("Выберите скорость передачи: ").strip()
                rate_choice = int(rate_choice)

                if 1 <= rate_choice <= len(common_baudrates):
                    settings['baudrate'] = common_baudrates[rate_choice - 1]
                    break
                elif rate_choice == 0:
                    custom_rate = int(input("Введите пользовательскую скорость: "))
                    settings['baudrate'] = custom_rate
                    break
                else:
                    print("Некорректный выбор. Попробуйте снова.")
            except ValueError:
                print("Пожалуйста, введите корректное число.")

        # Настройка битов данных
        print("\n=== Выбор битов данных ===")
        byte_sizes = {
            1: serial.FIVEBITS,
            2: serial.SIXBITS,
            3: serial.SEVENBITS,
            4: serial.EIGHTBITS
        }
        print("1. 5 бит\n2. 6 бит\n3. 7 бит\n4. 8 бит")

        while True:
            try:
                bytesize_choice = int(input("Выберите количество бит данных: ").strip())
                if bytesize_choice in byte_sizes:
                    settings['bytesize'] = byte_sizes[bytesize_choice]
                    break
                else:
                    print("Некорректный выбор. Попробуйте снова.")
            except ValueError:
                print("Пожалуйста, введите корректное число.")

        # Настройка паритета
        print("\n=== Выбор паритета ===")
        parity_options = {
            1: serial.PARITY_NONE,
            2: serial.PARITY_EVEN,
            3: serial.PARITY_ODD,
            4: serial.PARITY_MARK,
            5: serial.PARITY_SPACE
        }
        print("1. Нет (None)\n2. Четный (Even)\n3. Нечетный (Odd)\n4. Маркер (Mark)\n5. Пробел (Space)")

        while True:
            try:
                parity_choice = int(input("Выберите тип паритета: ").strip())
                if parity_choice in parity_options:
                    settings['parity'] = parity_options[parity_choice]
                    break
                else:
                    print("Некорректный выбор. Попробуйте снова.")
            except ValueError:
                print("Пожалуйста, введите корректное число.")

        # Настройка стоп-битов
        print("\n=== Выбор стоп-битов ===")
        stopbits_options = {
            1: serial.STOPBITS_ONE,
            2: serial.STOPBITS_TWO,
            3: serial.STOPBITS_ONE_POINT_FIVE
        }
        print("1. 1 стоп-бит\n2. 2 стоп-бита\n3. 1.5 стоп-бита")

        while True:
            try:
                stopbits_choice = int(input("Выберите количество стоп-битов: ").strip())
                if stopbits_choice in stopbits_options:
                    settings['stopbits'] = stopbits_options[stopbits_choice]
                    break
                else:
                    print("Некорректный выбор. Попробуйте снова.")
            except ValueError:
                print("Пожалуйста, введите корректное число.")

        # Вывод итоговых настроек
        print("\n=== Итоговые настройки порта ===")
        print(f"Порт: {settings['port']}")
        print(f"Скорость: {settings['baudrate']} бод")
        print(f"Биты данных: {settings['bytesize']} бит")
        print(f"Паритет: {settings['parity']}")
        print(f"Стоп-биты: {settings['stopbits']}")

        return settings

    def configure_port_settings(self):
        """Конфигурация настроек порта"""
        # Выбор режима настройки
        default_settings = self.choose_configuration_mode()

        # Если выбраны настройки по умолчанию
        if default_settings:
            selected_port = self.select_port()
            if not selected_port:
                sys.exit(1)

            settings = {
                'port': selected_port.device,
                'baudrate': default_settings['baudrate'],
                'bytesize': default_settings['bytesize'],
                'parity': default_settings['parity'],
                'stopbits': default_settings['stopbits'],
                'timeout': 1
            }

            # Вывод итоговых настроек
            print("\n=== Итоговые настройки порта ===")
            print(f"Порт: {settings['port']}")
            print(f"Скорость: {settings['baudrate']} бод")
            print(f"Биты данных: {settings['bytesize']} бит")
            print(f"Паритет: {settings['parity']}")
            print(f"Стоп-биты: {settings['stopbits']}")

            return settings

        # Если выбрана полная настройка
        return self.full_port_configuration()

    def open_connection(self):
        """Открытие последовательного соединения с выбранными настройками"""
        try:
            self.serial_connection = serial.Serial(
                port=self.port_settings['port'],
                baudrate=self.port_settings['baudrate'],
                bytesize=self.port_settings['bytesize'],
                parity=self.port_settings['parity'],
                stopbits=self.port_settings['stopbits'],
                timeout=1
            )
            print(f"\nПодключение установлено: {self.serial_connection.port}")
        except serial.SerialException as e:
            print(f"Ошибка подключения: {e}")
            sys.exit(1)

    @staticmethod
    def process_request(request):
        """Логика обработки запросов"""
        print(f"Получен запрос: {request.hex()}")

        # Эмуляция устройства с различными откликами
        if request == bytes([0x01, 0x02, 0x03]):
            return bytes([0x01, 0x0C])

        elif request == bytes([0xAA, 0xBB, 0xCC]):
            return bytes([0xDD, 0xEE])

        elif len(request) == 3 and request[0] == 0x01:
            return bytes([request[0], request[1] + 10])

        else:
            return bytes([0x00, 0x00])

    def start_emulation(self):
        self.open_connection()

        print("Эмулятор готов к работе. Используйте Ctrl+C для остановки.")
        try:
            while True:
                if self.serial_connection.in_waiting:
                    request = self.serial_connection.read(self.serial_connection.in_waiting)
                    response = self.process_request(request)
                    self.serial_connection.write(response)
                    print(f"Отправлен ответ: {response.hex()}")
        except KeyboardInterrupt:
            print("\nОстановка эмуляции")
        finally:
            if self.serial_connection:
                self.serial_connection.close()


def main():
    try:
        emulator = DeviceEmulator()
        emulator.start_emulation()
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")


if __name__ == "__main__":
    main()