#venv  #comport 
[[Python]]


# VirtualCom

Эмулятор COM-порта с интерактивным интерфейсом для тестирования и разработки ПО, работающего с последовательными портами.

## Описание

VirtualCom позволяет:
- Подключаться к реальным COM-портам (физическим или виртуальным).
- Настраивать параметры соединения (скорость, биты данных, четность, стоп-биты).
- Отправлять данные в текстовом или HEX-формате.
- Автоматически добавлять CRC16 (Modbus) к отправляемым HEX-данным.
- Принимать данные и отображать их в различных форматах (HEX, ASCII, оба) с временными метками.
- Приостанавливать и возобновлять прием данных.
- Предотвращать запуск второй копии программы с тем же портом с помощью lock-файлов.

Интерфейс использует `prompt_toolkit` для интерактивности и мгновенного отклика на нажатия клавиш (без необходимости нажимать Enter для выбора опций меню или конфигурации).

## Возможности

-   Автоматическое обнаружение и **сортировка** доступных COM-портов.
-   Ручная настройка параметров соединения или использование **настроек по умолчанию** (38400 бод, 8 бит, без паритета, 1 стоп-бит).
-   **Мгновенный выбор** порта и параметров конфигурации (нажатием цифры).
-   Отправка **текстовых** сообщений (UTF-8).
-   Отправка **HEX-данных**.
-   Отправка HEX-данных с автоматическим расчетом и добавлением **CRC16 (Modbus)**.
-   Настраиваемый режим отображения принимаемых данных:
    -   Только HEX (`HH:MM:SS Порт 📥 HEX: ...`)
    -   Только ASCII (`HH:MM:SS Порт 📥 ASCII: ...`)
    -   Оба формата (`HH:MM:SS Порт 📥 HEX: ...`, `HH:MM:SS Порт 📥 ASCII: ...`)
-   Отображение **временных меток** (`HH:MM:SS`) для всех принятых и отправленных (через лог) сообщений и ошибок.
-   **Приостановка** (`🛑`) и **возобновление** (`▶️`) приема данных (с **очисткой буфера** при возобновлении).
-   **Очистка экрана** (`🧹`).
-   Интерактивное меню с управлением цифрами (`1`-`7`).
-   Выход из режимов отправки по `Esc`.
-   Завершение работы программы по `Ctrl+C`.
-   Отображение **статуса** приема данных, информации о **текущем порте** и его параметрах, и подсказки о выходе под меню.
-   Использование **автоматически рассчитанного таймаута между байтами (`inter_byte_timeout`)** для улучшения считывания полных сообщений.
-   **Блокировка порта:** Предотвращение запуска второй копии программы с тем же портом с помощью **lock-файлов** (с автоматическим удалением зависших файлов при старте).

## Требования

-   Python 3.8+ (из-за использования `:=` в некоторых местах, хотя можно адаптировать и для более ранних)
-   Библиотека `pyserial`: `pip install pyserial`
-   Библиотека `prompt_toolkit`: `pip install prompt_toolkit`
-   Операционная система: macOS, Linux, Windows (основной функционал кросс-платформенный).

## Установка

1.  **Клонируйте репозиторий или скачайте файлы.**
2.  **Создайте и активируйте виртуальное окружение (рекомендуется):**
    ```bash
    python -m venv .venv 
    # macOS / Linux
    source .venv/bin/activate 
    # Windows (Command Prompt)
    # .venv\Scripts\activate.bat
    # Windows (PowerShell)
    # .venv\Scripts\Activate.ps1 
    ```
3.  **Установите зависимости:**
    ```bash
    pip install pyserial prompt_toolkit
    ```

## Использование

1.  **Запустите программу из терминала:**
    (Убедитесь, что ваше виртуальное окружение активировано)
    ```bash
    python vicom.py
    ```
2.  **Выберите COM-порт** из списка, введя его номер.
3.  **Выберите режим настройки:**
    -   `1`: Ручная настройка (выбирайте параметры нажатием цифр).
    -   `2`: Использовать настройки по умолчанию.
4.  **Взаимодействуйте с основным меню:**
    -   `1`: Режим отправки текстовых сообщений.
    -   `2`: Режим отправки HEX данных.
    -   `3`: Режим отправки HEX данных с CRC16.
    -   `4`: `🛑` Остановить прием данных.
    -   `5`: `▶️` Продолжить прием данных (очищает буфер).
    -   `6`: `👁️` Сменить режим отображения (Оба -> HEX -> ASCII -> Оба).
    -   `7`: `🧹` Очистить экран.
    -   `Esc`: Выход из режимов отправки обратно в меню.
    -   `Ctrl+C`: Завершение работы программы.

