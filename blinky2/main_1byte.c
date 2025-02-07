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
//#include "usart.h"
#include <libopencm3/stm32/rcc.h>
#include <libopencm3/stm32/gpio.h>
#include <libopencm3/stm32/usart.h>
#include <libopencm3/stm32/f1/nvic.h>

extern void vApplicationStackOverflowHook(xTaskHandle *pxTask, signed portCHAR *pcTaskName);

void vApplicationStackOverflowHook(xTaskHandle *pxTask __attribute((unused)),signed portCHAR *pcTaskName __attribute((unused)))
{
  for(;;);	// Loop forever here..
}

 /*********************************************************************
 * Setup the UART
 *********************************************************************/
static void uart_setup(void) {

	rcc_periph_clock_enable(RCC_GPIOA);
	rcc_periph_clock_enable(RCC_USART1);

	// UART TX on PA9 (GPIO_USART1_TX)
	gpio_set_mode(GPIOA,GPIO_MODE_OUTPUT_50_MHZ,GPIO_CNF_OUTPUT_ALTFN_PUSHPULL,GPIO_USART1_TX);
  // UART RX on PA10 (GPIO_USART1_RX)
  gpio_set_mode(GPIOA, GPIO_MODE_INPUT, GPIO_CNF_INPUT_FLOAT, GPIO_USART1_RX);

	usart_set_baudrate(USART1,38400);
	usart_set_databits(USART1,8);
	usart_set_stopbits(USART1,USART_STOPBITS_1);
	usart_set_mode(USART1,USART_MODE_TX_RX);
	usart_set_parity(USART1,USART_PARITY_NONE);
	usart_set_flow_control(USART1,USART_FLOWCONTROL_NONE);
	usart_enable(USART1);

  nvic_enable_irq(NVIC_USART1_IRQ);
  usart_enable_rx_interrupt(USART1);
}

 /*********************************************************************
 * Send and receive one character to the UART by interrupt
 *********************************************************************/
void usart1_isr(void) {
    if (usart_get_flag(USART1, USART_SR_RXNE)) {
        char ch = usart_recv(USART1);  // Читаем байт из буфера
        usart_send(USART1, ch);        // Эхо-ответ
    }
}
 /*********************************************************************
 * Send and receive one character to the UART
 *********************************************************************/
static inline void uart_putc(char ch) {
	usart_send_blocking(USART1,ch);
}

/* static char uart_getc(void) {
        return usart_recv_blocking(USART1);
} */

/*********************************************************************
 * Send characters to the UART, slowly
 *********************************************************************/
static void
task1(void *args __attribute__((unused))) {
	int c = 'C';

	for (;;) {
	    gpio_toggle(GPIOC,GPIO13);
	    vTaskDelay(pdMS_TO_TICKS(1000));
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

static void
task2(void *args __attribute((unused))) {
    for (;;)
     {
       //uart_putc('T');  // Check if task2 is running
	   gpio_toggle(GPIOC,GPIO15);
	   vTaskDelay(pdMS_TO_TICKS(20));
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
  gpio_set_mode(GPIOC,GPIO_MODE_OUTPUT_2_MHZ,GPIO_CNF_OUTPUT_PUSHPULL,GPIO13);
  gpio_set_mode(GPIOC,GPIO_MODE_OUTPUT_2_MHZ,GPIO_CNF_OUTPUT_PUSHPULL,GPIO15);

  uart_setup();

  xTaskCreate(task1,"task1_UART_LED",100,NULL,configMAX_PRIORITIES-1,NULL);
  xTaskCreate(task2,"task2_IMP",50,NULL,configMAX_PRIORITIES-1,NULL);
  //xTaskCreate(uart_echo_task, "uart_echo_task", 100, NULL, configMAX_PRIORITIES-1, NULL);
  vTaskStartScheduler();

  for (;;);
  return 0;
}

// End
