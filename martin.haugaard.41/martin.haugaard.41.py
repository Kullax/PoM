# -*- coding: utf-8 -*-
from __future__ import division
import sys
from kursusuge6modul import visLife

"""
Dette er min implemenation af "Game of Life".

Jeg har valgt en simpel datastruktur, nemlig en liste af lister, således kan jeg nemt tilgå koordinator på formen
model[i][j]

I denne model vil hver celle være en af to tilstande (1 / 0). Hvor 1 er Levende, og 0 er Død.

Funktionen foerste() vil initialisere et spillebræt givet to globale variable width og height, disse kan ændres efter
behov, og vil definere størrelsen af spillebrættet.
Jeg har valgt at designe mit spillebræt som en lukket ring, dvs bevæger en "crawler" sig ud over kanten af brættet, vil
den bevæge sig viddere på den modsatte side af brættet, dette gælder både for højre og brede.
På samme måde vil et topkoordinat havde indflydelse på et koordinat i bunden af brættet, da disse vil blive set som
naboer.

Jeg har en kort liste af predefinerede opsætninger af spillebrættet i min kode, disse kan vælges ved at give et argument
med under kørsel af koden, fx vil "python martin.haugaard.41.py spaceship" inkludere et system, der kører et antal gange
inden den finder en stilstand, gives ingen sådanne tilfælde placeres den i opgaven definerede crawler i systemet, og den
kravler rundt indtil koden stoppes. Flere modeller kan godt loades ind på samme tidspunkt.
"""

# Globale variable height & width, indeholder dimensionen for spillet
width = 100
height = 100

def spawn_weekender(i,j):
    """
    Laver en weekender, ud fra det givne koordinat,
    OBS: der er ikke wrap around på spawn funktioner, så pas på ikke at lave en stor figur i kanten at brættet
    :param i: brede koordinatet på modellen
    :param j: højde koordinatet på modellen
    :return: None
    """
    set_alive(i+1,j+2, model)
    set_alive(i+1,j+15, model)
    set_alive(i+2,j+2, model)
    set_alive(i+2,j+15, model)
    set_alive(i+3,j+1, model)
    set_alive(i+3,j+3, model)
    set_alive(i+3,j+14, model)
    set_alive(i+3,j+16, model)
    set_alive(i+4,j+2, model)
    set_alive(i+4,j+15, model)
    set_alive(i+5,j+2, model)
    set_alive(i+5,j+15, model)
    set_alive(i+6,j+3, model)
    set_alive(i+6,j+7, model)
    set_alive(i+6,j+7, model)
    set_alive(i+6,j+8, model)
    set_alive(i+6,j+9, model)
    set_alive(i+6,j+10, model)
    set_alive(i+6,j+14, model)
    set_alive(i+7,j+7, model)
    set_alive(i+7,j+8, model)
    set_alive(i+7,j+9, model)
    set_alive(i+7,j+10, model)
    set_alive(i+8,j+3, model)
    set_alive(i+8,j+4, model)
    set_alive(i+8,j+5, model)
    set_alive(i+8,j+6, model)
    set_alive(i+8,j+11, model)
    set_alive(i+8,j+12, model)
    set_alive(i+8,j+13, model)
    set_alive(i+8,j+14, model)
    set_alive(i+10,j+5, model)
    set_alive(i+10,j+12, model)
    set_alive(i+11,j+6, model)
    set_alive(i+11,j+7, model)
    set_alive(i+11,j+10, model)
    set_alive(i+11,j+11, model)


def spawn_spaceship(i, j):
    """
    Tilføjer et spaceship på den givne placering, med venstre toppunkt i (i,j)
    """
    set_alive(i, 2+j, model)
    set_alive(i, 3+j, model)
    set_alive(i, 4+j, model)
    set_alive(1+i, 1+j, model)
    set_alive(1+i, 5+j, model)
    set_alive(2+i, j, model)
    set_alive(2+i, 6+j, model)
    set_alive(3+i, j, model)
    set_alive(3+i, 6+j, model)
    set_alive(4+i, 3+j, model)
    set_alive(5+i, 1+j, model)
    set_alive(5+i, 5+j, model)
    set_alive(6+i, 2+j, model)
    set_alive(6+i, 3+j, model)
    set_alive(6+i, 4+j, model)
    set_alive(7+i, 3+j, model)


def spawn_crawler(i, j):
    """
    Laver en simpel crawler med venstre toppunkt i (i,j)
    """
    set_alive(i+2, j, model)
    set_alive(i+2, j+1, model)
    set_alive(i+2, j+2, model)
    set_alive(i+1, j+2, model)
    set_alive(i, j+1, model)


