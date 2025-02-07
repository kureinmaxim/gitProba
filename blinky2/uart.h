#ifndef UART_H
#define UART_H

#include <stdint.h>


void uart_setup(void);
void uart_putc(char ch);
int  uart_read(char *ch);
void usart1_isr(void);  // Обработчик прерываний UART

#endif // UART_H
