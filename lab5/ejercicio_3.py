#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LABORATORIO 5 - EJERCICIO 3
Cassettes con multiples resticciones

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


lados = 2
canciones = 8

L = RangeSet(1, lados)
C = RangeSet(1, canciones)


# ==============
# PARAMETERS
# ==============

# duracion por cacion
Model.duracion = Param(C, mutable=True)
Model.duracion[1] = 4
Model.duracion[2] = 5
Model.duracion[3] = 3
Model.duracion[4] = 2
Model.duracion[5] = 4
Model.duracion[6] = 3
Model.duracion[7] = 5
Model.duracion[8] = 4


# tipo de cancion
tipo = {
        1: 'blues',
        2: 'rock',
        3: 'blues',
        4: 'rock',
        5: 'blues',
        6: 'rock',
        7: 'na',
        8: 'br' # blues & rock
        }




# ==============
# VARIABLES
# ==============

# modelo de decision LADO, CANCION
Model.x = Var(L, C, domain = Binary )


# ==============
# OBJECTIVE FUNCTION
# ==============


Model.OBJ = Objective(expr = 
                      sum( Model.x[i, j] for i in L for j in C ),
                      sense = minimize)

# ==============
# CONSTRAINTS
# ==============


# Cada lado debe tener exactamente 2 canciones de Blues.
def blues_por_lado(Model, l):
    return sum( Model.x[l, c] for l in L for c in C if tipo.get(c) == 'blues') == 4
Model.blues_por_lado=Constraint(L, rule = blues_por_lado)


# El lado A debe tener al menos 3 canciones tipo Rock and Roll
def lado_a_tres_rock(Model, l):
    if l == 1:
        return sum( Model.x[l, c] for c in C if tipo.get(c) == 'rock' or tipo.get(c) == 'br' ) >= 3
    else:
        return Constraint.Skip
Model.lado_a_tres_rock=Constraint(L, rule = lado_a_tres_rock)


# Si la canción 1 está en el lado A, la canción 5 no debe estar en el lado A.
def lado_a_uno_no_cinco(Model, l):
    if l == 1:
        return Model.x[l, 1] + Model.x[l, 5] <= 1
    else:
        return Constraint.Skip
Model.lado_a_uno_no_cinco=Constraint(L, rule = lado_a_uno_no_cinco)


# Si la canción 2 y 4 están en el lado A, entonces la canción 1 debe estar en el lado B
def lado_b_uno(Model, l):
    if l == 1:
        return (Model.x[l, 2] + Model.x[l, 2] >= 2) 
    else:
        return Constraint.Skip
Model.lado_b_uno=Constraint(L, rule = lado_b_uno)


# Duracion entre 14 y 16 minutos
def _duracion(Model, l):
    if l == 1:
        return sum( Model.x[l, c] * Model.duracion[c] for c in C ) >= 14
    elif l == 2:
        return sum( Model.x[l, c] * Model.duracion[c] for c in C ) >= 14
    else:
        return Constraint.Skip
Model._duracion=Constraint(L, rule = _duracion)

# Duracion entre 14 y 16 minutos
def _duracion_(Model, l):
    if l == 1:
        return sum( Model.x[l, c] * Model.duracion[c] for c in C ) <= 16
    elif l == 2:
        return sum( Model.x[l, c] * Model.duracion[c] for c in C ) <= 16
    else:
        return Constraint.Skip
Model._duracion_=Constraint(L, rule = _duracion_)

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


d = {
     1: 4,
     2: 5,
     3: 3,
     4: 2,
     5: 4,
     6: 3,
     7: 5,
     8: 4
     }
for l in L:
    for c in C:
        if Model.x[l, c] != 0:
            lado = 'A' if l == 1 else 'B'
            print(f"Lado {lado} -> Cancion {c} - {tipo.get(c)} - {d.get(c)} min")
















