Rikitake
========

Rikitake is a python program that integrates the Rikitake dynamo
differential equation sysytem and calculates the Lyapunov exponents of
the system using the obtained solution.

Theoretical background
======================

The Rikitake dynamo is a model that describes the geodynamo, that is the
mechanism that generate the Earth's megnetic field. It depends on four
variables $X_1, X_2, Y_1, Y_2$ and on two parameters $\mu$ and $k$. The
system of differtial equations is given by
![test](https://raw.githubusercontent.com/ManiOrgrim/Rikitake/master/gaga_2.png)
$$&\frac{dX_1}{d\tau} +\mu X_1=Y_1X_2 \\   
&\frac{dX_2}{d\tau}+\mu X_2=(Y_1 -A)X_1 \\
&\frac{dY_1}{d\tau}=1-X_1 X_2 \\
&Y_2=Y_1-A$$ where $A=\mu(k^2 -k^{-2})$.
