
import time
from pysat.solvers import Minisat22

# Pour le sudoku, les variables représentent des triplets (i,j,k) avec i, j et k dans [0,8].
# Ces triplet on la signification suivante : la variable (i,j,k) est vraie ssi
# dans la solution du sudoku, la case de coordonnée (i,j) contient le chiffre k+1.

# On définit l comme étant les chiffres dans [0,8]
l = list(range(0, 9))

# pos contient tous les triplets (i,j,k) possibles

pos = [(i,j,k) for i in l for j in l for k in l]

def encode(i,j,k):
    """La fonction encode prend un triplet (i,j,k) de pos en argument et renvoie un nombre qui indique la variable correspondant à ce triplet.
    """
    return 1 + i + j* 9 + k * 81

def decode(n):
    """Decode prend en argument prend un nombre entre 1 et 729 qui représente une variable représentant un triplet (i,j,k) et renvoie le triplet correspondant.
    """
    m = n-1
    i = m % 9
    m= m//9
    j = m % 9
    k = m//9
    return (i,j,k)

debut = time.time()

# Instancier la variable phi1 par la contrainte SAT qui indique que
# toute case contient une valeur

phi1 = []

for i in l :
    for j in l:
        h=[encode(i,j,k) for k in l]
        phi1+=[h]

#print(phi1)

# Instancier la variable phi2 par la contrainte SAT qui indique
# qu'une case contient au plus une valeur

phi2 = []

for i in l :
    for j in l:
        for d in l:
            for dd in range(d+1,9):
                phi2.append([-encode(i,j,d),-encode(i,j,dd)])

#print(phi2)

# Instancier la variable phi3 par la contrainte SAT qui indique que
# sur une ligne au plus une fois chaque valeur

phi3 = []

for i in l :
    for d in l:
        for j in l:
            for jj in range(j+1,9):
                phi3.append([-encode(i,j,d),-encode(i,jj,d)])
        

#print(phi3)

# Instancier la variable phi4 par la contrainte SAT qui indique que
# sur une colonne au plus une fois chaque valeur

phi4 = []

for j in l :
    for d in l:
        for i in l:
            for ii in range(i+1,9):
                phi4.append([-encode(i,j,d),-encode(ii,j,d)])

#print(phi3)
# Instancier la variable phi5 par la contrainte SAT qui indique que
# sur un carré au plus une fois chaque valeur.

# Pour cela on peut (ce n'est pas obligé) écrire une fonction carre correspondant
# à la spécification suivante:

phi5 = []

H = [0,1,2]

for i in H:
    for j in H:
        carre = [] 
        hi=i*3
        hj=j*3
        for m in H:
            for n in H:
                carre +=[ [hi+m,hj+n]  ]
        for d in l:
            for h1 in range(len(carre)):
                for h2 in range(h1+1,len(carre)):
                    phi5.append([-encode(carre[h1][0],carre[h1][1],d),-encode(carre[h2][0],carre[h2][1],d)])

#print(phi5)

# Instancier la variable phi6 par la contrainte SAT qui
# représente la grille de l'énoncé.
import os
import sys

phi6 =[]

f = open(os.path.join(sys.path[0], "sudoku.txt"), "r")
i=0
for x in f:
    print(x)
    x=x.replace('\n','').replace(' ','')
    for j in range(9):
        if x[j]!='0':
            phi6.append([encode(i,j,int(x[j])-1)])
    i+=1

print(phi6)

# Cette partie du programme lance le solveur SAT avec la conjonction des contraintes,
# c'est-à-dire la concaténation des listes les représentant.

with Minisat22(bootstrap_with=phi1+phi2+phi3+phi4+phi5+phi6) as m:
    # si on trouve une solution
    if m.solve():
        model = [decode(v) for v in m.get_model() if v >0] 
        
        print("temps d'execution :",time.time()-debut)
        # On affiche le résultat lisiblement
        r = [[0 for i in l] for j in l]
        for (i,j,k) in model:
            r[i][j] += k+1
        print("\n")
        for ligne in r:
            print(ligne)

    else:
        print("pas de solution")
