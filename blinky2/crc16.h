#ifndef CRC16_H
#define CRC16_H

#include <stdint.h>

// Функция расчёта CRC16 с полиномом 0xA001
uint16_t crc16(const uint8_t *data, uint16_t length);

#endif // CRC16_H