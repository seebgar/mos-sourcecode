** Ejercicio No. 2 - Parcial II MOS
** Jose Robinson Pacheco Gomez
** 201616338


** Definición Tipo de Nado
set i tipoNado /tn1*tn4/;


** Definición de Nadadores
set j nadadores /nad1*nad6/;


table tiemposCandidatos(i,j) Tabla que indica que el tiempo empleado por cada nadador para cada tipo de nado
         nad1    nad2    nad3    nad4    nad5    nad6
tn1       85      88      87      82      89      86
tn2       78      77      77      76      79      78
tn3       82      81      82      80      83      81
tn4       84      84      86      83      84      85;


** El problema plantea un caso de elegir que nadadores llevar, es decir,
** es necesario crear una variable binaria para la eleccion.


Variables
  x(i,j)         Eleccion del nadador. (1) si - (0) no
  z              z;

Binary Variable x;


Equations

funcionObjetivo         Funcion Objetivo
numeroNadadores         Tienen que haber obligatoriamente 4 nadadores

nados(j)                Todos los tipos de nados deben estar cubiertos por un nadador
nadador(i)              Un nadador seleccionado solo se desempeña en un tipo de nado;



funcionObjetivo          .. z =e= sum((i,j), x(i,j) * tiemposCandidatos(i,j));
numeroNadadores          .. sum((i, j), x(i, j)) =e= 4;

nados(j)                 .. sum((i), x(i, j)) =l= 1;
nadador(i)               .. sum((j), x(i, j)) =e= 1;



Model Modelo1 /all/;
option mip=CPLEX
Solve Modelo1 using mip minimizing z;


Display z.l;
Display x.l;