def spawn_flipper(i,j):
    """
    Laver en lodret flipper med top i (i,j)
    """
    set_alive(i, 0+j, model)
    set_alive(i, 1+j, model)
    set_alive(i, 2+j, model)



def foerste():
    """
    Initialiserings processen hvori der oprettes en list af lists, givet ved de globale variable height og width.

    Ved mindre der er givet et argument med idet scrippet blev initialiseret, ved spillet udelukkende bestå af døde
    celler, argumenter der kan gives er "spaceship" eller "crawler".
    :return: Giver dimensionen af spillet, ved de fire hjørner i et kvadrat
    """
    global model
    model = [[0 for i in range(height)] for j in range(width)]
    if sys.argv.__contains__("spaceship"):
        spawn_spaceship(40,40)
    if sys.argv.__contains__("crawler") or len(sys.argv) == 1:
        spawn_crawler(0,0)
    if sys.argv.__contains__("flipper"):
        spawn_flipper(10,10)
    if sys.argv.__contains__("weekender"):
        spawn_weekender(30,20)
    return 0, len(model), 0, len(model[0])


def naeste():
    """
    Udregner den næste iteration af spillet, ved at oprette et nyt spillebræt, og køre alle elementer igennem i det
    gamle spillebræt, for at se om der enten spawner, dør eller overlever en celle for hvert punkt. Disse observationer
    gemmes i det nye spillebræt, og når alle celler er checket, bliver det gamle spillebræt overskrevet af det nye, og
    dimensionen af brættet returneres.
    :return: giver dimensionen af spillebrættet, bør ikke ændres fra iteration til iteration
    """
    tmp = [[0 for _ in range(height)] for _ in range(width)]
    for i in range(width):
        for j in range(height):
            if check_neighbours((i, j)):
                set_alive(i, j, tmp)
    global model
    model = tmp
    return 0, len(model), 0, len(model[0])


def getup(k):
    """
    Bestemmer koordinatet netop en position over det givne koordinat, hvis dette overskrider spillebrættet fås det
    nederste koordinat, på samme position, som var spillebrættet en ring
    :param k: et sæt at koordinater på spillebrættet, (i,j)
    :return: koordinatet over det givne koordinatsæt
    """
    if k[1] == 0:
        return k[0], height-1
    return k[0], k[1]-1


def getdown(k):
    """
    Bestemmer koordinatet netop en position under det givne koordinat, hvis dette overskrider spillebrættet fås det
    øverste koordinat, på samme position, som var spillebrættet en ring
    :param k: et sæt af koordinater på spillebrættet, (i,j)
    :return: koordinatet under det givne koordinatsæt
    """
    if k[1] == height-1:
        return k[0], 0
    return k[0], k[1]+1


def getleft(k):
    """
    Bestemmer koordinatet netop en position til venstre fra det givne koordinat, hvis dette overskrider spillebrættet
    fås det tilsvarende højre koordinat, på samme højde position, som var spillebrættet en ring
    :param k: et sæt at koordinater på spillebrættet, (i,j)
    :return: koordinatet til venstre fra det givne koordinatsæt
    """
    if k[0] == 0:
        return width-1, k[1]
    return k[0]-1, k[1]


def getright(k):
    """
    Bestemmer koordinatet netop en position til højre fra det givne koordinat, hvis dette overskrider spillebrættet
    fås det tilsvarende venstre koordinat, på samme højde position, som var spillebrættet en ring
    :param k: et sæt af koordinater på spillebrættet, (i,j)
    :return: koordinatet til højre fra det givne koordinatsæt
    """
    if k[0] == width-1:
        return 0, k[1]
    return k[0]+1, k[1]


def getupleft(k):
    """
    En kombination af getleft() og getup(), så det koordinat skråt op til venstre fra det givne koordinat findes
    :param k: et sæt af koordinater på spillebrættet, (i, j)
    :return: koordinatet oppe og til venstre fra det givne koordinatsæt
    """
    return getup(getleft(k))


def getupright(k):
    """
    En kombination af getright() og getup(), så det koordinat skråt op til højre fra det givne koordinat findes
    :param k: et sæt af koordinater på spillebrættet, (i, j)
    :return: koordinatet oppe og til højre fra det givne koordinatsæt
    """
    return getup(getright(k))


def getdownleft(k):
    """
    En kombinaiton af getleft() og getdown(), så det koordinat skråt ned til venstre fra det givne koordinat findes
    :param k: et sæt af koordinater på spillebrættet, (i, j)
    :return: koordinatet nede og til venstre fra det givne koordinatsæt
    """
    return getdown(getleft(k))


