import socket
import sys


def start_server(server_ip, server_port, protocol_type='TCP'):
    # Создаем сокет в зависимости от выбранного протокола
    if protocol_type == 'TCP':
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((server_ip, server_port))
        server_socket.listen(5)
        print(f"TCP сервер слушает на {server_ip}:{server_port}")
    elif protocol_type == 'UDP':
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"UDP сервер слушает на {server_ip}:{server_port}")
    else:
        print("Неизвестный протокол. Используйте TCP или UDP.")
        sys.exit(1)

    # Принятие соединений или ожидание пакетов в зависимости от протокола
    if protocol_type == 'TCP':
        conn, addr = server_socket.accept()
        print(f"Подключение от {addr}")
        handle_tcp_connection(conn)
    elif protocol_type == 'UDP':
        while True:
            data, addr = server_socket.recvfrom(1024)  # Максимум 1024 байта
            print(f"Получено сообщение от {addr}: {data.hex()}")
            response = process_data(data)
            server_socket.sendto(response, addr)


def handle_tcp_connection(conn):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"Получено сообщение: {data.hex()}")
        response = process_data(data)
        print(f"Отправка ответа: {response.hex()}")
        conn.send(response)
    conn.close()


def process_data(data):
    # Обработка данных, аналогично предыдущему примеру
    if data == bytearray([0x01, 0x02, 0x03]):
        return bytearray([0x01, 0x0C])
    return bytearray([0xFF])  # Ответ на неизвестный запрос


if __name__ == "__main__":
    server_ip = "0.0.0.0"  # Слушаем на всех интерфейсах
    server_port = 12345  # Пример порта
    protocol_type = "TCP"  # Или 'UDP'

    start_server(server_ip, server_port, protocol_type)
