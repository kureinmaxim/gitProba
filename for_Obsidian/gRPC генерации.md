[[gRPC]]
#grpc

Для генерации gRPC файлов из вашего обновленного протофайла device_control.proto можно использовать следующие команды в зависимости от языка программирования:

Если папка shared еще не существует, сначала создайте ее:
```bash
mkdir -p shared
```

Далее
```bash
cd C:\Project\ProjectPython\UDP_gRPC_COM_Project 
 .\.venv312Win\Scripts\Activate.ps1    
```
### Python
```bash
python -m grpc_tools.protoc -I. --python_out=./shared --grpc_python_out=./shared device_control.proto
```
Это создаст два файла:

- device_control_pb2.py - содержит классы сообщений
- device_control_pb2_grpc.py - содержит классы gRPC клиента и сервера

### C++ (для STM32)
```bash
protoc --cpp_out=./shared --grpc_out=./shared --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` device_control.proto
```

### C#
```bash
protoc --csharp_out=./shared --grpc_out=./shared --plugin=protoc-gen-grpc=`which grpc_csharp_plugin` device_control.proto
```