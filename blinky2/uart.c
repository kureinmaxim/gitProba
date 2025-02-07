#include "uart.h"
#include "DataFile.h"

#include <libopencm3/stm32/rcc.h>
#include <libopencm3/stm32/gpio.h>
#include <libopencm3/stm32/usart.h>
#include <libopencm3/stm32/f1/nvic.h>

// Буфер приёма UART
volatile char uart_rx_buf[UART_BUF_SIZE];    // Буфер приёма
volatile uint16_t uart_rx_head = 0;          // Головной указатель
volatile uint16_t uart_rx_tail = 0;          // Хвостовой указатель
    
/*********************************************************************
 * Setup the UART
 *********************************************************************/
void uart_setup(void) {
    rcc_periph_clock_enable(RCC_GPIOA);
    rcc_periph_clock_enable(RCC_USART1);

    // UART TX на PA9
    gpio_set_mode(GPIOA, GPIO_MODE_OUTPUT_50_MHZ, GPIO_CNF_OUTPUT_ALTFN_PUSHPULL, GPIO_USART1_TX);
    // UART RX на PA10
    gpio_set_mode(GPIOA, GPIO_MODE_INPUT, GPIO_CNF_INPUT_FLOAT, GPIO_USART1_RX);

    usart_set_baudrate(USART1, 38400);
    usart_set_databits(USART1, 8);
    usart_set_stopbits(USART1, USART_STOPBITS_1);
    usart_set_mode(USART1, USART_MODE_TX_RX);
    usart_set_parity(USART1, USART_PARITY_NONE);
    usart_set_flow_control(USART1, USART_FLOWCONTROL_NONE);
    usart_enable(USART1);

    nvic_enable_irq(NVIC_USART1_IRQ);
    usart_enable_rx_interrupt(USART1);
}

/*********************************************************************
 * Send and receive one character to the UART
 *********************************************************************/
void uart_putc(char ch) {
    usart_send_blocking(USART1, ch);
}
/* static char uart_getc(void) {
        return usart_recv_blocking(USART1);
} */

 /*********************************************************************
 * Receive one command to the UART
 *********************************************************************/
int uart_read(char *ch) {
    if (uart_rx_tail == uart_rx_head) {
        return 0;                         // Буфер пуст
    }
    *ch = uart_rx_buf[uart_rx_tail];
    uart_rx_tail = (uart_rx_tail + 1) % UART_BUF_SIZE;
    return 1;
}

 /*********************************************************************
 * Receive for processing commands to the UART by interrupt
 *********************************************************************/
void usart1_isr(void) {
    if (usart_get_flag(USART1, USART_SR_RXNE)) {
        char ch = usart_recv(USART1);

        uint16_t next_head = (uart_rx_head + 1) % UART_BUF_SIZE;
        if (next_head != uart_rx_tail) {        // Проверка на переполнение
            uart_rx_buf[uart_rx_head] = ch;
            uart_rx_head = next_head;           // Сдвигаем указатель
        }
    }
}

