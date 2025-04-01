use serialport::{
    available_ports, SerialPortType, DataBits, Parity, StopBits
};
use std::io::{Read, Write, ErrorKind};
use std::error::Error;
use std::process;
use std::time::Duration;
use encoding_rs;
use chardet::detect;
use encoding_rs::Encoding as EncodingRs;
use crossterm::{
    event::{self, Event, KeyCode, KeyEvent, KeyModifiers},
    terminal::{self, ClearType},
    cursor::MoveTo,
    ExecutableCommand,
};

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

fn bytes_to_hex_string(bytes: &[u8]) -> String {
    bytes.iter()
        .map(|b| format!("{:02X}", b))
        .collect::<Vec<_>>()
        .join(" ")
}

fn bytes_to_text(bytes: &[u8]) -> String {
    // Если данных мало, используем только ASCII
    if bytes.len() < 4 {
        return bytes.iter()
            .map(|&b| {
                if b >= 32 && b <= 126 {
                    char::from(b).to_string()
                } else {
                    format!(".")
                }
            })
            .collect::<String>();
    }
    
    // Пытаемся определить кодировку автоматически
    let mut result = String::new();
    
    // ASCII декодирование (базовое всегда показываем)
    let ascii_text = bytes.iter()
        .map(|&b| {
            if b >= 32 && b <= 126 {
                char::from(b).to_string()
            } else {
                ".".to_string()
            }
        })
        .collect::<String>();
    
    result.push_str(&format!("ASCII: \"{}\"", ascii_text));
    
    // Автоопределение кодировки
    let detected = detect(bytes);
    // детект возвращает (charset: String, confidence: f32, language: String)
    let (charset, confidence, _) = detected;
    
    if confidence > 0.5 {
        result.push_str(&format!(" | Автоопределение: {}% - {}: ", 
                               (confidence * 100.0) as u8, 
                               charset));
        
        // Пытаемся декодировать с обнаруженной кодировкой
        if let Some(encoding) = EncodingRs::for_label(charset.as_bytes()) {
            let (text, _, _) = encoding.decode(bytes);
            result.push_str(&format!("\"{}\"", text.to_string()));
        } else {
            result.push_str("(не удалось декодировать)");
        }
    } else {
        result.push_str(" | Дополнительно: ");
        
        // Добавим UTF-8 и Windows-1251 как наиболее распространенные для русского
        let (utf8_text, _, _) = encoding_rs::UTF_8.decode(bytes);
        result.push_str(&format!("UTF-8: \"{}\" | ", utf8_text.to_string()));
        
        let (win1251_text, _, _) = encoding_rs::WINDOWS_1251.decode(bytes);
        result.push_str(&format!("Windows-1251: \"{}\"", win1251_text.to_string()));
    }
    
    result
}

fn print_data_info(prefix: &str, data: &[u8]) {
    let hex_string = bytes_to_hex_string(data);
    let text = bytes_to_text(data);
    
    println!("{}:", prefix);
    println!("  📍 HEX: {}", hex_string);
    
    // Изменяем вывод текста - убираем \n перед содержимым
    println!("  📝 Текст: {}", text.replace("\n", "\n          "));
    println!("  📊 Размер: {} байт", data.len());
}

fn process_request(request: &[u8]) -> Option<Vec<u8>> {
    print_data_info("📥 Получен запрос", request);

    let response = match request {
        [0x01, 0x02, 0x03] => Some(vec![0x01, 0x0C]),
        [0x41] => Some(vec![0x20, 0x00]),
        [0xAA, 0xBB, 0xCC] => Some(vec![0xDD, 0xEE]),
        [0x01, x, ..] => Some(vec![0x01, x + 10]),
        _ => None
    };
    
    if let Some(resp) = &response {
        print_data_info("📤 Отправлен ответ", resp);
    } else {
        println!("⚠️ Ответ не отправлен - нет подходящего шаблона");
        println!("❗ Меню - ESC, Выход - Ctrl+C");
    }
    
    response
}

// Обновляем функцию clear_screen для работы с crossterm
fn clear_screen() -> Result<(), Box<dyn Error>> {
    std::io::stdout().execute(terminal::Clear(ClearType::All))?;
    std::io::stdout().execute(MoveTo(0, 0))?;
    Ok(())
}

// Функция show_menu остаётся прежней
fn show_menu() {
    println!("\n=== Меню ===");
    println!("1. Очистить экран");
    println!("2. Выход");
    print!("Выберите действие: ");
    std::io::stdout().flush().unwrap();
}

