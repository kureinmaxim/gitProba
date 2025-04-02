#comport 

==com0com - это популярное решение для Windows, но есть и другие варианты, а также аналоги для macOS.==

**Для Windows 10:**

1. com0com: Собственно, сама программа com0com отлично работает на Windows 10 (и более новых версиях). 
2. Eltima Virtual Serial Port Driver (VSPD): Мощное коммерческое решение с множеством функций (создание пар, разделение, объединение портов). 
3. FabulaTech Virtual Serial Port Kit: Еще одно коммерческое решение, похожее по функциональности на Eltima VSPD.
4. VSPE (Virtual Serial Ports Emulator): Есть бесплатная версия для 32-битных систем, которая позволяет создавать пары портов. Для 64-битных систем и более сложной функциональности (например, эмуляция TCP-сервера/клиента) требуется платная лицензия.
5. HW VSP3 - Virtual Serial Port: Бесплатная утилита, в основном предназначенная для создания виртуального COM-порта, который подключается к удаленному TCP-серверу (например, к аппаратному преобразователю Serial-to-Ethernet), но может иметь и другие режимы.

**Для macOS:**

В macOS нет концепции COM-портов в том же виде, что и в Windows. Вместо этого используются файлы устройств в /dev/, такие как /dev/tty.* и /dev/cu.*. Эмуляция "соединенных" портов обычно достигается с помощью псевдотерминалов (pty).

1. **socat**: Это очень мощная и гибкая утилита командной строки. Она может создавать пару псевдотерминалов (pty), которые ведут себя как соединенные последовательные порты. Устанавливается обычно через менеджер пакетов, например, Homebrew (brew install socat).
```bash
socat PTY,raw,echo=0,link=/tmp/vport1 PTY,raw,echo=0,link=/tmp/vport2
```

Это создаст два устройства (/tmp/vport1 и /tmp/vport2), через которые программы смогут общаться. Реальные имена устройств pty будут выведены socat при запуске (например, /dev/ttys005, /dev/ttys006).

2. **Программные решения**: Можно написать скрипты (например, на Python с использованием модуля pty), которые создают и управляют парами псевдотерминалов для более специфических нужд.

Модуль pty в Python (доступен в основном на Unix-подобных системах, включая macOS и Linux) позволяет работать с псевдотерминалами. С его помощью можно создать пару "master" и "slave" псевдотерминалов. Программы могут подключаться к "slave"-устройству так, как будто это обычный последовательный порт или терминал, а ваш скрипт будет управлять "master"-концом, читая и записывая данные.

Чтобы эмулировать пару соединенных портов, как в com0com или socat PTY PTY, нам нужно создать две такие пары master/slave и перенаправлять данные между master-концами.

---

