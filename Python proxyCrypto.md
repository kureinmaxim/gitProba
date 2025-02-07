[[Python]] [[Python serverCrypto]]
#proxy

ProxyCrypto/
│── proxyCrypto.py   # Код UDP-прокси
│── client.py  # Тестовый клиент
│── serverCrypto.py  # Тестовый VDS сервер

Для реализации шифрования данных между прокси и сервером, необходимо добавить простое шифрование с использованием библиотеки `cryptography`.

**1. Установить библиотеку для шифрования**:
```bash
# for Debian
pip3 install cryptography
# for Windows
pip install cryptography
# for MacOS
brew install python-cryptography
brew install cryptography
```

**2. На VDS сервере запустить сервер с ключом шифрования**
```bash
# for Linux
python3 serverCrypto.py --host 0.0.0.0 --port 8888 --key "ВашКлюч=="
python3 serverCrypto.py --host 0.0.0.0 --port 8888 --key 25HykVxCN5-MbwlHosCTQXxma7EANm9HJhzngUsV6A4=
```

**3. На машине с прокси-сервером запустить прокси с тем же ключом**
```bash
# for Mac
python3 proxyCrypto.py --listen-ip 0.0.0.0 --listen-port 9999 --target-ip 138.124.19.67 --target-port 8888 --key "ВашКлюч=="
# for Windows
python proxyCrypto.py --listen-ip 0.0.0.0 --listen-port 9999 --target-ip 138.124.19.67 --target-port 8888 --key "ВашКлюч=="
```
Где `0.0.0.0` означает, что сервер будет слушать на всех сетевых интерфейсах VDS.

**4. На локальной машине запустить `client.py` без изменений, он уже настроен для работы с прокси на 127.0.0.1:9999**

**5. Генерация ключа шифрования**
```bash
python3 proxyCrypto.py --generate-key --target-ip 127.0.0.1 --target-port 8888  # Mac
OR
python proxyCrypto.py --generate-key --target-ip 127.0.0.1 --target-port 8888  # Windows
```
Значения ==--target-ip 127.0.0.1 --target-port 8888== могут быть любыми, так как сейчас генерируется ключ. 
Нажать Ctrl+C, чтобы остановить текущий запущенный прокси, и использовать уже полученный ключ. Затем скопируйте сгенерированный ключ и используйте его на обоих серверах.

### Принцип работы:
1. Клиент отправляет данные на прокси (127.0.0.1:9999)
2. Прокси шифрует данные и пересылает их на VDS сервер
3. VDS сервер расшифровывает данные, обрабатывает их и отправляет зашифрованный ответ обратно на прокси
4. Прокси расшифровывает ответ и пересылает его клиенту

Эта конфигурация обеспечивает защищенную передачу данных между прокси и VDS сервером, даже если трафик будет перехвачен.