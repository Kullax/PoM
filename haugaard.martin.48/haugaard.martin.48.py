from __future__ import division
#-*- coding: UTF-8 -*-
__author__ = 'Martin Simon Haugaard'
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
"""
Simpel implementation af en bølge på et stadium, i form af en en-dimensionel-graf
"""

# Globale variable, bør ikke ændres
c = 1
l = 250
k = 0.9
h = 0.9


def cal_u(x, t):
    """
    Hjælpefunktion for make_calculation(x, t).
    Udregner de fire led i formlen for at udregne næste iteration af bølgen
    :param x: x-koordinatet
    :param t: nuværende tidspunkt for bølgen
    :return: fire variable der bruges til udregning af næste bølge-værdi i x
    """
    if t == 0:
        u1 = np.exp(-((x-7.0)**2.0) / 4.0)
        u2 = np.exp(-((x-8.0)**2.0) / 4.0)
        u3 = np.exp(-((x-9.0)**2.0) / 4.0)
        u5 = np.exp(-((x-8.0)**2.0) / 4.0)
    elif t == k:
        u1 = np.exp(-((x-7.0-c*k)**2.0) / 4.0)
        u2 = np.exp(-((x-8.0-c*k)**2.0) / 4.0)
        u3 = np.exp(-((x-9.0-c*k)**2.0) / 4.0)
        u5 = np.exp(-((x-8.0-c*k)**2.0) / 4.0)
    else:
        # hvis vi når en kant, skal vi wrappe rundt til den modsatte side af stadium
        if x == l-1:
            u1 = iterations[t][0]
        else:
            u1 = iterations[t][x+1]
        u2 = iterations[t][x]
        if x == 0:
            u3 = iterations[t][l-1]
        else:
            u3 = iterations[t][x-1]
        u5 = iterations[t-1][x]
    return u1, u2, u3, u5


def make_calculation(x, t):
    """
    Udregner den aktuelle bølge-værdi i x for den næste iteration af bølgen
    :param x: x koordinatet
    :param t: nuværende tidsværdi
    :return: den næste værdi for x, i t+1
    """
    U1, U2, U3, U5 = cal_u(x, t)
    # Den i rapporten fremviste formel
    result = (c**2.0 * k**2.0) / (h**2.0) * (U1 - 2.0*U2 + U3) + 2.0*U2 - U5
    return result

if __name__ == "__main__":
    # jeg laver en liste af lister, således at den første liste er antallet af iterationer udført,
    # denne vil stige i takt med at programmet kører, den inderste liste er alle x-koordinaterne for den pågældende
    # iteration.
    global iterations

    iterations = [[0 for _ in xrange(l)] for _ in xrange(1)]

    plt.figure("Stadium - Iteration 0")
    plt.plot(xrange(l), iterations[0])
    plt.show()

    new_line = [0 for _ in xrange(l)]
    iterations.append(new_line)
    # Tilføjer endnu en interation til listen af iterationer
    for q in xrange(l):
        iterations[1][q] = make_calculation(q, 0)

    plt.figure("Stadium - Iteration 1 - Fan er oppe!")
    plt.plot(xrange(l), iterations[1])
    plt.show()
    # Tilføjer endnu 300 iterationer, dette burde være nok til at nå hele omgangen rundt om stadium
    for i in range(300):
        new_line = [0 for _ in xrange(l)]
        iterations.append(new_line)
        for q in xrange(l):
            iterations[1+i][q] = make_calculation(q, i)

    plt.figure("Stadium - Iteration 51 - Waven har flyttet sig!")
    plt.plot(xrange(l), iterations[int(np.floor(l/2))])
    plt.show()

    plt.figure("Stadium - Iteration 237 - Waven har flyttet sig endnu mere!")
    plt.plot(xrange(l), iterations[237])
    plt.show()

    # En bølge er ikke en bølge ved mindre den bevæger sig.
    # Derfor: Animation!
    fig = plt.figure("Animation af Wave Moment")
    ax = plt.axes(xlim=(0, l), ylim=(-20, 20))
    line, = ax.plot([], [], lw=2)

    def init():
        global iterations
        iterations = [[0 for _ in xrange(l)] for _ in xrange(1)]
        line.set_data([], [])
        return line,

    def animate(i):
        new_line = [0 for _ in xrange(l)]
        iterations.append(new_line)
        for q in xrange(l):
            iterations[i+1][q] = make_calculation(q, i)
        x = np.linspace(0, l, l)
        y = iterations[i]
        line.set_data(x, y)
        if round(y[l-1],2) != 0:
            print "Doing the wave on the edge!\n Iteration: ", i
        return line,

    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=l, interval=100, blit=True)
    plt.show()