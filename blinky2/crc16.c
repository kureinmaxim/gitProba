#include "crc16.h"
#include "DataFile.h"
#include <stdbool.h>

/*********************************************************************
* Функция расчета CRC16 (полином 0xA001)
*********************************************************************/
uint16_t crc16(const uint8_t *data, uint16_t length) {
    uint16_t crc = 0xFFFF;

    for (uint16_t i = 0; i < length; i++) {
        crc ^= data[i];
        for (uint8_t j = 0; j < 8; j++) {
            if (crc & 1)
                crc = (crc >> 1) ^ polynomial;
            else
                crc >>= 1;
        }
    }

    return crc;
}


int process_crc(uint8_t *data, uint16_t length, bool checkFlag) {
    uint16_t crc = crc16(data, length);

    if (checkFlag) {
        // Return 1 if CRC is 0, otherwise 0
        return (crc == 0) ? 1 : 0;
    } 
    else {
        // Append CRC to data (LSB first, then MSB)
        data[length] = crc & 0xFF;         // Least significant byte
        data[length + 1] = (crc >> 8) & 0xFF;  // Most significant byte

        return length + 2;  // Return new length of data
    }
}