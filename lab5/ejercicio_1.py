#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LABORATORIO 5 - EJERCICIO 1
Minimizar el número de trabajadores de tiempo completo
considerando la cantidad de trabajadores requeridos por cada día de la semana

Sebastian Garcia 201630047
Nicolas Sotelo 201623026
"""


from __future__ import division
from pyomo.environ import *
from pyomo.opt import SolverFactory
from math import pow

# ==============
# MODEL
# ==============
Model = ConcreteModel()

# ==============
# SETS
# ============== 


days = 7
D = RangeSet(1, days)


# ==============
# PARAMETERS
# ==============

workers = {
        1: 17,
        2: 13,
        3: 15,
        4: 19,
        5: 14,
        6: 16,
        7: 11
        }

# ==============
# VARIABLES
# ==============


Model.x = Var(D, domain = NonNegativeIntegers )


# ==============
# OBJECTIVE FUNCTION
# ==============


Model.OBJ = Objective(expr = 
                      sum( Model.x[d] for d in D ),
                      sense = minimize)


# ==============
# CONSTRAINTS
# ==============


def labour(Model, i):
    if i is 1:
        return Model.x[1] + Model.x[5] + Model.x[4] + Model.x[6] + Model.x[7] >= workers.get(1)
    elif i is 2:
        return Model.x[2] + Model.x[6] + Model.x[5] + Model.x[7] + Model.x[1] >= workers.get(2)
    elif i is 3:
        return Model.x[3] + Model.x[7] + Model.x[6] + Model.x[1] + Model.x[2] >= workers.get(3)
    elif i is 4:
        return Model.x[4] + Model.x[1] + Model.x[7] + Model.x[2] + Model.x[3] >= workers.get(4)
    elif i is 5:
        return Model.x[5] + Model.x[2] + Model.x[1] + Model.x[3] + Model.x[4] >= workers.get(5)
    elif i is 6:
        return Model.x[6] + Model.x[3] + Model.x[2] + Model.x[4] + Model.x[5] >= workers.get(6)
    elif i is 7:
        return Model.x[7] + Model.x[4] + Model.x[3] + Model.x[5] + Model.x[6] >= workers.get(7)
    else:
        return Constraint.Skip

Model.labour=Constraint(D, rule = labour)




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

total = 0
for n in D:
    val = "{:.2f}".format(Model.x[n].value)
    total += Model.x[n].value
    print(f'Dia {n} - Trabajan: {val}')
    
print(f"\nTotal Trabajadores: {total}")
















