#import matplotlib as mpl
#mpl.use('Agg')
import numpy as np
from matplotlib import pyplot as plt
import sys

def main(filename):

    data1 = np.genfromtxt(filename,delimiter=';',names=True)

    fig, ((accel1, accel2), (pressure, pressure2)) = plt.subplots(nrows=2, ncols=2, sharex=True)

    uax, uay, uaz = [a for a in (data1['uax'],data1['uay'],data1['uaz'])]

    trigger = data1['trigger']
    t_trigger_i = np.where(trigger==255.)[0][0]
    t_trigger = data1['t_start'][t_trigger_i]

    h = data1['h']
    #print(max(h), min(h), max(h)-min(h))
    dmax = h-max(h)
    t_max = data1['t_start'][h.argmax()]

    accel1.plot(data1['t_start'],data1['ax'], 'g', alpha = 0.2)
    accel1.plot(data1['t_start'],data1['ay'], 'b', alpha = 0.2)
    accel1.plot(data1['t_start'],-data1['az'], 'r', alpha = 1)
    accel1.yaxis.tick_right()
    accel1.yaxis.set_label_position("right")
    accel1.set_title('accelerations')
    accel1.legend(['ax [g]','ay [g]','az [g]']) #'uax','uay','uaz',
    #accel1.axes.set_xlim([t_max-10,t_max+10])
    accel1.axhline(color='k')
    accel1.axvline(t_max, color='k')
    #accel1.set_xlabel('t [s]')
    accel1.set_ylabel('a [g]')

    accel2.plot(data1['t_start'],uax, 'b', alpha = 0.2)
    accel2.plot(data1['t_start'],uay, 'g', alpha = 0.2)
    accel2.plot(data1['t_start'],uaz, 'r', alpha = 1)
    #accel2.plot(data1['t_start'],data1['ax'], 'g')
    #accel2.plot(data1['t_start'],data1['ay'], 'b')
    #accel2.plot(data1['t_start'],-data1['az'], 'r')
    accel2.yaxis.tick_right()
    accel2.yaxis.set_label_position("right")
    accel2.set_title('uaccelerations')
    accel2.legend(['uax [g]','uay [g]','uaz [g]'])
    #accel2.axes.set_xlim([t_max-10,t_max+10])
    accel2.axhline(color='k')
    accel2.axvline(t_max, color='k')
    #accel2.set_xlabel('t [s]')
    accel2.set_ylabel('a [g]')

    pressure.plot(data1['t_start'],data1['h'])
    pressure.plot(t_trigger,data1['h'][t_trigger_i], 'r', marker='o')
    pressure.set_title('height')
    #pressure.axes.set_xlim([t_max-10,t_max+10])
    pressure.axhline(max(h), color='k')
    pressure.axhline(min(h), color='k')
    pressure.axvline(t_max, color='k')
    #temp = pressure.twinx()
    #temp.plot(data1['t_start'],data1['p'], 'b', alpha=0.3) #varios
    #temp.plot(data1['t_start'],vario, 'r', alpha=0.1) #data1['p']
    #temp.plot(data1['t_start'],dmax, 'g', alpha=0.1) #data1['p']
    #temp.plot(data1['t_start'],data1['temp_imu'], 'r')
    #temp.legend(['p [mbar]'], loc=2)
    pressure.legend(['h [m]'], loc=4)
    pressure.set_xlabel('t [s]')
    pressure.set_ylabel('h [m]')
    pressure.yaxis.tick_right()
    pressure.yaxis.set_label_position("right")
    #temp.set_ylabel('p [mbar]')
    #, 'temp baro', 'temp imu'])

    pressure2.plot(data1['t_start'],data1['gx'], 'g', alpha=0.2)
    pressure2.plot(data1['t_start'],data1['gy'], 'b', alpha=0.2)
    pressure2.plot(data1['t_start'],data1['gz'], 'r', alpha=1)
    pressure2.axvline(t_max, color='k')
    #pressure2.axes.set_xlim([t_max-10,t_max+10])
    pressure2.yaxis.tick_right()
    pressure2.yaxis.set_label_position("right")
    pressure2.set_title('angular acceleration')
    pressure2.legend(['gx', 'gy', 'gz'])
    pressure2.axhline(color='k')
    pressure2.set_xlabel('t [s]')
    pressure2.set_ylabel('ang accel [Hz/s]')



    #fff.plot(data1['t'],data1['fff'])
    #fff.axes.set_ylim([-0.1,1.1])
    #fff.set_title('freefall')

    #accel2 = accel1.twinx()

    #accel2.set_title('accelerations')

    #accel2.legend(['ax','ay','az'])



    #accel.spines['right'].set_visible(False)
    #accel.spines['top'].set_visible(False)
    #pressure.spines['right'].set_visible(False)
    #pressure.spines['top'].set_visible(False)
    #accel.yaxis.set_ticks_position('left')
    #accel.xaxis.set_ticks_position('bottom')
    #pressure.yaxis.set_ticks_position('left')
    #pressure.xaxis.set_ticks_position('bottom')
    sc = 1
    fig.set_size_inches(16*sc,9*sc)
    plt.tight_layout()
    plt.savefig(filename[:-4]+'.png', dpi=120, format='png', transparent=False, frameon=False)
    plt.show()

if __name__ == "__main__":
    import convert
    convert.main(sys.argv[1])
    main(sys.argv[1][:-4]+'.csv')
