import intelhex

def calculate_checksum(data, start_address):
    checksum = 0
    for i in range(start_address, len(data), 2):
       # word = (data[i + 1] << 8) + data[i]
        word = (data[i] << 8) + data[i + 1]
        checksum = (checksum + word) & 0xFFFF
    return checksum

def main():
    input_hex_file = "C:/Project/Project_CodeMaster/PriborTL7/PriborTL7/Debug/Exe/PriborTL7.HEX"
    output_bin_file = "C:/Project/Project_CodeMaster/PriborTL7/PriborTL7/Debug/Exe/PriborTL7.bin"
    output_bin_file_cs = "C:/Project/Project_CodeMaster/PriborTL7/PriborTL7/Debug/Exe/PriborTL7_cs.bin"
    start_address = 0x2000
    bin_size = 32768
    bin_size2cs = 32766

    # Load the hex file
    hex_data = intelhex.IntelHex(input_hex_file)

    # Convert the hex file to binary
    bin_data = hex_data.tobinarray(start=0, size=bin_size)
    bin_data_cs = hex_data.tobinarray(start=0, size=bin_size2cs)

    # Write the binary data to the first file without checksum
    with open(output_bin_file, 'wb') as f:
        f.write(bin_data)

    # Calculate the checksum
    checksum = calculate_checksum(bin_data_cs, start_address)
    #checksum_bytes = checksum.to_bytes(2, byteorder='little')
    checksum_bytes = checksum.to_bytes(2, byteorder='big')
    print("Checksum bytes (hex):", ' '.join(f'{b:02x}' for b in checksum_bytes))

    # Write the binary data to the second file with checksum
    with open(output_bin_file_cs, 'wb') as f:
        f.write(bin_data_cs)
        f.write(checksum_bytes)

if __name__ == "__main__":
    main()