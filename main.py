from cardbrawlers import DecklistCB, DecklistOnlyCB
from altf4 import DecklistA4, DecklistOnlyA4
from cartamagica import DecklistCM, DecklistOnlyCM
import csv

file='decklists\\yang zing.txt'

tableurCM=DecklistCM(file)
tableurCB=DecklistCB(file)
tableurA4=DecklistA4(file)

tableurOnlyCB=DecklistOnlyCB(file)
tableurOnlyA4=DecklistOnlyA4(file)
tableurOnlyCM=DecklistOnlyCM(file)

with open('tableaux\\comparateur.csv', mode='w', newline='') as comp:
    wcomp=csv.writer(comp, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    wcomp.writerow(['carte','qt','prix','boutique'])
    for i in range(len(tableurCM)-1):
        minT = min(tableurCM[i][2],tableurCB[i][2],tableurA4[i][2])
        if tableurCM[i][2]==minT and tableurCM[i][1]!=0:
            tableurCM[i].append('cartamagica')
            wcomp.writerow(tableurCM[i])
        if tableurCB[i][2]==minT and tableurCB[i][1]!=0:
            tableurCB[i].append('cardbrawlers')
            wcomp.writerow(tableurCB[i])
        if tableurA4[i][2]==minT and tableurA4[i][1]!=0:
            tableurA4[i].append('altf4')
            wcomp.writerow(tableurA4[i])
print('------tableau comparatif done------')

with open('tableaux\\cardbrawlers.csv', mode='w', newline='') as comp:
    wcomp=csv.writer(comp, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    wcomp.writerow(['carte','qt voulue','qt dispo','prix'])
    for i in tableurOnlyCB[0]:
        wcomp.writerow(list(i))
    wcomp.writerow(['','','total :',tableurOnlyCB[1]])

with open('tableaux\\cartamagica.csv', mode='w', newline='') as comp:
    wcomp=csv.writer(comp, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    wcomp.writerow(['carte','qt voulue','qt dispo','prix'])
    for i in tableurOnlyCM[0]:
        wcomp.writerow(list(i))
    wcomp.writerow(['','','total :',tableurOnlyCB[1]])

with open('tableaux\\altf4.csv', mode='w', newline='') as comp:
    wcomp=csv.writer(comp, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    wcomp.writerow(['carte','qt voulue','qt dispo','prix'])
    for i in tableurOnlyA4[0]:
        wcomp.writerow(list(i))
    wcomp.writerow(['','','total :',tableurOnlyCB[1]])
