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
