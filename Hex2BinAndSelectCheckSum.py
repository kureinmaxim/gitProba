import intelhex
import os

def calculate_checksum(data, start_address):
    checksum = 0
    for i in range(start_address, len(data), 2):
        word = (data[i] << 8) + data[i + 1]
        checksum += word
    return checksum & 0xFFFF

def adjust_checksum(data, target_checksum, start_address, program_end):
    # Calculate the current checksum
    current_checksum = calculate_checksum(data, start_address)
    #print(f"Current checksum: {current_checksum:04X}")

    # Consider existing byte values after program_end
    current_value = (data[program_end] << 8) + data[program_end + 1]
    current_checksum -= current_value
    current_checksum &= 0xFFFF

    diff = (target_checksum - current_checksum) & 0xFFFF

    # Adjust the two bytes immediately after the program end
    high_byte = (diff >> 8) & 0xFF
    low_byte = diff & 0xFF

    # Modify the two bytes after the program end in the binary data
    data[program_end] = high_byte
    data[program_end + 1] = low_byte

    print(f"Adjusted bytes to achieve target checksum: {high_byte:02X} {low_byte:02X}")

def main():
    input_hex_file = "C:/Project/ProjectCodeMaster/PriborTL7/PriborTL7/Debug/Exe/PriborTL7.HEX"
    if not os.path.exists(input_hex_file):
        print(f"Файл найден Project_CodeMaster: {input_hex_file}")
        input_hex_file = "C:/Project/Project_CodeMaster/PriborTL7/PriborTL7/Debug/Exe/PriborTL7.HEX"
        output_bin_file = "C:/Project/Project_CodeMaster/PriborTL7/PriborTL7/Debug/Exe/PriborTL7.bin"
        output_bin_file_cs = "C:/Project/Project_CodeMaster/PriborTL7/PriborTL7/Debug/Exe/PriborTL7_cs.bin"
        output_bin_file_cs_real = "C:/Project/Project_CodeMaster/PriborTL7/PriborTL7/Debug/Exe/PriborTL7_csReal.bin"
    else:
        print(f"Файл найден ProjectCodeMaster: {input_hex_file}")
        output_bin_file = "C:/Project/ProjectCodeMaster/PriborTL7/PriborTL7/Debug/Exe/PriborTL7.bin"
        output_bin_file_cs = "C:/Project/ProjectCodeMaster/PriborTL7/PriborTL7/Debug/Exe/PriborTL7_cs.bin"
        output_bin_file_cs_real = "C:/Project/ProjectCodeMaster/PriborTL7/PriborTL7/Debug/Exe/PriborTL7_csReal.bin"

    start_address = 0x2000
    bin_size = 32768
    bin_size2cs = 32766

    # Load the hex file
    hex_data = intelhex.IntelHex(input_hex_file)

    # Determine the end of the program
    program_end = max(hex_data.segments(), key=lambda seg: seg[1])[1]
    if program_end % 2 == 1:
      program_end = (program_end + 1) & 0xFFFF
    print(f"Program end address: {program_end:04X}")

    # Convert the hex file to binary
    bin_data = hex_data.tobinarray(start=0, size=bin_size)
    bin_data_cs = hex_data.tobinarray(start=0, size=bin_size2cs)
    bin_data_cs_real = bin_data_cs[:]

    # Write the binary data to the first file without checksum
    with open(output_bin_file, 'wb') as f:
        f.write(bin_data)

    # Запрашиваем у пользователя контрольную сумму
    while True:
        try:
            user_input = input("Введите желаемую контрольную сумму (в формате 0xFFFF): ")
            target_checksum = int(user_input, 16)
            if 0 <= target_checksum <= 0xFFFF:
                break
            else:
                print("Ошибка: контрольная сумма должна быть в пределах от 0x0000 до 0xFFFF.")
        except ValueError:
            print("Ошибка: введён неправильный формат. Пожалуйста, введите число в шестнадцатеричном формате.")

    # Calculate the checksum
    checksum = calculate_checksum(bin_data_cs, start_address)
    checksum_bytes = checksum.to_bytes(2, byteorder='big')
    print(f"Контрольная сумма исходного файла: {checksum:04X}")
    with open(output_bin_file_cs_real, 'wb') as f:
        f.write(bin_data_cs_real)
        f.write(checksum_bytes)

    # Adjust the bytes immediately after the program end to achieve the target checksum
    adjust_checksum(bin_data_cs_real, target_checksum, start_address, program_end)

    final_checksum = calculate_checksum(bin_data_cs_real, start_address)
    final_checksum_bytes = final_checksum.to_bytes(2, 'big')

    # Write the modified binary data to the second file with checksum
    with open(output_bin_file_cs, 'wb') as f:
        f.write(bin_data_cs_real)
        f.write(final_checksum_bytes)

    print(f"Контрольная сумма файла PriborTL7_cs.bin: {final_checksum:04X}")

    if final_checksum == target_checksum:
        print("Контрольная сумма успешно достигнута.")
    else:
        print("Ошибка: контрольная сумма не совпадает!")

if __name__ == "__main__":
    main()
