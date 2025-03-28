#ifndef CRC16_H
#define CRC16_H

#include <stdint.h>
#include <stdbool.h>

uint16_t crc16(const uint8_t *data, uint16_t length);
int process_crc(uint8_t *data, uint16_t length, bool checkFlag);

#endif // CRC16_H