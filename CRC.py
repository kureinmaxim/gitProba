def calculate_crc16(data, poly, init_value=0xFFFF):
    crc = init_value
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1
    return crc

def format_crc16(crc):
    return f"{crc & 0xFF:02X}{(crc >> 8) & 0xFF:02X}"

def crc16_with_input(poly, init_value=0xFFFF):
    data_input = input("Введите байтовые данные через пробел и/или запятую (в формате 0xXX): ")
    try:
        data = [int(byte, 16) for byte in data_input.replace(',', ' ').split()]
    except ValueError:
        print("Ошибка: введите данные в правильном формате (например, 0xD5 0x02 0x04).")
        return

    crc = calculate_crc16(data, poly, init_value)
    crc_low_first = format_crc16(crc)
    print(f"CRC16 (low byte first): {crc_low_first}")

# Run the function
if __name__ == "__main__":
    crc16_with_input(0xA001)