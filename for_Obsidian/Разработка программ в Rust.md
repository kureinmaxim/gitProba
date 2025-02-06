#rust 

### 1. **Создать новый проект Rust**
  В PowerShell выполнить:
```powershell
cargo new hex_to_bin_checksum 
cd hex_to_bin_checksum  
```
###  2. **Скопировать код в проект**
  Перейти в папку проекта:
```powershell
cd hex_to_bin_checksum  
```
Открыть файл `src/main.rs` в текстовом редакторе (`Notepad` или Visual Studio Code):
```powershell
notepad src\main.rs 
```
Вставить свой код вместо содержимого файла.

### 3. **Добавьте зависимости (при необходимости)**

 Добавить необходимые зависимости в файл `Cargo.toml`:
```rust
[dependencies]  
#intelhex = "0.4.0" # Укажите последнюю версию библиотеки
#ihex = "3.0"  
hex = "0.4.3"
```
Затем выполнить:
```powershell
cargo build 
```

### 4. **Соберите программу**
Для компиляции программы выполнить:
```powershell
cargo build --release
```

### 5. **Запустить программу**
```powershell
.\target\release\hex_to_bin_checksum.exe 
```
Убедитесь, что входной файл HEX существует по указанному пути. Если требуется, измените пути в коде на доступные файлы.

### 6. **Отладка**
Если потребуется отладка, запускайте программу в режиме разработки:
```powershell
cargo run
```
