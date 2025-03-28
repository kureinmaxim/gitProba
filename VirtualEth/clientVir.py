import socket


def send_data(target_ip, target_port, comm_protocol='TCP'):
    # Создаем сокет в зависимости от выбранного протокола
    if comm_protocol == 'TCP':
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((target_ip, target_port))
    elif comm_protocol == 'UDP':
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        print("Неизвестный протокол. Используйте TCP или UDP.")
        return

    data = bytearray([0x01, 0x02, 0x03])  # Пример данных для отправки
    print(f"Отправка данных: {data.hex()}")

    if comm_protocol == 'TCP':
        client_socket.send(data)
        response = client_socket.recv(1024)
        print(f"Получен ответ: {response.hex()}")
        client_socket.close()
    elif comm_protocol == 'UDP':
        client_socket.sendto(data, (target_ip, target_port))
        response, addr = client_socket.recvfrom(1024)
        print(f"Получен ответ от {addr}: {response.hex()}")
        client_socket.close()


if __name__ == "__main__":
    target_ip = "127.0.0.1"  # Локальный IP
    target_port = 12345  # Порт
    comm_protocol = "TCP"  # Или 'UDP'

    send_data(target_ip, target_port, comm_protocol)
