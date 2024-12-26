#rust 

Файл Cargo.toml
```rust
[package]  
name = "hex_to_bin_checksum"  
version = "0.1.0"  
edition = "2021"  
  
[dependencies]
hex = "0.4.3"
```

```rust
use std::fs::File;
use std::io::{self, BufRead, Write};
use std::path::Path;

#[derive(Debug)]
struct HexRecord {
    address: u16,
    record_type: u8,
    data: Vec<u8>,
}

fn parse_hex_line(line: &str) -> Result<HexRecord, String> {
    if !line.starts_with(':') {
        return Err("Line does not start with ':'".to_string());
    }

    let bytes = hex::decode(&line[1..]).map_err(|_| "Failed to decode HEX line")?;

    if bytes.len() < 5 {
        return Err("Line too short".to_string());
    }

    let length = bytes[0] as usize;
    let address = ((bytes[1] as u16) << 8) | (bytes[2] as u16);
    let record_type = bytes[3];
    let data = bytes[4..4 + length].to_vec();
    let checksum = bytes[4 + length];

    // Verify checksum
    let sum: u8 = bytes.iter().take(4 + length).fold(0, |acc, &b| acc.wrapping_add(b));
    if sum.wrapping_add(checksum) != 0 {
        return Err("Invalid checksum".to_string());
    }

    Ok(HexRecord {
        address,
        record_type,
        data,
    })
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn calculate_checksum(data: &[u8], start_address: usize) -> u16 {
    let mut checksum = 0u16;
    for i in (start_address..data.len()).step_by(2) {
        let word = ((data[i] as u16) << 8) | (data[i + 1] as u16);
        checksum = checksum.wrapping_add(word);
    }
    checksum
}

fn load_hex_to_bin(file_path: &str, start: usize, size: usize) -> Vec<u8> {
    let mut bin_data = vec![0xFFu8; size];

    if let Ok(lines) = read_lines(file_path) {
        for line in lines {
            if let Ok(record_line) = line {
                if let Ok(record) = parse_hex_line(&record_line) {
                    if record.record_type == 0 {
                        let start_idx = (record.address as usize).saturating_sub(start);
                        let end_idx = start_idx + record.data.len();

                        if start_idx < size {
                            bin_data[start_idx..end_idx.min(size)].copy_from_slice(&record.data[..end_idx.min(size) - start_idx]);
                        }
                    }
                }
            }
        }
    }

    bin_data
}

fn main() -> io::Result<()> {
    let input_hex_file = "C:/Project/Project_CodeMaster/PriborTL7/PriborTL7/Debug/Exe/PriborTL7.HEX";
    let output_bin_file = "C:/Project/Project_CodeMaster/PriborTL7/PriborTL7/Debug/Exe/PriborTL7.bin";
    let output_bin_file_cs = "C:/Project/Project_CodeMaster/PriborTL7/PriborTL7/Debug/Exe/PriborTL7_cs.bin";

    let start_address = 0x2000;
    let bin_size = 32768;
    let bin_size2cs = 32766;

    // Load the binary data from HEX file
    let bin_data = load_hex_to_bin(input_hex_file, 0, bin_size);
    let bin_data_cs = load_hex_to_bin(input_hex_file, 0, bin_size2cs);

    // Write the binary data to the first file without checksum
    let mut output_file = File::create(output_bin_file)?;
    output_file.write_all(&bin_data)?;

    // Calculate the checksum
    let checksum = calculate_checksum(&bin_data_cs, start_address);
    let checksum_bytes = checksum.to_be_bytes();

    println!("Checksum bytes (hex): {:02x} {:02x}", checksum_bytes[0], checksum_bytes[1]);

    // Write the binary data to the second file with checksum
    let mut output_file_cs = File::create(output_bin_file_cs)?;
    output_file_cs.write_all(&bin_data_cs)?;
    output_file_cs.write_all(&checksum_bytes)?;

    Ok(())
}

```