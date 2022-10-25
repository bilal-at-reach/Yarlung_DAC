#!C:\Users\Bilal Gabula\AppData\Local\Programs\Python\Python37 python
import sidekickio as sk
from time import sleep
import pyvisa as visa
import time
import datetime

s = sk.SidekickIO()
s.gpio_set_led(True) #GPIO test
s.gpio_set_led(False)


baudrate = 1000000 #1Mhz
s.config_layout_spim(s.SPI_MODE_0, s.SPI_DATA_ORDER_MSB,baudrate)

cs = 10 
s.gpio_config(cs,s.GPIO_CONFIG_DIR_OUT, s.GPIO_CONFIG_PULL_NONE) #CS set to pin 10 

A = 0x0000;



# Keysight 34470A DMM
rm = visa.ResourceManager()
#rm.list_resources()
#dmm = rm.open_resource('USB0::0xF4EC::0xEE38::SDM34FBD4R1837::INSTR')
dmm = rm.open_resource('USB0::0x2A8D::0x0201::MY57701718::INSTR')


dmm.write('*RST')
dmm.write('CONF:VOLT:DC 54 V, MAX')
    
def dmm_voltage(dmm):
    voltDMM = float(dmm.query('MEAS:VOLT:DC?'))
    return voltDMM

def list2str(arr):
    return ','.join(str(item) for item in arr) 

VCC = 5.000 

filename =  'DAC&BUF_test_'+str(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M.csv'))   #'dataps.csv'

f = open(filename,'w')
Header = ['Time', 'DAC Code', 'Voltgae Expected (V)', 'Voltage Measured (V)', 'Error (mV)']
f.write(list2str(Header) + '\n')


#Cycle through all 2^10 DAC codes. 
while A<1025: 
    
    # 2 bytes per DAC write. 
    buf = bytearray(2)
    
    buf[1] = (A<<2 & (0xFF)); # Bottom two bits of registers are 00
    buf[0] = 0x10 | ((A>>6)&(0x0F));# Writting to Address 1 | Writting top bits of data. 
    
    
    #print('Demo: transfer packet', A, buf);
    time_stamp = datetime.datetime.now().strftime('%H:%M:%S')
    s.spim_transfer_packet(cs, buf) #transfer data 
    sleep(0.1) #sleep for selttling 
    
    V_measured = dmm_voltage(dmm)
    V_expected = VCC/1024*A*30/5
    print('DAC Code: ', A, '\t', 'Voltgae Expected: ','{:.9}'.format(V_expected),'V\t','Voltage Measured: ', '{:.9}'.format(V_measured),'V\t', 'Error: ','{:.3}'.format((V_expected-V_measured)*1000),'mV');
    f.write(
            f'{time_stamp},{A},{V_expected},{V_measured},{((V_expected-V_measured)*1000)}\n'
        )
    f.flush()
    A = A+1;

f.close()#Cleanup