## Быстрый запуск

### macOS

1.  **Создайте AppleScript:**
    -   Откройте приложение "Редактор скриптов" (Script Editor).
    -   Вставьте следующий код, **заменив пути** на ваши реальные пути к папке проекта и интерпретатору Python в виртуальном окружении:

    ```applescript
    on run
        -- ПОЛНЫЙ путь к папке, где лежит ваш скрипт vicom.py
        set scriptFolder to "/Users/olgazaharova/Project/Python/Python2Mac/VirtualCom/" -- <-- ЗАМЕНИТЕ НА ВАШ ПУТЬ
        -- Имя вашего скрипта
        set scriptName to "vicom.py"
        -- ПОЛНЫЙ путь к ИНТЕРПРЕТАТОРУ Python ВНУТРИ вашего виртуального окружения
        set pythonPath to "/Users/olgazaharova/Project/Python/Python2Mac/VirtualCom/.venv/bin/python3" -- <-- ЗАМЕНИТЕ НА ВАШ ПУТЬ K PYTHON В VENV
        -- Команда для запуска вашего скрипта
        set theCommand to "cd " & quoted form of scriptFolder & " && " & quoted form of pythonPath & " " & quoted form of scriptName

        tell application "Terminal"
            activate
            -- 1. Создаем новое окно/вкладку
            set targetTab to do script ""
            delay 0.7 

            try
                set targetWindow to window 1
                
                -- 2. Изменяем размер окна (опционально, можно закомментировать)
                set currentBounds to bounds of targetWindow
                set x1 to item 1 of currentBounds
                set y1 to item 2 of currentBounds
                set x2 to item 3 of currentBounds
                set y2 to item 4 of currentBounds
                set currentWidth to x2 - x1
                set currentHeight to y2 - y1
                set newWidth to round (currentWidth * 1.25) rounding as taught in school -- Шире на 25%
                set newHeight to round (currentHeight * 0.60) rounding as taught in school -- Ниже на 40%
                set newX2 to x1 + newWidth
                set newY2 to y1 + newHeight
                set bounds of targetWindow to {x1, y1, newX2, newY2}
                delay 0.2 

                -- 3. Изменяем размер шрифта (опционально, можно закомментировать)
                tell application "System Events"
                    tell process "Terminal"
                        set frontmost of targetWindow to true
                        delay 0.1
                        keystroke "-" using command down -- Уменьшить шрифт (повторить сколько нужно)
                        delay 0.1
                        keystroke "-" using command down
                        delay 0.1
                        keystroke "-" using command down
                    end tell
                end tell
                delay 0.2

                -- 4. Запускаем команду Python в уже настроенном окне
                do script theCommand in targetTab 

            on error errMsg number errNum
                display dialog "Ошибка при настройке окна/запуске скрипта: " & errMsg & " (" & errNum & ")"
            end try
            
        end tell
    end run
    ```
    -   Сохраните скрипт (`Файл -> Сохранить`) как **Программу** (Application) на Рабочий стол или в другое удобное место (например, `VirtualCom Launcher.app`).
2.  **Запустите сохраненную программу**, дважды кликнув по ней.

### Windows

**1.  Создать ярлык для выполнения программы на python через powershell**
Создать ярлык на Рабочем столе для  vicom.py открыть свойства и изменить:
Объект ярлыка
```txt
"C:\Program Files\PowerShell\7\pwsh.exe" -Command "& 'C:\Project\ProjectPython\Python2Mac\VirtualCom\.venv\Scripts\python.exe' 'C:\Project\ProjectPython\Python2Mac\VirtualCom\vicom.py'"
```
Рабочая папка
```txt
"C:\Program Files\PowerShell\7"
```
Убедится что:
- Файл `vicom.py` существует.    
- Виртуальное окружение было успешно создано в `.venv`.    
- Стоит `PowerShell 7` (а не Windows PowerShell), раз ты указываешь `C:\Program Files\PowerShell\7\pwsh.exe`.

