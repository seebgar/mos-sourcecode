#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PARCIAL 2 - PROBLEMA 2
Cuatro Nadadores, minimizar tiempos totales

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
_nadadores = 6
N = RangeSet(1, _nadadores)

_estilos = 4
E = RangeSet(1, _estilos)


# ==============
# PARAMETERS
# ==============

# tiempo que tarda cada nadador [fila] por estilo [columna]
cost = [
    # espalda pecho mariposa libre
    [85, 78, 82, 84],  # nadador 1
    [88, 77, 81, 84],  # nadador 2
    [87, 77, 82, 86],  # nadador 3
    [82, 76, 80, 83],  # nadador 4
    [89, 79, 83, 84],  # nadador 5
    [86, 78, 81, 85]  # nadador 6
]

Model.cost = Param(N, E, mutable=True)

_i = 0
for nadador in range(1, _nadadores + 1):
    _j = 0
    for estilo in range(1, _estilos + 1):
        Model.cost[nadador, estilo] = cost[_i][_j]
        _j = _j + 1
    _i = _i + 1

# ==============
# VARIABLES
# ==============

# seleccionar o no a un nadador
Model.x = Var(N, E, domain=Binary)

# ==============
# OBJECTIVE FUNCTION
# ==============
Model.OBJ = Objective(expr=sum(Model.x[n, e] * Model.cost[n, e]
                               for n in N for e in E),
                      sense=minimize)

# ==============
# CONSTRAINTS
# ==============

# solo 4 nadadores


def limite(Model):
    return sum(Model.x[n, e] for n in N for e in E) == 4


Model.limite = Constraint(rule=limite)

# todos los tipos de nados deben ser cubiertos por un nadador


def profesionales(Model, n):
    return sum(Model.x[n, e] for e in E) <= 1


Model.profesionales = Constraint(N, rule=profesionales)

# un nadador seleccionado solo se desempena en un unico tipo de nado


def unicos(Model, e):
    return sum(Model.x[n, e] for n in N) == 1


Model.nadador_por_estilo = Constraint(E, rule=unicos)


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

_nombre_estilo = {
    1: "Espalda",
    2: "Pecho",
    3: "Mariposa",
    4: "Libre"
}

for n in N:
    _choosen = False
    _estilo = ""
    for e in E:
        if Model.x[n, e].value >= 1.0:
            _choosen = True
            _estilo = _nombre_estilo.get(e)
    if _choosen:
        print(f'Nadador {n} - Estilo {_estilo} ')
