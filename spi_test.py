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

while True: 
    print('Demo: transfer packet')

    # max size is the packet size minus the chip select byte
    buf = bytearray(sk.MAX_PACKET_SIZE - 1)

    # write some data to the buffer so we can tell if any apis mutate it
    for k in range(len(buf)):
        buf[k] = k

    # transfer mutates buf
    s.spim_transfer_packet(cs, buf)

    # we expect buf to be all zeros if there isn't a device connected
    # print(buf)

    # reset buf data
    #for k in range(len(buf)):
    #    buf[k] = k

    # write has no effect on buf
    #sk.spim_write(cs, buf);
    sleep(1)

