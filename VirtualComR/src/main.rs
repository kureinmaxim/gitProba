use serialport::{
    available_ports, SerialPortType, DataBits, Parity, StopBits
};
use std::io::{Read, Write, ErrorKind};
use std::error::Error;
use std::process;
use std::time::Duration;

// Default settings struct
#[derive(Clone, Copy)]
struct PortSettings {
    baudrate: u32,
    bytesize: DataBits,
    parity: Parity,
    stopbits: StopBits,
}

impl Default for PortSettings {
    fn default() -> Self {
        PortSettings {
            baudrate: 38400,
            bytesize: DataBits::Eight,
            parity: Parity::None,
            stopbits: StopBits::One,
        }
    }
}

fn list_available_ports() -> Vec<String> {
    match available_ports() {
        Ok(ports) => {
            if ports.is_empty() {
                println!("❌ Нет доступных последовательных портов!");
                Vec::new()
            } else {
                println!("\n🔌 Доступные порты:");
                ports.iter().enumerate().for_each(|(i, port)| {
                    match &port.port_type {
                        SerialPortType::UsbPort(info) => {
                            println!("  {}. {} ({})",
                                     i + 1,
                                     port.port_name,
                                     info.product.clone().unwrap_or_default()
                            );
                        },
                        _ => {
                            println!("  {}. {}", i + 1, port.port_name);
                        }
                    }
                });
                ports.iter().map(|port| port.port_name.clone()).collect()
            }
        }
        Err(_) => {
            println!("❌ Не удалось получить список портов!");
            Vec::new()
        }
    }
}

fn select_port() -> Option<String> {
    let ports = list_available_ports();
    if ports.is_empty() {
        return None;
    }

    loop {
        print!("\nВведите номер порта: ");
        std::io::stdout().flush().unwrap();

        let mut input = String::new();
        std::io::stdin().read_line(&mut input).unwrap();

        match input.trim().parse::<usize>() {
            Ok(selected_index) if selected_index > 0 && selected_index <= ports.len() => {
                return Some(ports[selected_index - 1].clone());
            }
            _ => println!("⚠️ Ошибка: введите корректный номер порта!"),
        }
    }
}

fn choose_option<T: Clone + Eq>(
    prompt: &str,
    options: &[T],
    display_names: &[&str]
) -> T {
    println!("\n{}", prompt);
    display_names.iter().enumerate().for_each(|(i, &name)| {
        println!("  {}. {}", i + 1, name);
    });

    loop {
        print!("Выберите номер: ");
        std::io::stdout().flush().unwrap();

        let mut input = String::new();
        std::io::stdin().read_line(&mut input).unwrap();

        match input.trim().parse::<usize>() {
            Ok(selected_index) if selected_index > 0 && selected_index <= options.len() => {
                return options[selected_index - 1].clone();
            }
            _ => println!("⚠️ Ошибка: выберите корректный номер!"),
        }
    }
}

fn choose_configuration_mode() -> PortSettings {
    println!("\n=== ⚙  Настройка последовательного порта ===");
    println!("1. Использовать настройки по умолчанию");
    println!("   (38400 бод, 8 бит, без паритета, 1 стоп-бит)");
    println!("2. Ручная настройка параметров");

    loop {
        print!("Выберите режим настройки (1/2): ");
        std::io::stdout().flush().unwrap();

        let mut input = String::new();
        std::io::stdin().read_line(&mut input).unwrap();

        match input.trim() {
            "1" => return PortSettings::default(),
            "2" => break,
            _ => println!("⚠️ Некорректный выбор. Пожалуйста, введите 1 или 2."),
        }
    }

    let baudrates = [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200];
    let baudrate_names: Vec<String> = baudrates.iter().map(|x| x.to_string()).collect();
    let baudrate = choose_option(
        "Выберите скорость передачи (бод):",
        &baudrates,
        &baudrate_names.iter().map(|x| x.as_str()).collect::<Vec<&str>>()
    );

    let bytesizes = [
        DataBits::Five,
        DataBits::Six,
        DataBits::Seven,
        DataBits::Eight,
    ];
    let bytesize_names = ["5 бит", "6 бит", "7 бит", "8 бит (стандарт)"];
    let bytesize = choose_option(
        "Выберите размер байта:",
        &bytesizes,
        &bytesize_names
    );

    let parity_options = [
        Parity::None,
        Parity::Even,
        Parity::Odd,
    ];
    let parity_names = [
        "Нет",
        "Четный (Even)",
        "Нечетный (Odd)",
    ];
    let parity = choose_option(
        "Выберите паритет:",
        &parity_options,
        &parity_names
    );

    let stopbits = choose_option(
        "Выберите количество стоп-битов:",
        &[StopBits::One, StopBits::Two],
        &["1 стоп-бит", "2 стоп-бита"]
    );

    PortSettings {
        baudrate,
        bytesize,
        parity,
        stopbits,
    }
}

fn process_request(request: &[u8]) -> Option<Vec<u8>> {
    println!("Получен запрос: {}",
             request.iter().map(|b| format!("{:02X}", b)).collect::<String>()
    );

    match request {
        [0x01, 0x02, 0x03] => Some(vec![0x01, 0x0C]),
        [0x41] => Some(vec![0x20, 0x00]),
        [0xAA, 0xBB, 0xCC] => Some(vec![0xDD, 0xEE]),
        [0x01, x, ..] => Some(vec![0x01, x + 10]),
        _ => None
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    ctrlc::set_handler(move || {
        println!("\n🚪 Завершение работы");
        process::exit(0);
    })?;

    let port_name = match select_port() {
        Some(name) => name,
        None => {
            println!("❌ Выход: последовательный порт не выбран!");
            process::exit(0);
        }
    };

    let settings = choose_configuration_mode();

    let mut port = serialport::new(&port_name, settings.baudrate)
        .data_bits(settings.bytesize)
        .parity(settings.parity)
        .stop_bits(settings.stopbits)
        .timeout(Duration::from_secs(1))
        .open()?;

    println!(
        "\n✅ Соединение установлено: Порт 📌: {} @ {} бод @ {:?} @ {:?} @ {:?}",
        port_name, settings.baudrate, settings.bytesize, settings.parity, settings.stopbits
    );
    println!("\n🔄 Эмулятор готов к работе. 📍 Используйте Ctrl+C для остановки.");

    let mut buffer = [0; 1024];
    loop {
        match port.read(&mut buffer) {
            Ok(0) => {
                // No data received, sleep briefly to prevent busy waiting
                std::thread::sleep(Duration::from_millis(10));
            }
            Ok(bytes_read) => {
                let request = &buffer[..bytes_read];
                if let Some(response) = process_request(request) {
                    if let Err(e) = port.write(&response) {
                        eprintln!("Ошибка при отправке: {}", e);
                    } else {
                        println!(
                            "📤 Отправлен ответ: {}",
                            response.iter().map(|b| format!("{:02X}", b)).collect::<String>()
                        );
                    }
                }
            }
            Err(ref e) if e.kind() == ErrorKind::TimedOut => {
                // Timeout is expected, just continue
                std::thread::sleep(Duration::from_millis(10));
            }
            Err(e) => {
                eprintln!("Ошибка чтения порта: {}", e);
                return Err(Box::new(e));
            }
        }
    }
}