fn main() -> Result<(), Box<dyn Error>> {
    // НЕ включаем raw_mode в начале
    
    ctrlc::set_handler(move || {
        let _ = terminal::disable_raw_mode();
        println!("\n🚪 Завершение работы");
        process::exit(0);
    })?;

    // Основной цикл выбора порта - продолжаем, пока не получим успешное соединение или выход
    let mut port = None;
    let mut port_name = String::new();
    let mut settings = PortSettings::default();
    
    while port.is_none() {
        // Выбор порта
        port_name = match select_port() {
            Some(name) => name,
            None => {
                println!("❌ Выход: последовательный порт не выбран!");
                process::exit(0);
            }
        };

        // Выбор настроек
        settings = choose_configuration_mode();

        // Пытаемся открыть порт
        match serialport::new(&port_name, settings.baudrate)
            .data_bits(settings.bytesize)
            .parity(settings.parity)
            .stop_bits(settings.stopbits)
            .timeout(Duration::from_secs(1))
            .open() {
                Ok(opened_port) => {
                    port = Some(opened_port);
                    println!(
                        "\n✅ Соединение установлено: Порт 📌: {} @ {} бод @ {:?} @ {:?} @ {:?}",
                        port_name, settings.baudrate, settings.bytesize, settings.parity, settings.stopbits
                    );
                },
                Err(e) => {
                    println!("❌ Ошибка при открытии порта {}: {}", port_name, e);
                    println!("Возможно, порт уже используется другим приложением.");
                    
                    // Спрашиваем пользователя, что делать дальше
                    loop {
                        print!("Выберите действие (1 - попробовать другой порт, 2 - выйти): ");
                        std::io::stdout().flush().unwrap();
                        
                        let mut input = String::new();
                        std::io::stdin().read_line(&mut input).unwrap();
                        
                        match input.trim() {
                            "1" => break, // Вернуться к выбору порта
                            "2" => {
                                println!("🚪 Завершение работы");
                                process::exit(0);
                            },
                            _ => println!("⚠️ Некорректный выбор, пожалуйста введите 1 или 2")
                        }
                    }
                }
            }
    }
    
    // После успешного открытия порта
    let mut port = port.unwrap(); // Безопасно, так как мы выходим из цикла только когда порт не None
    
    println!("\n🔄 Эмулятор готов к работе. Используйте клавиши для управления:");
    println!("   ESC - показать меню, Ctrl+C - выход");
    
    // Теперь включаем raw mode для обработки клавиш когда порт уже открыт
    terminal::enable_raw_mode()?;

    let mut buffer = [0; 1024];
    let mut show_menu_flag = false;

    loop {
        // Проверяем события клавиатуры без блокировки
        if event::poll(Duration::from_millis(1))? {
            if let Event::Key(KeyEvent { code, modifiers, .. }) = event::read()? {
                match code {
                    // ESC для показа меню
                    KeyCode::Esc => {
                        show_menu_flag = true;
                    }
                    // Ctrl+C для выхода
                    KeyCode::Char('c') if modifiers.contains(KeyModifiers::CONTROL) => {
                        terminal::disable_raw_mode()?;
                        println!("\n🚪 Завершение работы");
                        process::exit(0);
                    }
                    _ => {}
                }
            }
        }

        // Обработка меню, если запрошено
        if show_menu_flag {
            terminal::disable_raw_mode()?;
            
            show_menu();
            
            let mut input = String::new();
            std::io::stdin().read_line(&mut input).unwrap();
            
            match input.trim() {
                "1" => {
                    clear_screen()?;
                    
                    println!("Экран очищен.");
                    println!(
                        "\n✅ Соединение установлено: Порт 📌: {} @ {} бод @ {:?} @ {:?} @ {:?}",
                        port_name, settings.baudrate, settings.bytesize, settings.parity, settings.stopbits
                    );
                    println!("\n🔄 Эмулятор готов к работе. Используйте клавиши для управления:");
                    println!("   ESC - показать меню, Ctrl+C - выход");
                },
                "2" => {
                    println!("\n🚪 Завершение работы");
                    process::exit(0);
                },
                _ => {
                    println!("Продолжение работы...");
                }
            }
            
            terminal::enable_raw_mode()?;
            show_menu_flag = false;
        }

        // Обычная работа с портом
        match port.read(&mut buffer) {
            Ok(0) => {
                // No data received, sleep briefly to prevent busy waiting
                std::thread::sleep(Duration::from_millis(10));
            }
            Ok(bytes_read) => {
                // Временно отключаем raw mode для вывода
                terminal::disable_raw_mode()?;
                
                let request = &buffer[..bytes_read];
                if let Some(response) = process_request(request) {
                    if let Err(e) = port.write(&response) {
                        eprintln!("❌ Ошибка при отправке: {}", e);
                    }
                }
                
                // Возвращаем raw mode
                terminal::enable_raw_mode()?;
            }
            Err(ref e) if e.kind() == ErrorKind::TimedOut => {
                // Timeout is expected, just continue
                std::thread::sleep(Duration::from_millis(10));
            }
            Err(e) => {
                // Отключаем raw mode перед выводом ошибки и выходом
                terminal::disable_raw_mode()?;
                eprintln!("❌ Ошибка чтения порта: {}", e);
                
                // Спрашиваем пользователя, что делать дальше при ошибке чтения
                println!("Возможно, порт был отключен или закрыт другим приложением.");
                
                loop {
                    print!("Выберите действие (1 - выбрать другой порт, 2 - выйти): ");
                    std::io::stdout().flush().unwrap();
                    
                    let mut input = String::new();
                    std::io::stdin().read_line(&mut input).unwrap();
                    
                    match input.trim() {
                        "1" => {
                            // Возвращаемся к выбору порта
                            return Ok(());  // Перезапускаем программу
                        },
                        "2" => {
                            println!("🚪 Завершение работы");
                            process::exit(0);
                        },
                        _ => println!("⚠️ Некорректный выбор, пожалуйста введите 1 или 2")
                    }
                }
            }
        }
    }
}