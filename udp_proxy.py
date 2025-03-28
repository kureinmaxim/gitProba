import socket
import binascii  # Для hex-представления байтов

PROXY_IP = "127.0.0.1"
PROXY_PORT = 9999

sock = None  # Создаём переменную заранее

try:
    print("Создание UDP-сокета...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    sock.bind((PROXY_IP, PROXY_PORT))
    print("UDP-прокси запущен! Ожидаем данные...\n")
    print("Нажмите Ctrl + C для остановки.")

    while True:
        try:
            data, addr = sock.recvfrom(4096)
            if not data:
                continue

            # Логирование полученных данных
            try:
                log_message = data.decode("utf-8")
                print("Получено текстовое сообщение от {}: {}".format(addr, log_message))
            except UnicodeDecodeError:
                hex_data = binascii.hexlify(data).decode("ascii")  # Совместимость с Python 3.4
                print("Получены бинарные данные от {}: {}".format(addr, hex_data))

            # Отправка эхо-ответа клиенту
            try:
                response = data
                sock.sendto(response, addr)
                print("Ответ клиенту отправлен (байты): {}\n".format(response))
            except Exception as e:
                print("Ошибка при отправке данных:", repr(e))

        except socket.timeout:
            continue

        except KeyboardInterrupt:
            print("\nОстановка прокси-сервера (Ctrl+C)")
            break

        except Exception as e:
            import traceback
            print("Неожиданная ошибка приема данных:", repr(e))
            traceback.print_exc()
            continue

finally:
    if sock:
        sock.close()
        print("Сокет закрыт.")
    input("Нажмите Enter для выхода...")
