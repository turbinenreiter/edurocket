import matplotlib as mpl
#mpl.use('Agg')  #'WebAgg'
mpl.rcParams.update({'font.size': 12})
import numpy as np
import scipy.integrate as it
from matplotlib import pyplot as plt
import sys

def main(filename):

    # read file
    data = np.genfromtxt(filename,delimiter=';',names=True)

    t = data['t_start']-data['t_start'][0]

    uax, uay, uaz = [a for a in (data['uax'],data['uay'],data['uaz'])]
    h = data['h']
    trigger = data['trigger']

    # analyze

    # max altitude
    dh_max = max(h)-min(h)
    print(dh_max)
    t_hmax_i = h.argmax()
    t_hmax = t[t_hmax_i]

    # parachute trigger
    try:
        t_trigger_i = np.where(trigger==255.)[0][0]
        t_trigger = t[t_trigger_i]
    except:
        print('didn\'t trigger, setting to 0')
        t_trigger_i = 0
        t_trigger = 0

    # integration

    def integrate(data, axis):
        res = [0]
        for i in range(len(data)-1):
            val = (data[i]+data[i+1])/2 * (axis[i+1]-axis[i])
            res.append(res[i]+val)
        return res

    claz = -data['az']*9.81-9.81


    vz = integrate(claz, t)
    #print(max(vz))
    sz = integrate(vz, t)
    #print(max(sz))

    # plot

    fig, ((accel, uaccel), (altitude, gyro)) = plt.subplots(nrows=2, ncols=2, sharex=True)
    fig.set_facecolor('white')

    # These are the "Tableau 20" colors
    c = {}
    tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
                 (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
                 (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
                 (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
                 (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
    colornames = ['blue','lblue','orange','lorange','green','lgreen','red','lred',
                  'purple','lpurple','brown','lbrown','pink','lpink','grey','lgrey',
                  'seaweed','lseaweed','turqois','lturqois']
    for i in range(len(tableau20)):
        r, g, b = tableau20[i]
        c[colornames[i]] = (r / 255., g / 255., b / 255.)

    # accel
    accel.set_title('accelerations', fontsize=22)
    accel.plot(t, data['ax'], color=c['lblue'])
    accel.plot(t, data['ay'], color=c['lred'])
    accel.plot(t, -data['az'], color=c['green'])
    accel.legend(['ax','ay','az'], frameon=False)
    accel.spines['top'].set_visible(False)
    accel.spines['right'].set_visible(False)
    accel.spines['bottom'].set_visible(False)
    accel.tick_params(bottom='off', top='off', right='off')
    accel.set_ylabel('g', rotation='horizontal')

    accel.plot(t_trigger, -data['az'][t_trigger_i], color=c['red'], marker='o')

    accel.axhline(color='k')
    accel.axvline(t_hmax, color=c['lturqois'])

    # uaccel
    uaccel.set_title('uaccelerations', fontsize=22)
    #uaccel.plot(t, uax, color=c['lblue'])
    #uaccel.plot(t, uay, color=c['lred'])
    #uaccel.plot(t, uaz, color=c['green'])
    uaccel.plot(t, vz, color=c['green'])
    uaccel.legend(['uax','uay','uaz'], frameon=False)
    uaccel.yaxis.tick_right()
    uaccel.yaxis.set_label_position("right")
    uaccel.spines['top'].set_visible(False)
    uaccel.spines['left'].set_visible(False)
    uaccel.spines['bottom'].set_visible(False)
    uaccel.tick_params(bottom='off', top='off', right='off')
    uaccel.set_ylabel('g', rotation='horizontal')

    uaccel.plot(t_trigger, uaz[t_trigger_i], color=c['red'], marker='o')

    uaccel.axhline(color='k')
    uaccel.axvline(t_hmax, color=c['lturqois'])

    # altitude
    altitude.set_title('altitude', fontsize=22)
    altitude.plot(t, h, color=c['blue'])
    altitude.plot(t, sz+h[0], color=c['lblue'])
    altitude.legend(['h'], frameon=False)
    altitude.spines['top'].set_visible(False)
    altitude.spines['right'].set_visible(False)
    altitude.spines['bottom'].set_visible(False)
    altitude.tick_params(bottom='off', top='off', right='off')
    altitude.set_ylabel('m', rotation='horizontal')
    altitude.set_xlabel('s')

    altitude.plot(t_trigger, h[t_trigger_i], color=c['red'], marker='o')

    altitude.axhline(min(h), color='k')
    altitude.axvline(t_hmax, color=c['lturqois'])

    # gyro
    gyro.set_title('angular acceleration', fontsize=22)
    gyro.plot(t, data['gx'], color=c['blue'])
    gyro.plot(t, data['gy'], color=c['lred'])
    gyro.plot(t, data['gz'], color=c['green'])
    gyro.legend(['gx', 'gy', 'gz'], frameon=False)
    gyro.yaxis.tick_right()
    gyro.yaxis.set_label_position("right")
    gyro.spines['top'].set_visible(False)
    gyro.spines['left'].set_visible(False)
    gyro.spines['bottom'].set_visible(False)
    gyro.tick_params(bottom='off', top='off', right='off')
    gyro.set_ylabel('Hz/s', rotation='horizontal')
    gyro.set_xlabel('s')

    gyro.plot(t_trigger, data['gz'][t_trigger_i], color=c['red'], marker='o')

    gyro.axhline(color='k')
    gyro.axvline(t_hmax, color=c['lturqois'])

    # savefig config
    sc = 1
    fig.set_size_inches(16*sc,9*sc)
    plt.tight_layout()
    #plt.savefig(filename[:-4]+'.png', dpi=120, format='png', transparent=False, frameon=False)
    plt.show()

if __name__ == "__main__":
    #import convert
    #convert.main(sys.argv[1])
    main(sys.argv[1]) #[:-4]+'.csv')
