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
l = 250             # length of stadium
k = 0.5              # how fast people are to react
h = 0.5        # how close people are stashed next to each other

def cal_u(i, t):
    """
    Hjælpefunktion for make_calculation(x, t).
    Udregner de fire led i formlen for at udregne næste iteration af bølgen
    :param x: x-koordinatet
    :param t: nuværende tidspunkt for bølgen
    :return: fire variable der bruges til udregning af næste bølge-værdi i x
    """
    if t == 0:
        u1 = np.exp(-((i-8.0)**2.0) / 4.0)
        u2 = np.exp(-((i-8.0)**2.0) / 4.0)
        u3 = np.exp(-((i-8.0)**2.0) / 4.0)
        u5 = np.exp(-((i-8.0)**2.0) / 4.0)
    elif t == k:
        u1 = np.exp(-((i-8.0-c*k)**2.0) / 4.0)
        u2 = np.exp(-((i-8.0-c*k)**2.0) / 4.0)
        u3 = np.exp(-((i-8.0-c*k)**2.0) / 4.0)
        u5 = np.exp(-((i-8.0-c*k)**2.0) / 4.0)
    else:
        i = i / h
        t = t / k
        # hvis vi når en kant, skal vi wrappe rundt til den modsatte side af stadium
        try:
            u1 = iterations[t][i+1]
        except IndexError:
            u1 = iterations[t][0]
        u2 = iterations[t][i]
        if i == 0:
            u3 = iterations[t][len(iterations[0])-1]
        else:
            u3 = iterations[t][i-1]
        u5 = iterations[t-1][i]
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
    result = np.int32((c**2.0 * k**2.0) / (h**2.0) * (U1 - 2.0*U2 + U3) + 2.0*U2 - U5)
    return result

if __name__ == "__main__":
    # jeg laver en liste af lister, således at den første liste er antallet af iterationer udført,
    # denne vil stige i takt med at programmet kører, den inderste liste er alle x-koordinaterne for den pågældende
    # iteration.
    global iterations
    iterations = np.array([[0 for _ in np.arange(0, l, h)] for _ in np.arange(0, 400, k)])

    plt.figure("Stadium - Iteration -1 - ikke begyndt wave")
    plt.plot(np.arange(0, l, h), iterations[0])
    plt.show()

    for t in xrange(500):
        for x in np.arange(0, l, h):
            iterations[t+1][x/h] = make_calculation(x, t*k)

    plt.figure("Stadium - Iteration 1 - Fan er oppe!")
    plt.plot(np.arange(0, l, h), iterations[1])
    plt.show()

    plt.figure("Stadium - Iteration 2 - Waven har flyttet sig!")
    plt.plot(np.arange(0, l, h), iterations[51])
    plt.show()

    plt.figure("Stadium - Iteration 233 - Waven har flyttet sig endnu mere!")
    plt.plot(np.arange(0, l, h), iterations[233])
    plt.show()

    plt.figure("Stadium - Iteration 482 - Waven er snart ved kanten")
    plt.plot(np.arange(0, l, h), iterations[482])
    plt.show()

    # En bølge er ikke en bølge ved mindre den bevæger sig.
    # Derfor: Animation!
    fig = plt.figure("Animation af Wave Moment")
    ax = plt.axes(xlim=(0, len(iterations[0])), ylim=(-20, 20))
    line, = ax.plot([], [], lw=2)

    def init():
        global iterations
        iterations = np.array([[0 for _ in np.arange(0, l, h)] for _ in np.arange(0, 400, k)])
        line.set_data([], [])
        return line,

    def animate(i):
        global iterations
        for q in np.arange(0, l, h):
            iterations[i+1][q/h] = make_calculation(q, i*k)
        x = np.linspace(0, len(iterations[0]), len(iterations[0]))
        y = iterations[i]
        line.set_data(x, y)
        if (iterations[i][len(iterations[0])-1] != 0):
            print "Wave reached edge, iteration", i
        return line,

    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=len(iterations[0])+15, interval=100, blit=True)
    plt.show()