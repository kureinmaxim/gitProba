#ifndef FRAM_H
#define FRAM_H

#include "stm32f4xx_hal.h"

#define FRAM_OK           0x00
#define FRAM_INIT_ERROR   0xFF

#define FRAM_WREN         0x06
#define FRAM_WRDI         0x04
#define FRAM_RDSR         0x05
#define FRAM_WRSR         0x01
#define FRAM_READ         0x03
#define FRAM_WRITE        0x02

#define FRAM_MEM_SIZE     0x8000

typedef struct {
    SPI_HandleTypeDef *hspi;
    GPIO_TypeDef *cs_port;
    uint16_t cs_pin;
} fram_t;

typedef struct
{
    // Communication GPIO pins
	GPIO_TypeDef* miso_port;
	uint16_t miso;
	GPIO_TypeDef* mosi_port;
	uint16_t mosi;
	GPIO_TypeDef* sck_port;
	uint16_t sck;
	GPIO_TypeDef* cs_port;
	uint16_t cs;

    // Additional GPIO pins
	//GPIO_TypeDef* hld_port;
	//uint16_t hld;
	//GPIO_TypeDef* wp_port;
	//uint16_t wp;

    // Static variables
    //uint32_t spi_speed;
    //uint16_t   spi_mode;
    //uint16_t cs_polarity;

} fram_cfg_t;

void fram_cfg_setup(fram_cfg_t *cfg);
int fram_init(fram_t *fram, fram_cfg_t *cfg);
void fram_write_enable(fram_t *fram);
void fram_write_disable(fram_t *fram);
uint8_t fram_read_status(fram_t *fram);
void fram_write_status(fram_t *fram, uint8_t value);
void fram_read(fram_t *fram, uint16_t address, uint8_t *buffer, uint16_t count);
void fram_write(fram_t *fram, uint16_t address, uint8_t *buffer, uint16_t count);
void fram_erase_all(fram_t *fram);

#endif  // FRAM_H

