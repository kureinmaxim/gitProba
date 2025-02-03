# Define constants for default parameters
DEFAULT_POLY = 0xA001
DEFAULT_INIT_VALUE = 0xFFFF


def get_input_data():
    """
    Prompts user to input byte data and parses it into a list of integers.
    :return: List of integers representing byte data.
    :rtype: list[int]
    """
    user_input = input("Enter byte data separated by spaces (format: 0xXX): ").strip()
    if not user_input:
        raise ValueError("Error: Input cannot be empty.")
    try:
        return [int(byte, 16) for byte in user_input.split()]
    except ValueError:
        raise ValueError("Error: Please provide data in correct format (e.g., 0xD5 0x02 0x04).")


def crc16_with_input(poly=DEFAULT_POLY, init_value=DEFAULT_INIT_VALUE):
    """
    Calculates the CRC16 checksum for a given input of byte data using a specified polynomial
    and starting value.
    :param poly: The polynomial used for the CRC16 calculation.
    :type poly: int
    :param init_value: The initial value for the CRC calculation. Defaults to 0xFFFF.
    :type init_value: int
    :return: None. Outputs the CRC16 checksum as a low-byte-first string.
    :rtype: None
    """
    try:
        byte_data = get_input_data()
    except ValueError as e:
        print(e)
        return

    # Initialize the CRC value
    crc = init_value
    for byte in byte_data:
        crc ^= byte  # XOR with the byte
        for _ in range(8):  # Process each of the 8 bits
            if crc & 0x0001:  # If the least significant bit is set
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1

    # Format the result as low byte first
    crc_low_first = f"{crc & 0xFF:02X}{(crc >> 8) & 0xFF:02X}"
    print(f"CRC16 (low byte first): {crc_low_first}")


# Run the function
crc16_with_input()
