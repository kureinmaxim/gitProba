######################################################################
#  Project Makefile
######################################################################

BINARY		= main
SRCFILES	= main.c rtos/heap_4.c rtos/list.c rtos/port.c rtos/tasks.c rtos/opencm3.c
LDSCRIPT	= stm32f103c8t6.ld

CFLAGS += -I/home/mxm/stm32f103c8t6/libopencm3/include/libopencm3/stm32

CFLAGS += -I./rtos
CFLAGS += -I./rtos/portable
CFLAGS += -I./rtos/include
CFLAGS += -I./rtos/portable/GCC/ARM_CM3

include ../../Makefile.incl
include ../Makefile.rtos

######################################################################
#  NOTES:
#
#	1. remove any modules you don't need from SRCFILES
#	2. "make clean" will remove *.o etc., but leaves *.elf, *.bin
#	3. "make clobber" will "clean" and remove *.elf, *.bin etc.
#	4. "make flash" will perform:
#	   st-flash write main.bin 0x8000000
#
######################################################################
