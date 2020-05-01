** Ejercicio No. 1 - Parcial II MOS
** Jose Robinson Pacheco Gomez
** 201616338

set i corriente /i1*i4/;

Parameter b(i) valorCorriente
   /i1 4,i2 6,i3 8,i4 18/;

Variables
r1 Resitencia No. 1
r2 Resitencia No. 2
r3 Resitencia No. 3
r4 Resitencia No. 4

z Variable Objetivo;



Positive Variable
r1,r2,r3,r4;

Equations
funcionObjetivo         Funcion Objetivo

restriccion1            Restriccion No.1
restriccion2            Restriccion No.2
restriccion3            Restriccion No.3
restriccion4            Restriccion No.4
restriccion5            Restriccion No.5
restriccion6            Restriccion No.6
restriccion7            Restriccion No.7
restriccion8            Restriccion No.8
restriccion9            Restriccion No.9
restriccion10           Restriccion No.10;


funcionObjetivo         .. z=e= ( sqr(b('i1'))*r1 + sqr(b('i2'))*r2 + sqr(b('i3'))*r3 + sqr(b('i4'))*r4 );

restriccion1            .. b('i1')*r1 =e= b('i2')*r2;
restriccion2            .. b('i2')*r2 =e= b('i3')*r3;
restriccion3            .. b('i1')*r1 =g= 2;
restriccion4            .. b('i1')*r1 =l= 10;
restriccion5            .. b('i2')*r2 =g= 2;
restriccion6            .. b('i2')*r2 =l= 10;
restriccion7            .. b('i3')*r3 =g= 2;
restriccion8            .. b('i3')*r3 =l= 10;
restriccion9            .. b('i4')*r4 =g= 2;
restriccion10           .. b('i4')*r4 =l= 10;



Model Modelo1 /all/;
option mip=CPLEX
Solve Modelo1 using mip minimizing z;


Display z.l;
Display r1.l;
Display r2.l;
Display r3.l;
Display r4.l;