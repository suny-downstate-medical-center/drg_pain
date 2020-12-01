import numpy as np

#v = adjust RMP with curr injections, -50, -60, -70
class npcurr():
    def __init__(self, t, dt, base):
        self.vector = np.full( t/dt, base)
        self.base = base
        self.t = np.arange(0, t, dt)
        self.dt = dt

    def sinf(self, delta, dur, amp):
        start = delta / self.dt
        end = start + dur / self.dt
        t = np.arange(0, dur, self.dt)
        self.vector[start:end] = amp * np.sin( t * np.pi / dur ) + self.base

    def rmpf(self, delta, dur, amp):
        start = delta / self.dt
        end = start + dur / self.dt
        self.vector[start:end] = amp * np.linspace( self.base, self.amp + self.amp, end-start )

    def plsf(self, delta, dur, amp):
        start = delta / self.dt
        end = start + dur / self.dt
        self.vector[start:end] = np.full()


def sinf(peak, duration, t):
    return peak * np.sin( t * np.pi / duration )

def rmpf(peak, duration, t):
    return peak * t / duration

def plsf(peak, duration, t):
    i = np.empty( int(duration / cfg.dt) )
    i.fill(peak)
    return i

def stim(delay, duration, peak, f):
    deltv = np.zeros( int(delay / cfg.dt) )
    stmtv = np.arange(0, duration, cfg.dt)
    return di, np.concatenate((deltv,f(peak,duration,stmtv)))