Вот пример простого скрипта на Python, который создает два псевдотерминала (slave) и соединяет их так, что всё, что записано в один, появляется на другом, и наоборот:
```python
import pty
import os
import select
import threading
import fcntl
import termios
import time

def pipe_data(fd_in, fd_out, stop_event):
    """Читает из fd_in и пишет в fd_out."""
    while not stop_event.is_set():
        # Ждем, пока данные будут доступны для чтения
        readable, _, _ = select.select([fd_in], [], [], 0.1)
        if fd_in in readable:
            try:
                data = os.read(fd_in, 1024)
                if not data:  # EOF
                    print(f"EOF on fd {fd_in}, stopping pipe.")
                    stop_event.set()
                    break
                os.write(fd_out, data)
            except OSError as e:
                print(f"Error piping data from fd {fd_in} to {fd_out}: {e}")
                stop_event.set()
                break

def main():
    # Создаем первую пару master/slave
    master1, slave1 = pty.openpty()
    # Создаем вторую пару master/slave
    master2, slave2 = pty.openpty()

    # Получаем имена slave-устройств (это то, к чему будут подключаться программы)
    slave1_name = os.ttyname(slave1)
    slave2_name = os.ttyname(slave2)

    print(f"Virtual serial port pair created:")
    print(f"  Port 1: {slave1_name}")
    print(f"  Port 2: {slave2_name}")
    print("Press Ctrl+C to stop.")

    # Устанавливаем неблокирующий режим для master-концов
    # (Важно для select и чтобы read не зависал навсегда)
    fcntl.fcntl(master1, fcntl.F_SETFL, os.O_NONBLOCK)
    fcntl.fcntl(master2, fcntl.F_SETFL, os.O_NONBLOCK)

    # Устанавливаем атрибуты терминала (raw mode) для slave-концов,
    # чтобы они вели себя как последовательные порты, а не интерактивные терминалы
    # (отключаем echo, обработку спец. символов и т.д.)
    for fd in [slave1, slave2]:
      attrs = termios.tcgetattr(fd)
      # Установка Raw mode
      attrs[0] &= ~(termios.IGNBRK | termios.BRKINT | termios.PARMRK | termios.ISTRIP | termios.INLCR | termios.IGNCR | termios.ICRNL | termios.IXON)
      attrs[1] &= ~termios.OPOST # Отключение выходной обработки
      attrs[2] &= ~(termios.CSIZE | termios.PARENB)
      attrs[2] |= termios.CS8 # 8 бит данных
      attrs[3] &= ~(termios.ECHO | termios.ECHONL | termios.ICANON | termios.ISIG | termios.IEXTEN) # Отключение канонического режима, эха и сигналов
      attrs[6][termios.VMIN] = 1 # Читать минимум 1 байт
      attrs[6][termios.VTIME] = 0 # Без таймаута
      termios.tcsetattr(fd, termios.TCSANOW, attrs)


    stop_event = threading.Event()

    # Создаем потоки для перенаправления данных
    thread1 = threading.Thread(target=pipe_data, args=(master1, master2, stop_event))
    thread2 = threading.Thread(target=pipe_data, args=(master2, master1, stop_event))

    thread1.start()
    thread2.start()

    try:
        # Ждем завершения потоков (или прерывания Ctrl+C)
        while thread1.is_alive() and thread2.is_alive():
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping...")
        stop_event.set()

    thread1.join()
    thread2.join()

    # Закрываем файловые дескрипторы
    os.close(master1)
    os.close(slave1)
    os.close(master2)
    os.close(slave2)

    print("Ports closed.")

if __name__ == "__main__":
    main()
```

1. Сохраните код как virtual_serial_pair.py.
2. Запустите его из терминала: python virtual_serial_pair.py.
3. Скрипт выведет имена созданных slave-устройств (например, /dev/ptyp0 и /dev/ptyp1 или /dev/ttys005 и /dev/ttys006 на macOS).
4. Теперь вы можете использовать эти два имени файлов устройств в своих программах как концы виртуального нуль-модемного кабеля. Например, одна программа может открыть /dev/ptyp0 для записи, а другая - /dev/ptyp1 для чтения, и наоборот.

Важные моменты:
- Unix-like: Этот скрипт будет работать только на macOS и Linux. Модуль pty недоступен на Windows.
- Права доступа: В зависимости от системы, созданные устройства /dev/pty* могут требовать определенных прав доступа для использования другими программами. Возможно, потребуется запускать скрипт или клиентские программы с sudo или настроить правила udev (в Linux).
- Надежность: Это базовый пример. В реальном приложении может потребоваться более сложная обработка ошибок, управление буферами, обработка сигналов управления модемом (если это необходимо) и более надежная логика завершения.
- Терминальные атрибуты: Настройка termios.tcsetattr важна, чтобы псевдотерминал вел себя как "прозрачный" канал передачи данных, а не как интерактивный терминал (без эха, канонического режима и т.д.).

Этот скрипт демонстрирует основной принцип создания виртуальной пары последовательных портов с помощью Python и модуля pty.

---



