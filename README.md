Rikitake
========

Rikitake is a python program that integrates the Rikitake dynamo
differential equation sysytem and calculates the Lyapunov exponents of
the system using the obtained solution.

The Rikitake dynamo
======================

The Rikitake dynamo is a model that describes the geodynamo, that is the
mechanism that generate the Earth's megnetic field. The first description has been made by [Rikitake (1973)](https://academic.oup.com/gji/article/35/1-3/277/615502). 
These equations depend on four variables X<sub>1</sub>, X<sub>2</sub>, Y<sub>1</sub> and Y<sub>2</sub> and on two parameters μ and k.

 More informations can be found in (D. L. Turcotte, *Fractals and chaos in geophysics*, 1992, Cambridge University press). 
![The Rikitake dynamo equations](https://github.com/ManiOrgrim/Rikitake/blob/master/Images/Rikitake_dynamo_eqs.png?raw=true)
It is a system of four non-linear coupled differential equations that may show chaotic behaviour. A measure of the chaoticity of a system is given by the Lyapunov exponents
