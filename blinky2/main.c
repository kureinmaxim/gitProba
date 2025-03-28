/* Simple LED task demo, using timed delays:
 *
 * The LED on PC13 is toggled in task1.
 */

// !!! in FreeRTOSConfig.h add string
// #define INCLUDE_uxTaskGetStackHighWaterMark 1
// для контроля заполнения стека, если осталось
// менее 10 слов (8*10=80 байт), то часто мигает светодиод С13

#include "FreeRTOS.h"
#include "task.h"
#include "DataFile.h"
#include "uart.h"
#include "crc16.h"

#include <string.h>  // Для strcmp()
#include <stdbool.h>

#include <libopencm3/stm32/rcc.h>
#include <libopencm3/stm32/gpio.h>
#include <libopencm3/stm32/usart.h>
#include <libopencm3/stm32/f1/nvic.h>
#include <libopencm3/stm32/f1/usart.h>


volatile uint32_t last_rx_time = 0;       // Время последнего принятого байта


extern void vApplicationStackOverflowHook(xTaskHandle *pxTask, signed portCHAR *pcTaskName);

void vApplicationStackOverflowHook(xTaskHandle *pxTask __attribute((unused)),signed portCHAR *pcTaskName __attribute((unused)))
{
  for(;;);	// Loop forever here..
} 

/*********************************************************************
 * Send characters to the UART, slowly
 *********************************************************************/
static void task1(void *args __attribute__((unused))) {
	int c = 'C';

	for (;;) {
	    gpio_toggle(GPIOC,GPIO13);
	    vTaskDelay(pdMS_TO_TICKS(3000));
	    uart_putc(c);
	    // Get the remaining stack size and output it to UART
        /* UBaseType_t stackRemaining = uxTaskGetStackHighWaterMark(NULL);
        char buffer[50];
        int len = snprintf(buffer, sizeof(buffer), "Stack remaining: %lu\n", stackRemaining);
        for (int i = 0; i < len; i++) {
            uart_putc(buffer[i]);
          } */
	 }
}

/*********************************************************************
 * toggle PortC -> GPIO15
 * The function `task2` toggles the state of GPIO pin 15 every 20 milliseconds.
 * 
 * @param args In the provided code snippet, the `args` parameter is a void pointer that is not being
 * used in the `task2` function. It is declared with the `__attribute((unused))` attribute, which is a
 * compiler directive indicating that the variable is intentionally not used in the function. This
 *********************************************************************/
static void task2(void *args __attribute((unused))) {
    for (;;)
     {
     //uart_putc('T');  // Check if task2 is running
	   gpio_toggle(GPIOC,GPIO15);
	   vTaskDelay(pdMS_TO_TICKS(20));
    }
}

/*********************************************************************
 * receive control commands 
 *********************************************************************/
static void uart_task(void *args __attribute__((unused))) {
    uint8_t command[UART_BUF_SIZE];
    uint16_t index = 0;
    uint16_t crc = 0;

    for (;;) {
        char ch;
        if (uart_read(&ch)) {
            last_rx_time = xTaskGetTickCount();  // Обновляем время последнего байта

            if (index < UART_BUF_SIZE) {
                command[index++] = ch;  // Записываем байт в буфер
            }
        }

        // Проверяем таймаут
        if (index > 0 && (xTaskGetTickCount() - last_rx_time) > pdMS_TO_TICKS(UART_TIMEOUT_MS)) {
            // Данные приняты, вычисляем CRC16
            crc = process_crc(command, index, true);
            // Выводим CRC в UART
            uart_putc(crc);
            
            // Обработка команды (пример: включение светодиода по первой команде)
            if (crc == 1 && command[0] == 1 && command[1] == 1) {
                gpio_clear(GPIOC, GPIO13);                
            } else if (crc == 1 && command[0] == 0 && command[1] == 0) {
                gpio_set(GPIOC, GPIO13);
            }
            
            index = 0;  // Сбрасываем буфер
        }

        vTaskDelay(pdMS_TO_TICKS(10));  // Периодическая проверка
    }
}

/* static void uart_echo_task(void *args __attribute__((unused))) {
    char ch;
    for (;;) {     
      while (!(USART_SR(USART1) & USART_SR_RXNE));

      ch = uart_getc();
      uart_putc(ch);
    }
} */

int main(void) {

  rcc_clock_setup_pll(&rcc_hse_configs[RCC_CLOCK_HSE8_72MHZ]);
  rcc_periph_clock_enable(RCC_GPIOC);
  gpio_set_mode(GPIOC,GPIO_MODE_OUTPUT_2_MHZ,GPIO_CNF_OUTPUT_PUSHPULL,GPIO13|GPIO15);

  uart_setup();

  xTaskCreate(task1,"task1_UART_LED",100,NULL,configMAX_PRIORITIES-1,NULL);
  xTaskCreate(task2,"task2_IMP",50,NULL,configMAX_PRIORITIES-1,NULL);
  //xTaskCreate(uart_echo_task, "uart_echo_task", 100, NULL, configMAX_PRIORITIES-1, NULL);
  xTaskCreate(uart_task, "uart_task", 150, NULL, configMAX_PRIORITIES-1, NULL);

  vTaskStartScheduler();

  for (;;);
  return 0;
}

// End
