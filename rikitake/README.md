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



#Getting started: download and installation
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
How Rikitake works
============
The Rikitake routine can be summarized in 4 steps:
1. Input creation and/or reading
2. Integration
3. Estimate of the greatest Lyapunov exponent
4. Image generation

From your terminal, get in the directory you want Rikitake to operate, and run the command
'rikitake'. Then Rikitake should run and the user will be asked for inputs.

##Input reading and creation
There are two ways the user can specify the desired inputs to Rikitake: in-run and out-run. As first step, Rikitake will search for a 
file called "input_values.txt" within the current wrking directory. If this file does't exist, the in-run input procedure will automatically start. If such file exists,
the user will be asked "Do you want to create a new 'input_values.txt' file? (y/n)" via command line. If the answer is "y" ("yes") the in-run input procedure will be used,
otherwise the out-run input procedure will be performed. 

**In-run input ** 
Rikitake will ask the user "Type the data in the form 'mu k N_steps x1_0 x2_0 y1_0 simulation_identifier':". The user will then enter the parameters they wish. These are.
'mu'	(float)	value of the *μ* parameter
'k'	(float)	value of the *k* parameter
'N_steps' (int)	number of integration steps you wish to perform 
x1_0	(float)	value of the initial state for function *x<sub>1<sub/>*
x2_0	(float)	value of the initial state for function *x<sub>2<sub/>*
y1_0	(float)	value of the initial state for function *y<sub>1<sub/>*
sim_ID (string)	identifying string for the simulation.
The answer should be given writing all the values separated by a space ' ' character. 
N_steps determines for how many time steps the integration will be performed. The default time step is *dt*=1/256=0.00390625 (arbitrary time units), if not specified by the user [see here](#errors).
 This means that the simultation will run until a time value *t*=*dt* * Nsteps, generating Nsteps points as solution. As Nsteps grows, the lyapunov exponent will converge better, but it will take more computation time. 
*simID* functions as a "name" for the simulation: every file that Rikitake will generate will have this string as initial characters.
These values have to be written in one single line, and they should be separated by a space character.
With these inputs Rikitake will create a file called "input_values.txt" in the save directory. For more informations about these files see the dedicated section.
**NOTE**: if an "input_values.txt" already exists in the save directory, this procedure will overwrite it. In this case, Rikitake will always warn the user and ask for 
more confirmations before proceeding.
**NOTE**: if you run two different simulations with the same simID, the output of the former one will be overwritten, so be careful!
**creation of the input file** With these inputs Rikitake will create the two initial conditions for the system. The first one,
that from now on will be referred to as _unperturbed state_, is given by the triplet (x1_0, x2_0, y1_0). The second one,
that from now on will be referred to as _perturbed state_, is obtained from the perturbed one with a procedure descripted **here**. 
**input file layout**
The input file is a two-lines text file with the following layout:
~~~
μ	k 	N_steps		x1_0u	x2_0u	y1_0u SimID
μ	k 	N_steps		x1_0p	x2_0p	y1_0p SimID
~~~
Where μ (float) and k (float) are the parameters of the simulation, N_steps (integer) is the number of integration steps and Sim_ID (string) is the simulation identifier, that is the name that 
Rikitake will use to store and identify the outputs. These values must be equal between the two lines, otherwise Rikitake will end right after completing the integration (with exit
value 6, see [here]). The x1_0u	x2_0u	y1_0u (floats) are the initial states for the unperturbed state, x1_0p	x2_0p	y1_0p (floats) are the initial states for the perturbed
states. These triplets *should* be different, in order for the simulation to be meaningful. In this case, Rikitake will not stop but it won't be able to calculate Lyapunov exponents.
The user is free write its own input_values.txt (a basic text editor is sufficient) and Rikitake will work, given the file follows the right layout.
**NOTE**: this file is explicitly searched by Rikitake with the name "input_values.txt". Any other name will make the file invisible to the program.


**Out-run input **
Rikitake will read the existing "input_values.txt" file in the save directory and will start with the actual simulation. 
In this way the user is able to perform desired modifications to a previously-generated input_values file. 
the user is also free to fully write its own input file (until it follows the correct layout (see previous  section to see how it's done). 


Integration
====
In this step, Rikitake reads the ''input_values.txt'' file.
Rikitake reads the first line, extracts the informations about the system and makes a Runge-Kutta 4th-order integration (see supplementary material for details about the precise algorithm).
 ''N_Steps'' integrations are performed. 
The results are saved in .csv format, in a file named ''SimID_0.csv'' (where the string ''SimID'' will be replaced by the simulation identifier given in input).
The same is done reading the second line of ''input_values.txt'' creating a file named
 ''SimID_1.csv''. More information about the structure of this output files [here](##The outputs).

Lyapunov exponents estimate
=====
In this step, Rikitake reads the results of the two simulations, and estimates the greatest Lyapunov exponent from these (the calculation procedure is rather complex and will be omitted here. You can find it in the [supplementary material](https://www.youtube.com/watch?v=dQw4w9WgXcQ&app=desktop)). 
Rikitake calcluates the estimated Lyapunov exponent for _each_ timestep of the integration, thus creating a time series of estimated Lyapunov exponents. Given the asymptotical definition of the Lyapunov exponents, the last values are supposed to be the most meaningful, so Rikitake will calculate the mean of the last 100<sup>1<sup/> 
values. This mean value will be stored in a file named "SimIDlyap.dat". The time-series of the Lyapunov exponents will be plotted and saved as an image named 
"SimID_lyap_exp.png

Image generation
====
As final step, Rikitake creates 12 plots, 6 for each integration. These plots made for each integration are: 
1. A 3-dimensional plot of the trajectory of the system in the phase-space
2. A projection of the trajectory in the *x<sub>1<sub/>* *x<sub>2<sub/>* plain
3. A projection of the trajectory in the *x<sub>1<sub/>* *y<sub>1<sub/>* plain
4. A projection of the trajectory in the *x<sub>2<sub/>* *y<sub>1<sub/>* plain
5. A *x<sub>1<sub/>* vs *time* plot
6. A *x<sub>2<sub/>* vs *time* plot

The file format is png. The file  naming follows the structure "SimID_"+"simulation number_"+"plot subject", 
where simulation number is 0 for the unperturbed solution, 1 for the perturbed solution.

Once image generation is complete, the simulation is over. Rikitake will ask the user if he wishes to perform another simulation.
If the answer is 'yes', Rikitake will start again from the **input reading and creation** step, otherwise it will shut down
with exit value 0.

The outputs
=====
Rikitake will create 16 files (17 counting the eventual 'input_values.txt' file).
 Each of them will be explained here. In all of these file names 
'SimID' will be replaced with the simulation ID you gave Rikitake. The files labeled with '0' refer to the unperturbed 
solution and the file labeled with '1' refer to the perturbed solution.
1. SimID_0.csv
2. SimID_1.csv
Two .csv files that store the results of the integration, one for each state. 
The first line records the values of *µ* and *k* of the integration.
 The second line is a header reporting the column structure. 
 From the third line on, the integration results are stored in the format
~~~
time;x_1;x_2;y_1;y_2
~~~
3. SimID_0_3Dplot.png
4. SimID_1_3Dplot.png
Two png images showing the 3D plot of the trajectory of the solutions in the 
*x<sub>1<sub/>* *x<sub>2<sub/>**y<sub>1<sub/>* space. 
5. SimID_0_X1time.png
6. SimID_0_X1time.png
Two png images showing the *x<sub>1<sub/>* vs *time* plot for the solutions.
7. SimID_0_X2time.png
8. SimID_0_X2time.png
Two png images showing the *x<sub>2<sub/>* vs *time* plot for the solutions.



gg
=========

Within this step, Rikitake reads the input the user gave and creates some addition files that will help it run. 
Let us assume the input is
'
3 4 1000000 1 2 3 foo
'
that is: 
the parameters of this simulation are *µ*=3, *k*=4. We will perform 1000000 integration steps. The initial state is given by *x<sub>1<sub/>*=1, *x<sub>2<sub/>*=2, *y<sub>1<sub/>*=3. The simulation identifier is 'foo'.
First, Rikitake will generate an initial condition adjacent to the given initial condition. This initial condition is found by: 
1. calculating the Jacobian matrix of the system 
2. finding the eigenvector *v* relative to the greatest eigenvalue of the Jacobian
3. displacing the initial condition by a factor 2<sup>-32<sup/> along the direction given by *v*

This creates a new initial condition, slightly different from the first one.
Then, Rikitake will create a file, called 'input_values.txt'. As the name suggests, all the informations about the inputs will be stored here.
The file consists in two lines. The first one is a direct replica of the input the user gave. The second line is the same as the first one, but the initial conditions written will be the perturbed ones. So, for our example input, the 'input_values.txt' file will look like this:

~~~
3 4 100000 1.0 2.0 3.0 foo
3 4 100000 0.9999999999907341 1.999999999990734 2.9999999999352895 foo
~~~
##Integration

 
 So, in our example, we will have our integrations saved in the files "foo_0.csv" and 
 "foo_1.csv".

##Lyapunov exponents estimate




##Image generation
As final step, Rikitake creates 12 plots, 6 for each integration. These plots made for each integration are: 
1. A 3-dimensional plot of the trajectory of the system in the phase-space
2. A projection of the trajectory in the *x<sub>1<sub/>* *x<sub>2<sub/>* plain
3. A projection of the trajectory in the *x<sub>1<sub/>* *y<sub>1<sub/>* plain
4. A projection of the trajectory in the *x<sub>2<sub/>* *y<sub>1<sub/>* plain
5. A *x<sub>1<sub/>* vs *time* plot
6. A *x<sub>2<sub/>* vs *time* plot

The file format is png. These image naming follows the structure "SimID_"+"simulation number_"+"plot subject", where simulation number is 0 for the unperturbed solution, 1 for the perturbed solution. : for our example case, we will have then:
1. foo_0_3Dplot.png
2. foo_0_X1X2.png
3. foo_0_X1Y1.png
4. foo_0_Y1X2.png
5. foo_0_X1time.png
6. foo_0_X2time.png
7. foo_1_3Dplot.png
8. foo_1_X1X2.png
9. foo_1_X1Y1.png
10. foo_1_Y1X2.png
11. foo_1_X1time.png
12. foo_1_X2time.png

Below you can see the 3D phase space plot for our example case.
![plot](foo_0_3Dplot.png)




1: 100 is a totally arbitrary value. If you can suggest a more meaningful criterion, you're welcome to share it!
 
##The outputs
Rikitake will create 17 files. Each of them will be explained here. In all of these file names 
'SimID' will be replaced with the simulation ID you gave Rikitake.

0. input_values.txt

A 2-lines text file containing the input informations Rikitake needs in order to run. Then structure is 
First line refers to the unperturbed solution, second line refers to the perturbed one. 
The first two numbers represent respectively the values of the
*µ* and *k* parameters. The third value is an integer and represents 
the number of integration steps to be performed. These three initial values should be equal for both the unperturbed
and perturbed solution. The following three numbers represent the values of the initial conditions, 
in the order x_1, x_2, y_1. They should differ slightly between the two lines. The last word is the SimID, which should
be equal between the two lines.
An example of 'input_values.txt' file is 
~~~
5 10 100000 2.0 2.0 2.0 foo
5 10 100000 2.000000000029093 2.000000000029093 1.999999999988681 foo

~~~
This file can be directly given as input from the user, as can easily be written by the user. 



2. SimID_0.csv
3. SimID_1.csv
Two .csv files, with the results of the integration. The file labelled with '0' holds the results obtained integrating with the unperturbed initial condition; the file labelled with '1' holds the results obtained integrating with the perturbed initial condition.
The first line records the values of *µ* and *k* of the integration. The second line is a header reporting the column structure. From the third line on, the integration results are stored in the format

~~~
time;x_1;x_2;y_1;y_2
~~~




#Errors
====================
Describe the error codes. Describe the typical bugs (or wrong usage) one can run into.
Known issues. 


