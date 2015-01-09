import sys
import numpy as np
import random
from matplotlib import pyplot as plt
from matplotlib import animation

dt = 1
MAXSPEED = 2

class Vector:
    x = 0
    y = 0
    """-"""
    def __init__(self, x,  y):
        self.x = x
        self.y = y

    def len(self):
        return np.sqrt(self.x**2 + self.y**2)

    def scale(self, s):
        l = self.len()
        return Vector((self.x/l)*s, (self.y/l)*s)

    def vec(self, other):
        return Vector(other.x - self.x, other.y - self.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def dot(self, other):
        return self.x*other.x + self.y*other.y

    def proj(self, p):
        return self.scale(self.dot(p) / self.len())

    def __neg__(self):
        return Vector(-self.x, -self.y)

class Particle:
    """-"""
    def __init__(self, x, y, V):
        # Position
        self.P = Vector(x, y)
        # Direction
        self.V = V
        # mass
        self.m = 10**-23

    def step(self, dt):
        return Vector(self.P.x + dt*self.V.x, self.P.y + dt*self.V.y)

    def findpc(self):
        r = can.R
        c = can.C

        u = -(-can.C.len() + self.P.len() + can.R)/self.V.len()#+ Vector(0, can.R))
        if u >= 0:
            return self.P + self.V.scale(u), u
        else:
            u = (can.C.len() - self.P.len() + can.R)/self.V.len()
            return self.P + self.V.scale(u), u

class Canister:
    """-"""
    def __init__(self, rad=10, elements=10, pos=Vector(0, 0)):
        # Center is located at position 0,0
        self.C = pos
        self.R = rad

        self.listOfParticles = []
        for i in xrange(0, elements):
            a = 2.*np.pi*random.random()
            r = np.sqrt(random.random())
            x = (self.R*r)*np.cos(a)+self.C.x
            y = (self.R*r)*np.sin(a)+self.C.y
            sig = random.uniform(0, np.pi)
            v = random.uniform(0, MAXSPEED)
            speed = Vector(v*np.cos(sig), v*np.sin(sig))
            particle = Particle(x, y, speed)
            self.listOfParticles.append(particle)

    def willcollide(self, p, c, r, v=None):
        return (p.step(dt).vec(c)).len() > r

    def update(self, dt):
        for p in self.listOfParticles:
            if self.willcollide(p, can.C, can.R):
                p1 = p.P
                pc, u = p.findpc()
                vp = p1.vec(p1.proj(pc.vec(can.C)))
                p1m = p1.__add__(vp.scale(vp.len()))
                v2 = pc.vec(p1m).scale(p.V.len())
                p.V = v2
                p.P = pc + p.V.scale(1-u)
            else:
                p.P = p.step(dt)

    def calP(self):
        N = len(self.listOfParticles)
        m = self.listOfParticles[0].m
        vsum = 0
        for particle in self.listOfParticles:
            vsum += particle.V.len()
        A = np.pi*self.R**2
        P = N * m * vsum**2 / 2 * A
        return P

def main():
    global can
    can = Canister()
    fig = plt.figure()
    ax = plt.axes(xlim=(can.C.x-can.R, can.R), ylim=(can.C.y-can.R, can.R))
    line, = ax.plot([], [], 'bo', lw=2)

    print "Canister with radius: ", can.R
    print "Amount of particles: ", len(can.listOfParticles)
    print "Force from particles: ", can.calP()

    def init():
        circle=plt.Circle(( can.C.x, can.C.y),can.R,color='grey')
        fig.gca().add_artist(circle)
        return line,

    def animate(i):
        x = []
        y = []
        for p in can.listOfParticles:
            plt.plot(p.P.x, p.P.y,  '*', color='black')
            x.append(p.P.x)
            y.append(p.P.y)
        line.set_data(x,y)
        can.update(1)
        return line,

    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=300, interval=100, blit=True)
    plt.show()

if __name__ == "__main__":
    main()
