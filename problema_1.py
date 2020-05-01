#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PARCIAL 2 - PROBLEMA 1
Hallar las resistencias que permitan minimizar 
la potencia disipada en el circuito

Sebastian Garcia 201630047
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
_corrientes = 4
I = RangeSet(1, _corrientes)

# ==============
# PARAMETERS
# ==============
_i = { 
      1: 4, 
      2: 6, 
      3: 8, 
      4: 18
     }

# ==============
# VARIABLES
# ==============

# valor de cada resistencia
Model.x = Var(I, domain = NonNegativeReals )

# ==============
# OBJECTIVE FUNCTION
# ==============
Model.OBJ = Objective(expr = 
                      sum( Model.x[n] * pow(_i.get(n), 2) for n in I ),
                      sense = minimize)

# ==============
# CONSTRAINTS
# ==============

# V1 = V2 = V3
def igualdad_voltajes(Model, i):
    if i is 1 or i is 2:
        return _i.get(i) * Model.x[i] == _i.get(i+1) * Model.x[i+1] 
    else:
        return Constraint.Skip
Model.igualdad_voltajes=Constraint(I, rule = igualdad_voltajes)

# Limites cantidad volatje por Resistencia 
def limite_R(Model, i):
    return inequality(2, Model.x[i], 10)
Model.limite_R = Constraint(I, rule = limite_R)


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
for n in I:
    val = "{:.2f}".format(Model.x[n].value)
    print(f'Resistencia {n} = {val}')
















