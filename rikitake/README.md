RIKITAKE
========

Rikitake is a Python command line interface (CLI) software able to:
- Integrate the Rikitake Dynamo differential equation system with a Runge-Kutta with user-specified parameters and initial conditions, generating machine-readable solutions 
- Estimate the greatest Lyapunov exponent of the obtained solution 
- Generate plots with informations about the dynamics of the system

Each of these tasks can be performed separately, allowing the user to run the program with more flexibility.



Introduction: The Rikitake dynamo 
===================
The Rikitake Geodynamo is a model proposed by Tsuneji Rikitake in his paper ["Oscillations of a system of disk dynamos" in 1958](https://www.cambridge.org/core/journals/mathematical-proceedings-of-the-cambridge-philosophical-society/article/oscillations-of-a-system-of-disk-dynamos/CDDB16F7655910A13D299B1325A3239B) in order to describe and quantify Earth's magnetic field oscillation. The model consists in a linear system of three differential equations of three time dependant functions *x<sub>1<sub/>*, *x<sub>2<sub/>* and *y<sub>1<sub/>* and two parameters *μ* and *k*. Exaustive theoretical explaination about Rikitake dynamo can be found in the [supplementary material](https://www.youtube.com/watch?v=dQw4w9WgXcQ&app=desktop) or in chapter 14 of ["Fractals and Chaos in Geology and Geophysics" by D. L. Turcotte](https://www.cambridge.org/it/academic/subjects/earth-and-environmental-science/solid-earth-geophysics/fractals-and-chaos-geology-and-geophysics-2nd-edition?format=PB). Within this guide, the basic notions about the system, as well as about dynamic systems, will be considered known and will not be explained. 



Getting started: download and installation
====================
**add requirements**
You can get Rikitake [here](https://github.com/ManiOrgrim/Rikitake). If you downloaded the .zip file, extract it and you should be able to find the "rikitake" folder in it. 
In order to install and run Rikitake, you need Python v3 ([here](https://www.python.org/)) and pip3 ([here](https://pypi.org/project/pip/)).
From your command line, run the command

~~~
pip3 install -e path/to/rikitake
~~~

where 'path/to/rikitake' should be replaced with the actual path of the rikitake folder in your local computer. When installation is complete, you can run Rikitake from any folder right in your command line, just by running the command:

~~~
rikitake
~~~

If installation was successfull, Rikitake should run properly.

In order to uninstall rikitake, from your command line run the command
~~~
pip3 uninstall rikitake
~~~
You will be asked confirmation before pip proceeds in the uninstallation. Confirm and Rikitake will be correctly uninstalled.
**NOTE:** When you uninstall Rikitake, all the files that it has created will -not- be deleted.


Running Rikitake: usage tutorial
====================
Here I will describe how to run the program. Remember to specify flags. Describe how the results are given. 


Errors
====================
Describe the error codes. Describe the typical bugs (or wrong usage) one can run into.
Known issues. 