Создать виртуальное окружение в папке C:\Project\ProjectPython\Python2Mac\VirtualCom
```powershell
cd 'C:\Project\ProjectPython\Python2Mac\VirtualCom'
python -m venv .venv
. .venv\Scripts\Activate.ps1
# Если будет ошибка — можно временно изменить политику
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Установить нужные пакеты:
```powershell
pip install prompt_toolkit pyserial
```

==ИЛИ ЛУЧШЕ создать файл `requirements.txt`==

Узнать список установленных пакетов:
```bash
pip freeze
```
 Открой папку    C:\Project\ProjectPython\Python2Mac\VirtualCom
Создай там файл `requirements.txt`

```ini
prompt_toolkit==3.0.50
pyserial==3.5
wcwidth==0.2.13
```

==Теперь чтобы установить все зависимости на другом компьютере:==
```powershell
pip install -r requirements.txt
```

2.  **Создать пакетный файл (.bat):**

   -   Откройте Блокнот.
   -   Вставьте следующий код, **заменив пути** на ваши реальные пути к папке проекта и скрипту активации виртуального окружения:

```bash
@echo off
REM Путь к Python из виртуального окружения
set VENV_PYTHON=C:\Project\GitPython\Python2Mac\VirtualCom\.venv\Scripts\python.exe

REM Путь к скрипту vicom.py
set SCRIPT_PATH=C:\Project\GitPython\Python2Mac\VirtualCom\vicom.py

REM Проверка существования python.exe
if not exist "%VENV_PYTHON%" (
    echo Виртуальное окружение не найдено по пути: %VENV_PYTHON%
    pause
    exit /b 1
)

REM Запуск скрипта через PowerShell 7
"C:\Program Files\PowerShell\7\pwsh.exe" -Command "& '%VENV_PYTHON%' '%SCRIPT_PATH%'"
pause
```

ИЛИ такой 

```bash
@echo off
 :: Установите ПРАВИЛЬНЫЙ путь к папке вашего проекта
  set SCRIPT_DIR="C:\путь\к\вашей\папке\VirtualCom" 
  :: Установите ПРАВИЛЬНЫЙ путь к скрипту активации venv
  set VENV_ACTIVATE=%SCRIPT_DIR%\.venv\Scripts\activate.bat

    :: Переходим в папку проекта
    cd /D %SCRIPT_DIR%
    if errorlevel 1 (
        echo Ошибка: Не удалось перейти в папку %SCRIPT_DIR%
        pause
        exit /b 1
    )

    :: Активируем виртуальное окружение
    call %VENV_ACTIVATE%
    if errorlevel 1 (
        echo Ошибка: Не удалось активировать виртуальное окружение %VENV_ACTIVATE%
        pause
        exit /b 1
    )

    :: Запускаем скрипт Python
    echo Запуск VirtualCom...
    python vicom.py

    :: Деактивация (опционально, окно закроется само)
    :: call .venv\Scripts\deactivate.bat
    
    echo.
    echo VirtualCom завершил работу.
    pause :: Оставляем окно открытым, чтобы увидеть вывод
```

-   Сохраните файл (`Файл -> Сохранить как...`) с именем `run_vicom.bat` (убедитесь, что тип файла "Все файлы", а не ".txt") в папку вашего проекта (`VirtualCom`).
3.  **Создайте ярлык на Рабочем столе:**
    -   Щелкните правой кнопкой мыши на файле `run_vicom.bat` в папке проекта.
    -   Выберите "Отправить" -> "Рабочий стол (создать ярлык)".
    -   Перейдите на Рабочий стол, найдите новый ярлык (`run_vicom.bat - Ярлык`).
    -   Вы можете переименовать его (например, в "VirtualCom").
    -   (Опционально) Щелкните правой кнопкой мыши на ярлыке -> "Свойства" -> "Сменить значок..." и выберите подходящую иконку.
4.  **Запустите программу**, дважды кликнув по ярлыку на Рабочем столе. Откроется окно командной строки, активируется окружение и запустится `vicom.py`.

## Формат вывода данных

Входящие данные отображаются в двух строках:

```
{Имя порта} 📥 Получен запрос HEX: <байт1> <байт2> ...
{Имя порта} 📥 ASCII: <строковое представление>
Меню (Esc) или Выход (Ctrl+C): 
```

(Непечатаемые символы в ASCII заменяются символом-заполнителем).

## Параметры по умолчанию

-   Скорость: 38400 бод
-   Размер байта: 8 бит
-   Паритет: нет
-   Стоп-биты: 1

## Поддерживаемые запросы (Эмуляция)

Для целей тестирования, скрипт может имитировать ответы на некоторые запросы:

-   `01 02 03` -> ответ: `01 0C`
-   `41` -> ответ: `20 00`
-   `AA BB CC` -> ответ: `DD EE`
-   Запросы длиной 3 байта, начинающиеся с `01` -> ответ: первый байт запроса и второй байт + 10

## Завершение работы

Для завершения работы используйте комбинацию клавиш `Ctrl+C`. 