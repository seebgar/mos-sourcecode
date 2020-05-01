** Ejercicio No. 3 - Parcial II MOS
** Jose Robinson Pacheco Gomez
** 201616338

set i Nodos /n1*n6/;
alias (i,j);

** Se calculo la distancia con base al modelo presentado
** en el enunciado

table c(i,j) Tabla de Conexion para los Nodos
          n1   n2   n3   n4   n5   n6
 n1       99   22   99   20   99   99
 n2       22   99   20   20   99   99
 n3       99   20   99   99   20   22
 n4       22   20   99   99   20   99
 n5       99   99   20   20   99   22
 n6       99   99   22   99   22   99;

Variables
z            Funcion Objetivo
x(i,j)       Domiciliario I
y(i,j)       Domiciliario II;

Binary Variables x,y;



Equations

funcionObjetivo          Funcion Objetivo

nodoFuenteX(i)           Nodo fuente del repartidor uno
nodoDestinoX(j)          Nodo de destino del repartidor uno
nodoIntermedioX          Nodo intermedio del repartidor uno

nodoFuenteY(i)           Nodo fuente del repartidor dos
nodoDestinoY(j)          Nodo de destino del repartidor dos
nodoIntermedioY          Nodo intermedio del repartido dos;


funcionObjetivo                     .. z=e=sum((i,j), c(i,j)*x(i,j)) + sum((i,j), c(i,j)*y(i,j));


nodoFuenteX(i)$(ord(i)=1)                                .. sum((j), x(i,j)) =e= 1;
nodoDestinoX(j)$(ord(j)=3)                               .. sum((i), x(i,j)) =e= 1;
nodoIntermedioX(i)$(ord(i) <> 1 and ord(i) ne 3)         .. sum((j), x(i,j)) - sum((j), x(j,i)) =e=0;


nodoFuenteY(i)$(ord(i)=4)                                .. sum((j), y(i,j)) =e= 1;
nodoDestinoY(j)$(ord(j)=6)                               .. sum((i), y(i,j)) =e= 1;
nodoIntermedioY(i)$(ord(i) <> 4 and ord(i) ne 6)         .. sum((j), y(i,j)) - sum((j), y(j,i)) =e=0;


Model Modelo1 /all/;
option mip = CPLEX
Solve Modelo1 using mip minimizing z;


Display z.l;
Display x.l;
Display y.l;