#freertos 
[[FreeRTOS]]

Вот основные варианты использования log_printf в STM32:

- **Отладочные сообщения:**
```c
log_printf("Debug: Entering function X\r\n");
log_printf("Debug: Variable value = %d\r\n", some_variable);
```

- **Информация о состоянии системы:**
```c
log_printf("System status: CPU freq = %d MHz\r\n", SystemCoreClock/1000000);
log_printf("Memory usage: %d bytes free\r\n", xPortGetFreeHeapSize());
```
   
- **Временные метки и измерения:**
```c
log_printf("Time elapsed: %lu ms\r\n", HAL_GetTick());
log_printf("Operation completed in %lu ms\r\n", end_time - start_time);
```
   
- **Сообщения об ошибках:**
```c
log_printf("Error: SPI initialization failed, code: %d\r\n", error_code);
log_printf("Warning: Battery low (%d%%)\r\n", battery_level);
```
    
- **Информация о периферии:**
```c
log_printf("UART configured: %d baud\r\n", huart1.Init.BaudRate);
log_printf("GPIO Pin %d state: %d\r\n", pin_number, pin_state);
```
 
- **Данные датчиков:**
```c
log_printf("Temperature: %.2f C\r\n", temperature);
log_printf("Sensor readings: X=%d, Y=%d, Z=%d\r\n", x, y, z);
```

- **Состояние задач RTOS:**
```c
log_printf("Task %s created, priority: %d\r\n", task_name, task_priority);
log_printf("Queue usage: %d/%d\r\n", uxQueueMessagesWaiting(queue), queue_length);
```

==Важные замечания:==

- Всегда добавляйте "\r\n" в конце строки для правильного переноса
- Используйте правильные спецификаторы формата (%d, %lu, %f и т.д.)
- Помните, что частое использование log_printf может замедлить работу системы
- В релизной версии рекомендуется отключать отладочный вывод

==Вот основные спецификаторы формата для log_printf:==
### Целые числа:
```c
%d // десятичное целое со знаком
%u // десятичное целое без знака
%x // шестнадцатеричное число (строчные буквы)
%X // шестнадцатеричное число (заглавные буквы)
%o // восьмеричное число
```
### ### Длинные целые:
```c
%ld // длинное целое со знаком (long)
%lu // длинное целое без знака (unsigned long)
%lx // длинное шестнадцатеричное (long hex)
```
### Числа с плавающей точкой:
```c
%f // число с плавающей точкой
%e // научная нотация (1.23e+4)
%g // автоматический выбор между %f и %e
%.2f // число с плавающей точкой с 2 знаками после запятой
```
### Символы и строки:
```c
%c // одиночный символ
%s // строка
```
### Указатели:
```c
%p // адрес памяти (указатель)
```

### Примеры использования:
```c
uint32_t time = HAL_GetTick();
int temperature = 25;
float voltage = 3.3f;
char* message = "Hello";

log_printf("Time: %lu ms\r\n", time);
log_printf("Temp: %d°C\r\n", temperature);
log_printf("Voltage: %.1f V\r\n", voltage);
log_printf("Message: %s\r\n", message);
log_printf("Memory address: %p\r\n", (void*)message);
log_printf("Hex value: 0x%08X\r\n", some_register);
```
### Модификаторы ширины и выравнивания:
```c
%5d // минимум 5 символов, выравнивание вправо
%-5d // минимум 5 символов, выравнивание влево
%05d // дополнение нулями слева до 5 символов
%*d // ширина задается аргументом
```
### Пример с модификаторами:
```c
int value = 42;

log_printf("[%5d]\r\n", value); // [ 42]
log_printf("[%-5d]\r\n", value); // [42 ]
log_printf("[%05d]\r\n", value); // [00042]
log_printf("[%*d]\r\n", 5, value); // [ 42]
```
