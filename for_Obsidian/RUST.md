#rust

## Загрузка и установка Rust

1. Установите Rust с помощью [официального установщика Rust](https://rustup.rs/).

- Откройте PowerShell и выполните:
```powershell
Invoke-WebRequest -Uri https://sh.rustup.rs -OutFile rustup-init.exe .\rustup-init.exe
```
- После завершения перезапустите PowerShell, чтобы обновить переменные окружения.

2. Проверьте установку Rust:

```powershell
rustc --version 
cargo --version
```

## Сборка и запуск

### Вариант 1: Разработка
```bash
# Собрать и запустить в режиме разработки
cargo run
```
### Вариант 2: Релизная сборка
```bash
# Собрать оптимизированную версию
cargo build --release
# Запустить созданный исполняемый файл
./target/release/serial_emulator  # на Linux/macOS

.\target\release\serial_emulator.exe  # на Windows
```
### Вариант 3: Установка в систему

```bash
# Установить приложение в систему
cargo install --path .

# Запустить (если ~/.cargo/bin в PATH)
serial_emulator
```

## Сборка для различных платформ

### Для Windows (из Linux или macOS)
```bash
# Сначала добавьте целевую платформу
rustup target add x86_64-pc-windows-gnu

# Затем соберите
cargo build --release --target x86_64-pc-windows-gnu
```

### Для Linux (из Windows)
```bash
# Добавьте целевую платформу Linux
rustup target add x86_64-unknown-linux-gnu

# Соберите проект
cargo build --release --target x86_64-unknown-linux-gnu
```

==Проблемы при сборке:==
- cargo clean - для очистки кэша проекта
- cargo update - для обновления зависимостей 

# Добавление зависимостей в Cargo.toml

Вот как должен выглядеть ваш файл Cargo.toml со всеми необходимыми зависимостями для проекта:
```rust
[package]
name = "serial_emulator"
version = "0.1.0"
edition = "2021"
authors = ["Your Name <your.email@example.com>"]
description = "Эмулятор последовательного порта с поддержкой русских символов и интерактивным меню"

[dependencies]
serialport = "4.2.0"
ctrlc = "3.2.0"
encoding_rs = "0.8.32"
encoding = "0.2.33"
chardet = "0.2.4"
crossterm = "0.27.0"

[profile.release]
opt-level = 3
lto = true
codegen-units = 1
panic = 'abort'
strip = true
```

Этот файл включает:
**1. Все необходимые зависимости:**
- serialport для работы с COM-портами
- ctrlc для обработки Ctrl+C
- encoding_rs и encoding для поддержки различных кодировок, включая кириллицу
- chardet для автоматического определения кодировок
- crossterm для создания интерактивного меню

**2. Оптимизации для релизной сборки. После обновления Cargo.toml запустите:**
```bash
cargo update
```
 Затем можно собрать проект командой:
```bash
cargo build --release
# Или запустить его
cargo run --release
```

Флаг --release включит все оптимизации, указанные в файле, что сделает  приложение более быстрым и эффективным.