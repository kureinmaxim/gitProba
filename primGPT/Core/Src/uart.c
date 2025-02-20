#include "uart.h"
#include "DataFile.h"
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"


extern QueueHandle_t uartQueue;  //  Declare(Объявляем) a variable created in main.c
extern volatile uint32_t last_rx_time;

volatile char uart1_rx_buf[UART_BUF_SIZE];    // Receive buffer
volatile uint8_t uart1_rx_head = 0;           // Головной указатель
volatile uint8_t uart1_rx_tail = 0;           // Хвостовой указатель

void log_printf(const char *format, ...) {
    char buffer[40];
    va_list args;
    va_start(args, format);
    vsnprintf(buffer, sizeof(buffer), format, args);
    va_end(args);
    HAL_UART_Transmit(&huart6, (uint8_t *)buffer, strlen(buffer), 100);
}

int _write(int file, char *ptr, int len) {
    for (int i = 0; i < len; i++) {
        HAL_UART_Transmit(&huart1, (uint8_t *)&ptr[i], 1, HAL_MAX_DELAY);
    }
    return len;
}

/*********************************************************************
 * Send and receive one character to the UART and othet
 *********************************************************************/
 void uart1_put_ch(char ch) {
	  HAL_UART_Transmit(&huart1, (uint8_t *)&ch, 1, HAL_MAX_DELAY);
	 }

 /* static char uart1_get_ch(void) {
	 uint8_t ch;
// Принимаем один байт UART1, блокируя выполнение программы до получения данных
	 if (HAL_UART_Receive(&huart1, &ch, 1, HAL_MAX_DELAY) == HAL_OK) {
	     return (char)ch;
	 }
	     return -1;  // В случае ошибки, возвращаем -1
} */

 void uart1_put_u16(uint16_t data) {
     uint8_t buffer[2];
     buffer[0] = (data >> 8) & 0xFF;  // Старший байт
     buffer[1] = data & 0xFF;         // Младший байт
     HAL_UART_Transmit(&huart1, buffer, 2, HAL_MAX_DELAY);
 }

 void uart1_put_u32(uint32_t data) {
     uint8_t buffer[4];
     buffer[0] = (data >> 24) & 0xFF;
     buffer[1] = (data >> 16) & 0xFF;
     buffer[2] = (data >> 8) & 0xFF;
     buffer[3] = data & 0xFF;
     HAL_UART_Transmit(&huart1, buffer, 4, HAL_MAX_DELAY);
 }

 /*********************************************************************
 * Receive one command to the UART
 *********************************************************************/
 int uart_read(char *ch)
 {
     if (uart1_rx_tail == uart1_rx_head) {
    	 //printf("READ: Buffer empty. Tail: %d, Head: %d\n", uart1_rx_tail, uart1_rx_head);
         return 0;                         // Buffer is empty
     }
     //then the FreeRTOS function that disables interrupts
     taskENTER_CRITICAL();                // Blocking access to buffer
     *ch = uart1_rx_buf[uart1_rx_tail];
     uart1_rx_tail = (uart1_rx_tail + 1) % UART_BUF_SIZE;
     taskEXIT_CRITICAL();                 // Unlock

     return 1;
 }

/*********************************************************************/
char usart_recv_byte(UART_HandleTypeDef *huart) {
    uint8_t ch;
    HAL_UART_Receive(huart, &ch, 1, HAL_MAX_DELAY);
    return (char)ch;
}

 /*********************************************************************
 * Receive for processing commands to the UART by interrupt
 *********************************************************************/
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
      if (huart->Instance == USART1) {
        uint8_t ch = uart1_rx_buf[uart1_rx_head];
        uint8_t next_head = (uart1_rx_head + 1) % UART_BUF_SIZE;

        if (next_head != uart1_rx_tail) {
        	//uart1_rx_buf[uart1_rx_head] = ch;
            uart1_rx_head = next_head;
        }
        else {
            //printf("BUFFER OVERFLOW! HEAD: %d, TAIL: %d\n", uart1_rx_head, uart1_rx_tail);
       	    uart1_rx_head = 0;
       	    uart1_rx_tail = 0;
        }

        // Отправляем байт в очередь FreeRTOS
        BaseType_t xHigherPriorityTaskWoken = pdFALSE;
        //xQueueSendFromISR(uartQueue, &ch, &xHigherPriorityTaskWoken);
        xQueueSendFromISR(uartQueue, (const void *)&ch, &xHigherPriorityTaskWoken);

        // Update the time of the last received byte
        last_rx_time = xTaskGetTickCountFromISR();
        //uart1_put_ch(uart1_rx_head);

        // Перезапускаем приём
        HAL_UART_Receive_IT(&huart1, (uint8_t *)&uart1_rx_buf[uart1_rx_head], 1);
        //HAL_UART_Receive_IT(&huart1, (uint8_t *)&uart1_rx_buf[next_head], 1);

        // Переключение контекста, если нужно
        portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
    }
}


