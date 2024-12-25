#terminal
[[Python]]   [[GIT]]

 ==В WSL (Windows Subsystem for Linux) для перехода в папку на диске `C:\Project\Project_Python` нужно выполнить следующие действия:==

1. **Откройте WSL терминал.**    
2. **Перейдите на диск `C` в файловой системе WSL.** В WSL Windows-диски монтируются в папке `/mnt`. Чтобы перейти на диск `C`, выполните команду:
```bash
cd /mnt/c
```
3. **Перейдите в нужную папку.** После перехода на диск `C` просто укажите путь до нужной директории:
```bash
cd Project/Project_Python
```
Если путь к папке содержит пробелы, оберните его в кавычки или экранируйте пробелы с помощью обратного слэша (`\`):
```bash
cd "Project/Project Python"
```
or
```bash
cd Project/Project\ Python
```


==Если вы используете **Windows Shell** (например, командную строку `cmd` или `PowerShell`), то переход в папку `C:\Project\Project_Python` делается немного по-другому:==
### В **Command Prompt (cmd)**:

1. Откройте `cmd`.
2. Выполните команду для перехода на диск `C`:    
```bash
C:
```
3. Перейдите в нужную папку:
```bash
cd \Project\Project_Python
```

### В **PowerShell**:

1. Откройте PowerShell.
2. Перейдите на диск `C` (если вы не находитесь на нём):
```bash
Set-Location C:\
```
или просто:
```bash
cd C:\
```
3. Перейдите в нужную папку:
 ```bash
 cd Project\Project_Python
```
