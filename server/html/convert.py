from __future__ import division, print_function
import struct
import math
import sys


def loadconfig(filename):
    con = open(filename, 'r')
    lines = con.readlines()
    con.close()
    for name, value in zip(lines[0].split(','), lines[1].split(',')):
        globals()[name.strip()] = float(value.strip())
        #print(name.strip(), value.strip())
    globals()['ascale'] = (16384, 8192, 4096, 2048)[int(accel_range)]
    globals()['gscale'] = (131, 65.5, 32.8, 16.4)[int(gyro_range)]

def fileparse(filename, line_len):
    with open(filename, 'rb') as infile:
            content = infile.readlines()
            dat = b''
            for line in content:       
                    dat = dat + line
    dat_list = []
    for val in dat:
        dat_list.append(val)
    dat_lines = []
    for i in range(0, len(dat_list), line_len):
        dat_lines.append(dat_list[i:i+line_len])
    return dat_lines

def bytes(bl):
    return b''.join(bl)

def lineparse(line):
    t = struct.unpack('I', bytes(line[0:4]))[0]/1000
    if ord(line[4])/80 > 1.5:
        uax = ord(line[4])/80 - 3
    else:
        uax = ord(line[4])/80
    if ord(line[5])/80 > 1.5:
        uay = ord(line[5])/80 - 3
    else:
        uay = ord(line[5])/80
    if ord(line[6])/80 > 1.5:
        uaz = ord(line[6])/80 - 3
    else:
        uaz = ord(line[6])/80
    ax = struct.unpack('>h', bytes(line[7:9]))[0]/ascale
    ay = struct.unpack('>h', bytes(line[9:11]))[0]/ascale
    az = struct.unpack('>h', bytes(line[11:13]))[0]/ascale
    gx = struct.unpack('>h', bytes(line[13:15]))[0]/gscale/360
    gy = struct.unpack('>h', bytes(line[15:17]))[0]/gscale/360
    gz = struct.unpack('>h', bytes(line[17:19]))[0]/gscale/360
    T = temperature(line[19:21])
    p = pressure(ord(line[21]), ord(line[22]), ord(line[23]), int(oversample_sett), line[19:21])
    h = altitude(p, 101325.0)
    trigger = ord(line[24])

    return [t,uax,uay,uaz,ax,ay,az,gx,gy,gz,T,p,h,trigger]

def temperature(UT_raw):
    UT = struct.unpack('>h', bytes(UT_raw))[0]
    X1 = (UT-AC6)*AC5/2**15
    X2 = MC*2**11/(X1+MD)
    B5_raw = X1+X2
    return (((X1+X2)+8)/2**4)/10

def B5(UT_raw):
    UT = struct.unpack('>h', bytes(UT_raw))[0]
    X1 = (UT-AC6)*AC5/2**15
    X2 = MC*2**11/(X1+MD)
    B5_raw = X1+X2
    return B5_raw

def pressure(MSB_raw, LSB_raw, XLSB_raw, oversample_sett, UT_raw):
    MSB = MSB_raw
    LSB = LSB_raw
    XLSB = XLSB_raw
    UP = ((MSB << 16)+(LSB << 8)+XLSB) >> (8-oversample_sett)
    B6 = B5(UT_raw)-4000
    X1 = (B2*(B6**2/2**12))/2**11
    X2 = AC2*B6/2**11
    X3 = X1+X2
    B3 = ((int((AC1*4+X3)) << oversample_sett)+2)/4
    X1 = AC3*B6/2**13
    X2 = (B1*(B6**2/2**12))/2**16
    X3 = ((X1+X2)+2)/2**2
    B4 = abs(AC4)*(X3+32768)/2**15
    B7 = (abs(UP)-B3) * (50000 >> oversample_sett)
    if B7 < 0x80000000:
        pressure = (B7*2)/B4
    else:
        pressure = (B7/B4)*2
    X1 = (pressure/2**8)**2
    X1 = (X1*3038)/2**16
    X2 = (-7357*pressure)/2**16
    return pressure+(X1+X2+3791)/2**4

def altitude(pressure, baseline):
    p = -7990.0*math.log(pressure/baseline)
    return p

def main(filename):

    loadconfig('/home/oeplse/data/config.txt')
    lines = fileparse(filename, 25)
    log = open(filename[:-4]+'.csv', 'w')
    log.write('t_start;uax;uay;uaz;ax;ay;az;gx;gy;gz;temp_imu;p;h;trigger\n')
    for line in lines:
        log.write('{};{};{};{};{};{};{};{};{};{};{};{};{};{}\n'.format(*lineparse(line)))
    log.close()

if __name__ == '__main__':
    main(sys.argv[1])
