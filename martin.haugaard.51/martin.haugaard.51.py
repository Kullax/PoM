import sys
import numpy as np
import random
from matplotlib import pyplot as plt
from matplotlib import animation

"""
This is my simple simulation of a Canister filled with moving particles
"""

dt = 1
MAXSPEED = 40
m = 10**-23

class Vector:
    """
    My Vector class, used for both direction and position of elements in the program
    """
    x = 0
    y = 0

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
        """
        In order to negate a Vector by using the - operator.
        """
        return Vector(-self.x, -self.y)


class Particle:
    """
    A Particle, with a Position vector P, a Direction vector V, and a globally defined mass, m.
    """
    def __init__(self, x, y, V):
        # Position
        self.P = Vector(x, y)
        # Direction
        self.V = V
        # mass
        self.m = m

    def step(self, dt):
        """
        Determines the position of the particle, after dt amount of time
        :param dt:  time passed since current position
        :return: estimated particle position
        """
        return Vector(self.P.x + dt*self.V.x, self.P.y + dt*self.V.y)

    def findpc(self):
        """
        Determines the particle collision position, and the u scale value matching
        """
        u = -(-can.C.len() + self.P.len() + can.R)/self.V.len()
        if u >= 0:
            return self.P + self.V.scale(u), u
        else:
            u = (can.C.len() - self.P.len() + can.R)/self.V.len()
            return self.P + self.V.scale(u), u


class Canister:
    """-"""
    def __init__(self, rad=500, elements=10, pos=Vector(0, 0)):
        # Center is located at position 0,0
        self.C = pos
        self.R = rad
        self.listOfParticles = []
        # Generates a list of particles, according to the input
        for i in xrange(0, elements):
            a = 2.*np.pi*random.random()
            r = np.sqrt(random.random())
            # x and you will be inside the canister radius
            x = (self.R*r)*np.cos(a)+self.C.x
            y = (self.R*r)*np.sin(a)+self.C.y
            # the randomly generated direction of the particle is given through these two variables
            sig = random.uniform(0, np.pi)
            v = random.uniform(0, MAXSPEED)
            speed = Vector(v*np.cos(sig), v*np.sin(sig))
            # new particle is generated and appended to the list
            particle = Particle(x, y, speed)
            self.listOfParticles.append(particle)

    def willcollide(self, p, c, r, v=None):
        """
        Boolean check if a particle will collide with the canister if the direction is unchanged
        """
        return (p.step(dt).vec(c)).len() > r

    def update(self, dt):
        """
        Updates the position for each particle in the canister
        """
        for p in self.listOfParticles:
            if self.willcollide(p, can.C, can.R):
                p1 = p.P
                pc, u = p.findpc()
                vp = p1.vec(p1.proj(pc.vec(can.C)))
                p1m = p1.__add__(vp.scale(vp.len()))
                v2 = pc.vec(p1m).scale(p.V.len())
                p.V = v2
                p.P = pc + p.V.scale(p.V.len()*(1-u))
            else:
                p.P = p.step(dt)

    def calP(self):
        """
        Returns the force applied on the canister from the particles colliding
        """
        N = len(self.listOfParticles)
        m = self.listOfParticles[0].m
        vsum = 0
        for particle in self.listOfParticles:
            vsum += particle.V.len()
        A = np.pi*self.R**2
        F = 0.5 * A * (2*self.R) * m * N * vsum**2
        return F

    def setTemp(self, T):
        """
        Scales the direction vector of each particle, to have the length corresponding to the given temperature
        """
        kb = 1.380658*10**-23
        v = np.sqrt(2)*np.sqrt(kb)*np.sqrt(T) / np.sqrt(m)
        for p in self.listOfParticles:
            # Downscale the direction vector
            p.V = p.V.scale(1)
            # Scale the direction vector to fit the temperature
            p.V = p.V.scale(v)


def show_animation():
    """
    Creates a new figure with an animation of the system
    """
    fig = plt.figure()
    ax = plt.axes(xlim=(can.C.x-can.R, can.R), ylim=(can.C.y-can.R, can.R))
    plt.title("Canister with %d particles\nProducing force of %s" % (len(can.listOfParticles), can.calP()))
    line, = ax.plot([], [], 'bo', lw=2)

    print "Starting new animation"
    print "Canister with radius: ", can.R
    print "Amount of particles: ", len(can.listOfParticles)
    print "Force from particles: ", can.calP()

    # Here starts the actual animation
    def init():
        circle = plt.Circle((can.C.x, can.C.y), can.R, color='grey')
        fig.gca().add_artist(circle)
        return line,

    # Each new frame will plot the current system, then update it for the next frame
    def animate(i):
        x = []
        y = []
        for p in can.listOfParticles:
            plt.plot(p.P.x, p.P.y,  '*', color='black')
            x.append(p.P.x)
            y.append(p.P.y)
        line.set_data(x, y)
        can.update(1)
        return line,

    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                    interval=100, blit=True)
    plt.show()


def main():
    # Define the canister, using default setting
    global can
    can = Canister()
    show_animation()

    # Change the temperature to 300 K
    can.setTemp(300)
    show_animation()
    # Now increase the temperature to 373.15 K
    can.setTemp(373.15)
    show_animation()

if __name__ == "__main__":
    main()