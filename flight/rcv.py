import pyb

class Reciever():

    def __init__(self):

        self.timer = pyb.Timer(2, prescaler=83, period=0x3ffffff)

        self.itq_ch1 = pyb.ExtInt(pyb.Pin.board.X1, pyb.ExtInt.IRQ_RISING_FALLING, pyb.Pin.PULL_DOWN, self.time)

        self.ch = [None, [0, 0, 0]]

    def time(self, line):

        if pyb.Pin.board.X1.value():
            self.timer.counter(0)
        else:
            self.ch[1][1] = (self.timer.counter()-1500) // 7
            if abs(self.ch[1][0]-self.ch[1][1]) < 25:
                self.ch[1][0] = self.ch[1][1]
            elif self.ch[1][1] == self.ch[1][2]:
                self.ch[1][0] = self.ch[1][1]
            else:
                self.ch[1][2] = self.ch[1][1]
