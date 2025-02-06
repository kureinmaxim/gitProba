#stm 
[[STM]]

1. Папка верхнего уровня:
    ==~/stm32f103c8t6==

2. Install ==Make== and ==Git== for Mac, Windows(only WSL2), Linux
```bash
brew install make
brew install git
```

3.  Клонирование репозитория
git clone https://github.com/Apress/beginning-STM2-second-edition

4.  Заменить при необходимости
 beginning-STM2-second-edition -> stm32f103c8t6

5.  Установить ==unzip==
```bash
apt install unzip
```

6. Загрузить ==libopencm3==
```bash
cd stm32f103c8t6 
git clone https://github.com/libopencm3/libopencm3.git 
```

7. Загрузить ядро ==FreeRTOS==
```bash
cd ~/stm32f103c8t6/rtos 
git clone --depth 1 https://github.com/FreeRTOS/FreeRTOS-Kernel.git

или для всех веток 
git clone https://github.com/FreeRTOS/FreeRTOS-Kernel.git 
или вместо последней 
git config --global http.postBuffer 524288000 
git clone --depth 1 https://github.com/FreeRTOS/FreeRTOS-Kernel.git
cd FreeRTOS-Kernel 
git fetch --unshallow
```

1. Установить ==кросс-компилятор ARM==
Например если Intel-Linux то скачать с [https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads](https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads)
```bash
sudo -i 
mkdir /opt 
cd /opt 
chmod 755 /opt 
cd /opt 
for Windows 
wget -O a.zip 'https://developer.arm.com/-/media/Files/downloads/gnu/14.2.rel1/binrel/arm-gnu-toolchain-14.2.rel1-mingw-w64-x86_64-arm-none-eabi.zip' 

for Linux wget -O a.xz 'https://developer.arm.com/-/media/Files/downloads/gnu/14.2.rel1/binrel/arm-gnu-toolchain-14.2.rel1-aarch64-arm-none-eabi.tar.xz'
```
**Если не скачивается ПО**
Попробуйте пинговать доменное имя:
```bash
ping developer.arm.com
```
Если это не работает, временно настройте другой DNS-сервер, например, Google DNS:  
Откройте файл настроек DNS:
```bash
nano /etc/resolv.conf
```
Добавьте строку:
```bash
nameserver 8.8.8.8
```

```bash
==для расширения .zip==
unzip a.zip
==для расширения .xz==
tar xJf a.xz
==для расширения .gz==
tar xzf a.gz
```
переименовать
```bash
mv arm-none-eabi gcc-arm
OR
mv arm-gnu-toolchain-14.2.rel1-aarch64-arm-none-eabi gcc-arm
```
выйти из root
```bash
exit
```

2. Настроить переменную ==$PATH==
```bash
export PATH="/opt/gcc-arm/bin:$PATH"
export PATH="/opt/bin:$PATH"
nano ~/.zshrc
Add the following line:
export PATH="/opt/bin:$PATH"
Save and exit the editor.
source ~/.zshrc

sudo chown $(whoami):$(whoami) /opt/bin/arm-none-eabi-gcc.exe
chmod +x /opt/bin/arm-none-eabi-gcc.exe
ls -l /opt/bin/arm-none-eabi-gcc.exe

arm-none-eabi-gcc.exe --version
```
Необходимость добавления `.exe` обусловлена особенностями WSL и совместимостью с файловой системой Windows. Настройка окружения (через PATH, ссылки или алиасы) позволит устранить неудобства.  
протестировать установленный компилятор
```bash
arm-none-eabi-gcc.exe --version
```

добавить для удобства алиас без `.exe`
```bash
nano ~/.zshrc
alias arm-none-eabi-gcc="arm-none-eabi-gcc.exe"
source ~/.zshrc
which arm-none-eabi-gcc
```
еще протестировать установленный компилятор
```bash
arm-none-eabi-gcc --version
```
еще ==протестировать== установленный компилятор
```bash
git clone https://github.com/libopencm3/libopencm3.git
cd libopencm3
make
```
Если библиотека `libwwg` вам не нужна для проекта, вы можете удалить или закомментировать строки, связанные с ней, в `Makefile`:
```make
nano ../Makefile.incl
# ..............-lwwg
make clean
make
```

11. Установить все для ==ST-Link==

```bash
apt install stlink-tools
apt install linux-tools-virtual hwdata
```