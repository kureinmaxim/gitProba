#comport 

## Пример запуску скрипта vicom.py Python сразу в окне PowerShell
==Создайте ярлык==
- Щелкните правой кнопкой мыши на рабочем столе или в папке, где хотите создать ярлык.
- Выберите "Создать" -> "Ярлык".

1.  Если вы не используете виртуальное окружение для vicom.py, используйте путь, который вы нашли с помощью команды: 
```powershell
where python 
#(обычно первый в списке) или
Get-Command python
 ```
тогда в свойствах ярлыка указать такую команду
```txt
"C:\Program Files\PowerShell\7\pwsh.exe" -Command "& 'C:\Users\z6364\AppData\Local\Programs\Python\Python313\python.exe' 'C:\Project\ProjectPython\VirtualCom\vicom.py'"
```

2. Если вы активировали виртуальное окружение для вашего проекта (C:\Project\ProjectPython\VirtualCom), то Python будет находиться внутри папки этого окружения, обычно по пути. Что гарантирует, что скрипт будет запущен с правильными зависимостями, установленными в этом окружении.
```txt
C:\Project\ProjectPython\VirtualCom\Scripts\python.exe
```
тогда в свойствах ярлыка указать такую команду
```txt
"C:\Program Files\PowerShell\7\pwsh.exe" -Command "& 'C:\Project\ProjectPython\VirtualCom\.venv\Scripts\python.exe' 'C:\Project\ProjectPython\VirtualCom\vicom.py'"
```
для теста если сразу закрывается с ошибкой 
```txt
"C:\Program Files\PowerShell\7\pwsh.exe" -NoExit -Command "& 'C:\Project\ProjectPython\VirtualCom\Scripts\python.exe' 'C:\Project\ProjectPython\VirtualCom\vicom.py'"
OR
"C:\Program Files\PowerShell\7\pwsh.exe" -NoExit -Command "& 'C:\Project\ProjectPython\VirtualCom\.venv\Scripts\python.exe' 'C:\Project\ProjectPython\VirtualCom\vicom.py'"
```


3. Самый удобный способ добиться похожего поведения — ==создать ярлык==:
 Найдите ваш virtualcompy2r.exe. Если это Rust-проект, он, скорее всего, находится в папке target\debug\ или target\release\ внутри вашего проекта (например, C:\Project\Project_Rust\VirtualComPro\target\release\virtualcompy2r.exe). Уточните точный путь.

 Создайте ярлык:
- Кликните правой кнопкой мыши на рабочем столе или в папке, где хотите разместить ярлык.
- Выберите "Создать" -> "Ярлык".
- В поле "Укажите расположение объекта" введите команду, которая запускает Windows Terminal (wt.exe) и передает ему команду для запуска вашего файла. Замените ПУТЬ_К_ВАШЕМУ_EXE на реальный полный путь к virtualcompy2r.exe:
```bash
wt.exe "ПУТЬ_К_ВАШЕМУ_EXE"
# пример
wt.exe "C:\Project\Project_Rust\VirtualComPro\target\release\virtualcompy2r.exe"
# еще пример
C:\Distribs\Terminal\terminalwt.exe "C:\Project\Rust\virtualcompy2r.exe"
```
   
- Нажмите "Далее".
- Введите имя для ярлыка, например, "Запустить VirtualComPort".
- Нажмите "Готово".

Теперь двойной клик по этому ярлыку будет открывать Windows Terminal и запускать в нем ваше приложение virtualcompy2r.exe.