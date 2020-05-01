#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PARCIAL 2 - PROBLEMA 3
Minimizar el tiempo de ruta asignada a un domociliario.

Nota: 
    este modelo es para DOS domiciliarios, porque no se como
    agregar constraints de forma dinamica :)

Sebastian Garcia 201630047

* Basado en el ejemplo 
* ejCaminoMinimoCostoGraficaResultados.py
* desarrollado por German  
"""

from __future__ import division
from pyomo.environ import *
from pyomo.opt import SolverFactory
import sys
import os
import math
import matplotlib.pyplot as plt
import numpy as np
from ast import literal_eval
import re

plt.style.use('ggplot')

# ==============
# MODELO
# ==============
Model = ConcreteModel()

# ==============
# SETS
# ==============

# nodo origen y destino para domiciliario 1
_S_A = 1
_D_A = 3

# nodo origen y destino para domiciliario 2
_S_B = 4
_D_B = 6

# cantidad de nodos
numNodes = 6
N = RangeSet(1, numNodes)

# radio de comunicacion determina si un nodo x se puede comunicar con un nodo y
RC = 25

# coordenadas
coorX = [10, 30, 50, 30, 50, 70]
coorY = [50, 60, 60, 40, 40, 50]

# para usar coordenadas desde un input
# =============================================================================
# coors = input('''
# Ingrese las coordenadas (X,Y) de cada parada, separadas por un espacio.
# Ejemplo: (10,50) (30,60) (50,60) (30,40) (50,40) (70,50)\n
# ''')
# _coors = literal_eval(
#     re.sub('(\))(\s+)(\()', '\g<1>,\g<3>', coors))  # as array
# 
# for x in range(len(_coors)):
#     coorX[x] = _coors[x][0]
#     coorY[x] = _coors[x][1]
# =============================================================================
# end coords desde un input


# ==============
# PARAMETERS
# ==============

# distancia entre nodos
dist = 999 * np.ones((numNodes, numNodes))


# ==============
# PLOT NODOS INICIALES
# ==============
fig1 = plt.figure(1)
for cont in range(len(coorX)):
    x = coorX[cont]
    y = coorY[cont]

    plt.plot(x, y, 'ro')
    plt.text(x - 2, y + 1, str(cont+1), rotation=0, size=12, weight='bold')
# end


# ==============
# PLOT CAMINOS POSIBLES
# ==============
for i in range(len(coorX)):
    for j in range(len(coorY)):
        if i != j:
            dij = math.sqrt((coorX[i]-coorX[j]) ** 2 +
                            (coorY[i]-coorY[j]) ** 2)
            if dij <= RC:
                dist[i][j] = dij
                plt.plot([coorX[i], coorX[j]], [coorY[i], coorY[j]], 'w--')
# end


# ==============
# VARIABLES
# ==============

# camino para el domiciliario 1
Model.x = Var(N, N, domain=Binary)

# camino para el domiciliario 2
Model.y = Var(N, N, domain=Binary)

# cost == tiempo
Model.cost = Param(N, N, mutable=True)

# registro de distancias en el modelo
_i = 0
for i in N:
    _j = 0
    for j in N:
        Model.cost[i, j] = dist[_i][_j]
        _j = _j + 1
    _i = _i + 1
# end


# ==============
# OBJECTIVE FUNCTION
# ==============
Model.OBJ = Objective(expr=(
    sum(Model.x[i, j] * Model.cost[i, j] for i in N for j in N) +
    sum(Model.y[i, j] * Model.cost[i, j] for i in N for j in N)
),
    sense=minimize)


# ==============
# CONSTRAINTS
# ==============

def source_rule(Model, i):
    if i == _S_A:
        return sum(Model.x[i, j] for j in N) == 1
    if i == _S_B:
        return sum(Model.y[i, j] for j in N) == 1
    else:
        return Constraint.Skip


def destination_rule(Model, j):
    if j == _D_A:
        return sum(Model.x[i, j] for i in N) == 1
    if j == _D_B:
        return sum(Model.y[i, j] for i in N) == 1
    else:
        return Constraint.Skip


def intermediate_rule(Model, i):
    if i != _S_A and i != _D_A:
        return sum(Model.x[i, j] for j in N) - sum(Model.x[j, i] for j in N) == 0
    if i != _S_B and i != _D_B:
        return sum(Model.y[i, j] for j in N) - sum(Model.y[j, i] for j in N) == 0
    else:
        return Constraint.Skip


def notRepLinkRule(Model, i, j):
    return Model.x[i, j] + Model.x[j, i] <= 1


Model.source = Constraint(N, rule=source_rule)
Model.destination = Constraint(N, rule=destination_rule)
Model.intermediate = Constraint(N, rule=intermediate_rule)
Model.notRepLink = Constraint(N, N, rule=notRepLinkRule)


# ==============
# SOLVER
# ==============
SolverFactory('glpk').solve(Model)

# Model.display()


# ==============
# PLOT CAMINOS RESULTADOS
# ==============

print('''\n
-------------------------
      RESULTADOS
-------------------------\n

* Domiciliario 1 = CAMINO AZUL
* Domiciliario 2 = CAMINO VERDE
      ''')

for x in range(len(coorX)):
    for y in range(len(coorY)):
        if Model.x[x + 1, y + 1].value == 1:
            plt.plot([coorX[x], coorX[y]], [coorY[x], coorY[y]], 'b--')

        if Model.y[x + 1, y + 1].value == 1:
            plt.plot([coorX[x], coorX[y]], [coorY[x], coorY[y]], 'g--')
# end
