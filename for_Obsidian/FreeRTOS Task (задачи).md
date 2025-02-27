#freertos #task
[[FreeRTOS]]

В FreeRTOS задача может находиться в одном из следующих состояний: **выполнения**, **готовности**, **ожидания** и нескольких других.
### 1. **Состояние выполнения (Running)**

- Задача непосредственно выполняется процессором.
- В любой момент времени процессор может выполнять только одну задачу (в случае однопроцессорной системы).
- Задача с наивысшим приоритетом среди готовых задач получает это состояние.

**Пример:**  
Если только одна задача имеет самый высокий приоритет и нет вызовов `vTaskDelay()`, `vTaskSuspend()` или блокировок, эта задача будет непрерывно выполняться.

---
### 2. **Состояние готовности (Ready)**

- Задача готова к выполнению, но не выполняется, потому что процессор занят задачей с более высоким или таким же приоритетом.
- Как только планировщик освобождает процессор, задача может перейти в состояние выполнения.

**Пример:**  
Если у задачи с приоритетом 2 есть вызов `vTaskDelay(100)` и освободилась другая задача с приоритетом 3, задача с приоритетом 2 становится готовой, но ждет своей очереди.

---
### 3. **Состояние ожидания (Blocked)**

- Задача временно ожидает какого-то события или завершения таймера.
- После завершения события задача переходит в состояние готовности.

**Причины перехода задачи в ожидание:**

- Вызов `vTaskDelay(pdMS_TO_TICKS(n))`: задача ожидает завершения задержки.
- Ожидание завершения передачи через очередь или получение семафора (`xQueueReceive`, `xSemaphoreTake`).

**Пример:**
`vTaskDelay(pdMS_TO_TICKS(500));`
Задача блокируется на 500 миллисекунд и освобождает процессор для выполнения других задач.

---
### 4. **Состояние приостановки (Suspended)**

- Задача не участвует в планировании и не может быть запущена, пока явно не будет возобновлена вызовом `vTaskResume()`.

**Пример:**

`vTaskSuspend(myTaskHandle);  // Приостановка задачи vTaskResume(myTaskHandle);   // Возобновление`

---
### 5. **Состояние завершения (Deleted/Terminated)**

- Задача была удалена вызовом `vTaskDelete()`.
- Её ресурсы могут быть освобождены вручную или автоматически.

---
### Переходы между состояниями

|Текущее состояние|Действие|Новое состояние|
|---|---|---|
|Running|Более высокая готовая задача|Ready|
|Ready|Планировщик запускает задачу|Running|
|Running|`vTaskDelay()` или ожидание события|Blocked|
|Blocked|Событие произошло или таймер истек|Ready|
|Ready/Blocked|`vTaskSuspend()`|Suspended|
|Suspended|`vTaskResume()`|Ready|

Таким образом, механизм состояний и переключений между ними позволяет FreeRTOS эффективно распределять процессорное время между задачами.