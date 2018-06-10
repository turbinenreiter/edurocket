# datalogger.py
# Logs the data from the acceleromter to a file on the SD-card

import struct
import pyb
from bmp180 import BMP180
from mpu9150 import MPU9150
from rcv import Reciever
import os
import gc
import sys

hmax = 0
hc = 0
def para(h):
    global hmax, hc
    if h > hmax:
        hmax = h
    elif h < hmax-3:
        hc = hc + 1
        if hc == 4:
            pyb.LED(3).on()
            return b'\xff'
    else:
        pass
    return b'\x00'

def main():

    # create objects
    accel = pyb.Accel()
    blue = pyb.LED(4)
    switch = pyb.Switch()
    servo = pyb.Servo(2)
    pyb.delay(10)
    baro = BMP180('X')
    pyb.delay(10)
    imu = MPU9150('X', 1)
    rcv = Reciever()

    # settings
    baro.oversample_sett = 3
    servo.calibration(860, 2160, 1500)

    # test i2c
    if len(baro._bmp_i2c.scan()) != 4:
        pyb.LED(2).on()
        print('sensors failed')
    else:
        print('sensors ready')

    # create dir
    if 'log' not in os.listdir('/sd/'):
        os.mkdir('/sd/log')
        print('created log dir')
    else:
        print('log dir already there')

    config = open('/sd/log/config.txt', 'w')
    config.write('AC1, AC2, AC3, AC4, AC5, AC6, B1, B2, MB, MC, MD, oversample_sett, accel_range, gyro_range\n')
    con = baro.compvaldump() + [imu.accel_range(), imu.gyro_range()]
    config.write('{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(*con))
    config.close()
    print('wrote config file')

    # loop
    while True:

        # wait for interrupt
        pyb.wfi()

        # start if switch is pressed
        if (rcv.ch[1][0] < -45) or switch():                            # switch(): rcv.ch[1][0] < -45
            pyb.delay(300)                      # delay avoids detection of multiple presses
            blue.on()                           # blue LED indicates file open
            pyb.LED(3).off()
            filename = '/sd/log/log'+str(len(os.listdir('log'))+1)+'.bin'
            print('opening '+filename)
            log = open(filename, 'wb')
            i = 0
            trigger = b'\x00'
            gc.collect()
            t0 = pyb.millis()/1000
            # until switch is pressed again
            while (rcv.ch[1][0] < 45) and (not switch()):                      #not switch(): rcv.ch[1][0] < 45

                t_start_ms = pyb.millis()
                next(baro.gauge())
                log.write(b''.join([struct.pack('I', t_start_ms),
                                    bytes(accel.filtered_xyz()),
                                    imu.get_accel_raw(),
                                    imu.get_gyro_raw(),
                                    baro.UT_raw,
                                    baro.MSB_raw,
                                    baro.LSB_raw,
                                    baro.XLSB_raw,
                                    trigger]))
                i = i+1
                if i%100 == 0:
                    trigger = para(baro.altitude)
                    dt = t_start_ms/1000-t0
                    sys.stdout.write('writing '+
                                     filename+
                                     ' %d lines, %d s, %d Hz \r'
                                     % (i, dt, i/dt))
                    pyb.LED(1).toggle()

            # end after switch is pressed again
            log.close()                         # close file
            blue.off()                          # blue LED indicates file closed
            print('\nclosed '+filename)
            pyb.delay(300)                      # delay avoids detection of multiple presses

main()
