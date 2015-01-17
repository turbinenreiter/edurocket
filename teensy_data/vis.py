import matplotlib as mpl
#mpl.use('Agg')  #'WebAgg'
mpl.rcParams.update({'font.size': 12})
import numpy as np
import matplotlib.pyplot as plt
import mpld3
import sys

def main(filename):

    filename = filename.split('/')[-1]
    # read file
    data = np.genfromtxt('./data/'+filename,delimiter=',',names=True)

    t = data['millis']-data['millis'][0]

    h = data['alt']

    # plot

    fig, ((accel, ang), (altitude, gyro)) = plt.subplots(nrows=2, ncols=2, sharex=True)
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
    accel.axhline(color='k')

    # ang
    ang.set_title('angles', fontsize=22)
    ang.plot(t, data['pitch'], color=c['lblue'])
    ang.plot(t, data['yaw'], color=c['lred'])
    ang.plot(t, data['roll'], color=c['green'])
    ang.legend(['pitch','yaw','roll'], frameon=False)
    ang.yaxis.tick_right()
    ang.yaxis.set_label_position("right")
    ang.spines['top'].set_visible(False)
    ang.spines['left'].set_visible(False)
    ang.spines['bottom'].set_visible(False)
    ang.tick_params(bottom='off', top='off', right='off')
    ang.set_ylabel('deg', rotation='horizontal')
    accel.axhline(color='k')

    # altitude
    altitude.set_title('altitude', fontsize=22)
    altitude.plot(t, h, color=c['blue'])
    altitude.legend(['h'], frameon=False)
    altitude.spines['top'].set_visible(False)
    altitude.spines['right'].set_visible(False)
    altitude.spines['bottom'].set_visible(False)
    altitude.tick_params(bottom='off', top='off', right='off')
    altitude.set_ylabel('m', rotation='horizontal')
    altitude.set_xlabel('s')
#    altitude.axhline(min(h), color='k')

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
    gyro.set_ylabel('deg/s', rotation='horizontal')
    gyro.set_xlabel('s')
    gyro.axhline(color='k')

    # savefig config
    sc = 1
    fig.set_size_inches(16*sc,9*sc)
    plt.tight_layout()
    mpld3.save_html(fig, './graphs/'+filename.split('.')[0]+'.html')
#    plt.savefig(filename[:-4]+'.png', dpi=120, format='png', transparent=False, frameon=False)
#    plt.show()

if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except:
        print 'empty file'
