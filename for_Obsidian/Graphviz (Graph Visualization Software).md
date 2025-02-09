#dot #diagram

Graphviz (Graph Visualization Software) — это инструмент для визуализации графов и диаграмм. Он позволяет создавать диаграммы на основе текстового описания с помощью языка DOT. Это особенно полезно для представления сетей, иерархий, деревьев и других сложных структур.

**Примеры использования:**

- Визуализация зависимостей в проектах.
- Построение деревьев принятия решений.
- Графы связей и схемы потоков данных.
#### **Установка Graphviz на Mac**

1. **Через Homebrew (рекомендуется)**  
Откройте терминал и выполните команду:
```bash
brew install graphviz   
```

2. **Через скачивание дистрибутива**

- Перейдите на официальный сайт Graphviz и выберите версию для macOS.
- Скачайте и установите пакет `.dmg`.
- Перетащите приложение в папку `/Applications`.

#### **Установка Graphviz на Windows 11**

1. **Через установочный файл:**
- Зайдите на официальный сайт Graphviz и выберите версию для Windows.
- Скачайте и установите `.exe` файл, следуя инструкциям мастера установки.

2. **Настройка системного пути:**
 - Откройте «Настройки системы» и выберите«Дополнительныпараметрысистемы».
 - Перейдите в «Переменные среды» и найдите переменную `Path`.
- Нажмите «Изменить» и добавьте путь к папке установки Graphviz (например, `C:\Program Files\Graphviz\bin`).
- Сохраните изменения.
---

#### **Проверка установки**

В командной строке или терминале выполните:
```bash
dot -V
```
Если Graphviz установлен правильно, вы увидите информацию о версии.

#### **Применение в Python**

Чтобы использовать Graphviz с Python, установите библиотеку `graphviz`:
```bash
pip install graphviz
```

Пример простого графа на языке Python:
```python
from graphviz import Digraph

dot = Digraph()
dot.node('A', 'Start')
dot.node('B', 'Decision')
dot.edge('A', 'B')
dot.render('output_graph', format='png', cleanup=True)
```

Этот код создаст граф и сохранит его в PNG-файле.

==**Еще пример для FreeRTOPS**==
```python
from graphviz import Digraph

# Функция для создания и генерации диаграммы использования очереди
def generate_queue_diagram():
    # Создаём направленный граф (диаграмму)
    diagram = Digraph("Queue Usage", format="png")  # Название диаграммы и формат выходного файла
    diagram.attr(rankdir="TB", size="10,8")  # Настройка направления и размера диаграммы (TB — сверху вниз)

    # Определяем узлы диаграммы с подписями
    diagram.node("Start", "Task Execution Start")  # Начало выполнения задачи
    diagram.node("xQueueCreate", "xQueueCreate()\nCreate Queue")  # Создание очереди
    diagram.node("SendData", "xQueueSend()\nSend Data")  # Отправка данных в очередь
    diagram.node("DataSent", "Data Placed in Queue")  # Данные успешно размещены в очереди
    diagram.node("QueueEmpty", "Queue Empty?")  # Проверка: очередь пуста?
    diagram.node("ReceiveData", "xQueueReceive()\nReceive Data")  # Получение данных из очереди
    diagram.node("DataReceived", "Data Successfully Received")  # Данные успешно получены
    diagram.node("Timeout", "Timeout Occurred?")  # Проверка: истекло ли время ожидания?
    diagram.node("HandleTimeout", "Handle Timeout\n(e.g., Error Handling)")  # Обработка таймаута (например, обработка ошибок)
    diagram.node("End", "Task Continues")  # Продолжение выполнения задачи

    # Определяем связи между узлами диаграммы
    diagram.edge("Start", "xQueueCreate")  # Переход от начала к созданию очереди
    diagram.edge("xQueueCreate", "SendData")  # Переход от создания очереди к отправке данных
    diagram.edge("SendData", "DataSent")  # Переход от отправки данных к размещению данных в очереди

    # Путь при получении данных из очереди
    diagram.edge("QueueEmpty", "Timeout", label="No")  # Если очередь не пуста — проверка таймаута
    diagram.edge("QueueEmpty", "ReceiveData", label="Yes")  # Если очередь пуста — получение данных
    diagram.edge("ReceiveData", "DataReceived", label="Success")  # Успешное получение данных
    diagram.edge("Timeout", "HandleTimeout", label="Timeout")  # Обработка таймаута

    # Финальные переходы
    diagram.edge("DataReceived", "End")  # Переход после успешного получения данных
    diagram.edge("HandleTimeout", "End")  # Переход после обработки таймаута

    # Зацикливание для непрерывного выполнения
    diagram.edge("End", "QueueEmpty")  # Возврат к проверке пустоты очереди

    return diagram

# Генерация диаграммы использования очереди
diagram = generate_queue_diagram()

# Сохранение и рендеринг изображения
path = "queue_usage_diagram"  # Базовое имя файла

diagram.render(path, format="png")  # Создание файла PNG

print(f"Диаграмма сохранена как {path}.png")
```