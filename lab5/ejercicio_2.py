#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LABORATORIO 5 - EJERCICIO 2
Minima cantidad de losas para conocer el material de un tubo.

Sebastian Garcia 201630047
Nicolas Sotelo 201623026
"""


from __future__ import division
from pyomo.environ import *
from pyomo.opt import SolverFactory
from math import pow
import numpy as np

# ==============
# MODEL
# ==============


Model = ConcreteModel()

# ==============
# SETS
# ============== 


tubos = 7
losas = 20

T = RangeSet(1, tubos)
L = RangeSet(1, losas)


# ==============
# PARAMETERS
# ==============

mapa = {}

for t in range(1, tubos + 1):
    for l in range(1, losas + 1):
        mapa[f't{t},l{l}'] = 0


mapa['t1,l1'] = 1
mapa['t1,l5'] = 1

mapa['t2,l2'] = 1
mapa['t2,l3'] = 1
mapa['t2,l6'] = 1
mapa['t2,l7'] = 1

mapa['t3,l5'] = 1
mapa['t3,l9'] = 1

mapa['t3,l5'] = 1
mapa['t3,l9'] = 1

mapa['t4,l8'] = 1
mapa['t4,l12'] = 1
mapa['t4,l16'] = 1
mapa['t4,l20'] = 1
mapa['t4,l19'] = 1

mapa['t5,l9'] = 1
mapa['t5,l10'] = 1
mapa['t5,l13'] = 1
mapa['t5,l14'] = 1

mapa['t6,l10'] = 1
mapa['t6,l11'] = 1
mapa['t6,l14'] = 1
mapa['t6,l15'] = 1

mapa['t7,l13'] = 1
mapa['t7,l17'] = 1


# ==============
# VARIABLES
# ==============


Model.x = Var(L, domain = Binary )


# ==============
# OBJECTIVE FUNCTION
# ==============


Model.OBJ = Objective(expr = 
                      sum( Model.x[i] for i in L ),
                      sense = minimize)

# ==============
# CONSTRAINTS
# ==============


def conocer(Model, t):
    if t in range(1, tubos+1):
        return sum( mapa[f"t{t},l{l}"] * Model.x[l] for l in L ) == 1
    else:
        return Constraint.Skip

Model.conocer=Constraint(T, rule = conocer)

# ==============
# SOLVER
# ==============
SolverFactory('glpk').solve(Model)

Model.display()

print('''\n
-------------------------
      RESULTADOS
-------------------------\n
      ''')


for l in L:
    if Model.x[l].value != 0:
        print(f'Losa {l}')
