def getdownright(k):
    """
    En kombination af getright() og getdown(), så det koordinat skråt ned til højre fra det givne koordinat findes
    :param k: et sæt af koordinater på spillebrættet, (i, j)
    :return: koordinatet nede og til højre fra det givne koordinatsæt
    """
    return getdown(getright(k))


def is_alive(k):
    """
    Checker den globale model, om det givne koordinat indeholder en levende celle
    :param k: et sæt af koordinater på spillebrættet, (i, j)
    :return: en boolean værdi, True hvis cellen er i live (1), False hvis den er død (0)
    """
    return model[k[0]][k[1]] == 1


def set_alive(i, j, m):
    """
    Sætter et koordinat, på en given model til at være i live (1)
    :param i: brede koordinatet på modellen
    :param j: højde koordinatet på modellen
    :param m: den model hvor cellen skal sættes til at være i live på
    :return: None
    """
    m[i][j] = 1


def set_dead(i, j, m):
    """
    Sætter et koordinat, på en given model til at være død (0)
    :param i: brede koordinatet på modellen
    :param j: højde koordinatet på modellen
    :param m: den model hvor cellen skal sættes til at være død
    :return: None
    """
    m[i][j] = 0


def levende(i, j):
    """
    Checker om en celle er levende eller død, adskiller sig fra is_alive() ved at tage to argumenter, i stedet for et
    enkelt sæt at koordinater.
    :param i: brede koordinatet på modellen
    :param j: højde koordinatet på modellen
    :return: en boolean værdi, True hvis cellen er i live (1), False hvis den er død (0)
    """
    return model[i][j] == 1


def check_neighbours(k):
    """
    Tager et koordinat, og checker alle otte naboer fra denne, om de er i live (1) eller er døde (0).
    Hvis det givne koordinat er i live (1), og der er eksakt to eller tre af dens otte naboceller der også er i live,
    da vil koordinatet overleve, ellers vil den dø.
    Hvis koordinatet allerede er dødt (0), og den har netop tre levende naboer, da vil den blive bragt til live.
    :param k: et sæt af koordinater på spillebrættet, (i, j)
    :return: En booleansk værdi der bestemmer hvorvidt koordinatet vil være i live (True) eller dødt (False) i næste
    iteration af spillet.
    """
    alive = 0
    if is_alive(getdown(k)):
        alive += 1
    if is_alive(getup(k)):
        alive += 1
    if is_alive(getright(k)):
        alive += 1
    if is_alive(getleft(k)):
        alive += 1
    if is_alive(getdownleft(k)):
        alive += 1
    if is_alive(getdownright(k)):
        alive += 1
    if is_alive(getupleft(k)):
        alive += 1
    if is_alive(getupright(k)):
        alive += 1
    if is_alive(k) and (alive == 2 or alive == 3):
        return True
    if alive == 3 and (is_alive(k) is False):
        return True
    return False


if __name__ == "__main__":
    # Starter spillet
    visLife(foerste, naeste, levende)

    # TESTING, ved at lukke vinduet med game of life, vil der blive kørt et par hurtige tests for at bekræfte korrekthed
    # af implementationen

    """
    Flipper_test:
    Ved at køre min kode med et ekstra argument 'flipper' vil der blive lavet en tre lang lodret linie i spillet
    dette er en simpel måde at checke om min implemenation af spillets regler virker.
    En linie af længe tre, vil have et center punkt, med netop to naboer, og derved vil denne overleve
    De to yderpunkter har hver kun en nabo (centerpunktet) og vil i næste iteration dø.
    De to døde punkter til højre og venstre fra center punktet, har hver tre naboer, og vil i næste iteration
    blive bragt til live.
    Derved er næste iteration en ret vandret linie, af længe tre, med samme center som før.
    Nu vil hver iteration så skifte mellem en lodret og vandret linie, og vi har os en såkaldt 'flipper'.
    Ved kørsel af min kode "python martin.haugaard.41.py flipper" ser vi at dette er tilfældet.
    """

    """
    Grænsetest:
    Som tidligere nævnt, har jeg valgt at implementere min kode således at spillepladen fungerer som en ring,
    for at teste om min implementering er korrekt, burde et getup() kald på koordinatet (0,0) resultere i koordinatet
    (0, height-1), og ligeledes vil getleft() give (width-1, 0). Disse to kald bliver begge brugt i min funktion
    getupleft(), så getupleft(0,0) burde resultere i (width-1, height-1).
    """
    if getupleft((0,0)) != (width-1, height-1):
        print "Hvis du ser dette er der sket en fejl:\n gettupleft har givet forkert output"
    if getdownright((width-1, height-1)) != (0,0):
        print "Hvis du ser dette er der sket en fejl:\n getdownright har givet forkert output"