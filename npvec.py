import numpy as np
import matplotlib.pyplot as plt

#v = adjust RMP with curr injections, -50, -60, -70

class npvec():
    def __init__(self, duration, dt, base):
        self.vector = np.full( int(duration/dt), base).astype('float32')
        self.base = base
        self.t = np.arange(0, duration, dt)
        self.dt = dt

    def sinf(self, delta, dur, amp):
        start = int(delta / self.dt)
        end = start + int(dur / self.dt)
        t = np.arange(0, dur, self.dt)
        self.vector[start:end] = amp * np.sin( t * np.pi / dur ) + self.base

    def rmpf(self, delta, dur, amp):
        start = int(delta / self.dt)
        length = int(dur / self.dt)
        end = start + length
        self.vector[start:end] = np.linspace( self.base, self.base + amp, length )

    def plsf(self, delta, dur, amp):
        start = int(delta / self.dt)
        length = int(dur / self.dt)
        end = start + length
        self.vector[start:end] = np.full( length, self.base + amp)

    def plsf_train(self, deltas, dur, amp):
        for delta in deltas:
            self.plsf(delta, dur, amp)

    def plot(self):
        plt.plot(self.t, self.vector)
        plt.xlabel('time (ms)')
        plt.ylabel('value')
        plt.title('vector')
        plt.show()