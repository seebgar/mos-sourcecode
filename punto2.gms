*************************************************************************
***      Problema de los Nadadores                                    ***
***                                                                   ***
***         Plantilla Examen 2                                       ***
***** Mateo Saravia Salamanca  - 201629885                                     ***                                           ***
*************************************************************************
set i estilos /e1*e4/;

set j nadadores /n1*n6/;


table tiempos(i,j) tiempo de cada nadador por cada estilo
         n1      n2      n3      n4      n5      n6
e1       85      88      87      82      89      86
e2       78      77      77      76      79      78
e3       82      81      82      80      83      81
e4       84      84      86      83      84      85
;


Variables
  x(i,j)      si escojo o no el nadador
  z       minimizar_maximizar ;

Binary Variable x;



Equations 
Fun_Obj                  Funcion Objetivo

restr1(j)                  Un ejercicio solo puede estar cubierto por un nadador

restr2                  Solo pueden haber 4 nadadores

restrN(i)                  un nadador solo puede hacer un ejercicio
;



Fun_Obj                  ..      z =e= sum((i,j), x(i,j) * tiempos(i,j));

restr1(j)                  ..      sum((i), x(i, j)) =l= 1;

restr2                  ..      sum((i, j), x(i, j)) =e= 4;
restrN(i)                  ..      sum((j), x(i, j)) =e= 1;;





Model Modelo1 /all/ ;


option mip=CPLEX

Solve Modelo1 using mip minimizing z;

Display z.l;

Display x.l;

