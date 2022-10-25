#!C:\Users\Bilal Gabula\AppData\Local\Programs\Python\Python37 python
import sidekickio as sk
from time import sleep

s = sk.SidekickIO()
s.gpio_set_led(True) #GPIO test
s.gpio_set_led(False)

baudrate = 1000000 #1Mhz
s.config_layout_spim(s.SPI_MODE_0, s.SPI_DATA_ORDER_MSB,baudrate)

cs = 10 
s.gpio_config(cs,s.GPIO_CONFIG_DIR_OUT, s.GPIO_CONFIG_PULL_NONE) #CS set to pin 10 

A = 0x0000;

while A<1025: 
    
    # max size is the packet size minus the chip select byte
    buf = bytearray(2)
    
    # write some data to the buffer so we can tell if any apis mutate it
    buf[1] = (A<<2 & (0xFF));
    buf[0] = 0x10 | ((A>>6)&(0x0F));
    
    
    A = A+1; # Script will error out once A = > 256
    print('Demo: transfer packet', A, buf);
    
    # transfer mutates buf
    s.spim_transfer_packet(cs, buf)

    sleep(0.1)

