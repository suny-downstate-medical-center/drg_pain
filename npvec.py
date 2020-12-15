import numpy as np
import matplotlib.pyplot as plt

#v = adjust RMP with curr injections, -50, -60, -70

class npvec():
    def __init__(self, duration, dt, base):
        self.end = int(duration / dt)
        self.vector = np.full( self.end , base).astype('float32')
        self.base = base
        self.t = np.arange(0, duration, dt)
        self.dt = dt

    def sinf(self, delta, dur, amp):
        start = int(delta / self.dt)
        if start > self.end: return
        end = start + int(dur / self.dt)
        if end > self.end: 
            end = self.end
            tlength = end - start
        t = np.arange(0, dur, self.dt)
        self.vector[start:end] = amp * np.sin( (t + start) * np.pi / dur ) + self.base

    def rmpf(self, delta, dur, amp):
        start = int(delta / self.dt)
        if start > self.end: return
        length = int(dur / self.dt)
        end = start + length
        if end > self.end: 
            end = self.end
            tlength = end - start
            self.vector[start:end] = np.linspace( self.base, self.base + amp, length )[:tlength]
        self.vector[start:end] = np.linspace( self.base, self.base + amp, length )

    def plsf(self, delta, dur, amp):
        start = int(delta / self.dt)
        if start > self.end: return
        length = int(dur / self.dt)
        end = start + length
        if end > self.end: 
            end = self.end
            length = end - start
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
