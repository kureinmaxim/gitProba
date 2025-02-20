#ifndef UART_H
#define UART_H

#include <stdint.h>
#include "stm32f4xx_hal.h"
#include <stdio.h>
#include <stdarg.h>   // Для работы с va_list, va_start, va_end
#include <string.h>   // Для strlen

extern UART_HandleTypeDef huart1, huart6;

void log_printf(const char *format, ...);
void uart1_put_ch(char ch);
void uart1_put_u16(uint16_t data);
void uart1_put_u32(uint32_t data);
int  uart_read(char *ch);
char usart_recv_byte(UART_HandleTypeDef *huart);
//static char uart1_get_ch(void);
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart);

#endif // UART_H
