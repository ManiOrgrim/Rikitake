# RIKITAKE


Rikitake is a Python command line interface (CLI) software that:
- Integrates the Rikitake Dynamo differential equation system with a Runge-Kutta
4<sup>th</sup> order algorithm with user-specified parameters and initial conditions, 
generating machine-readable solutions; 
- Estimates the greatest Lyapunov exponent of the obtained solution; 
- Generates plots with informations about the dynamics of the system;

Each of these tasks can be performed separately, 
allowing the user to run the program with more flexibility.



# Introduction: The Rikitake dynamo 

The Rikitake Geodynamo is a model proposed by Tsuneji Rikitake in his paper 
["Oscillations of a system of disk dynamos" in 1958](https://www.cambridge.org/core/journals/mathematical-proceedings-of-the-cambridge-philosophical-society/article/oscillations-of-a-system-of-disk-dynamos/CDDB16F7655910A13D299B1325A3239B) 
in order to describe and quantify Earth's magnetic field oscillation. 
The model consists in a linear system of three differential equations of three time
 dependant functions *x<sub>1<sub/>*, *x<sub>2<sub/>* and *y<sub>1<sub/>* 
 and two parameters *μ* and *k*. 
 Exaustive theoretical explaination about Rikitake dynamo can be found in the 
 [supplementary material](https://www.youtube.com/watch?v=dQw4w9WgXcQ&app=desktop) 
 or in chapter 14 of ["Fractals and Chaos in Geology and Geophysics" by D. L. Turcotte](https://www.cambridge.org/it/academic/subjects/earth-and-environmental-science/solid-earth-geophysics/fractals-and-chaos-geology-and-geophysics-2nd-edition?format=PB). 
 Within this guide, the basic notions about the system, 
 as well as about dynamic systems, will be considered known and will not be 
 explained. 



# Getting started: download and installation


You can get Rikitake [here](https://github.com/ManiOrgrim/Rikitake). 
Downloaded the .zip file, extract it and you should be able to find the *rikitake* 
folder in it. You can also directly clone the git repository.
In order to install and run Rikitake, you need Python v3 ([here](https://www.python.org/)) 
and pip3 ([here](https://pypi.org/project/pip/)).
From your command line, run the command

~~~
pip3 install -e path/to/rikitake
~~~

where *path/to/rikitake* should be replaced with the actual path of the 
*rikitake* folder in your local machine.
 When installation is complete, you can run Rikitake from any folder right
 from your command line, just by running the command:

~~~
rikitake
~~~

If installation was successfull, Rikitake should run properly. 
In order to uninstall rikitake, from your command line run the command
~~~
pip3 uninstall rikitake
~~~
You will be asked confirmation before pip proceeds in the uninstallation. Confirm and Rikitake will be correctly uninstalled.


**NOTE:** When you uninstall Rikitake, all the files that it has created will **not** be deleted.







# How Rikitake works

The Rikitake routine can be summarized in 4 steps:
1. Input creation and/or reading;
2. Integration;
3. Estimate of the greatest Lyapunov exponent;
4. Image generation;


## Input reading and creation

There are two ways the user can specify the desired inputs to Rikitake: we can 
call them *in-run* and *out-run*. 
As first step, Rikitake will search for a 
file called *input_values.txt* within the current wrking directory. 
If this file does't exist, the in-run input procedure will automatically start. 
If such file exists,
Rikitake will ask the user 
~~~
Do you want to create a new 'input_values.txt' file? (y/n)
~~~
 via standard output. Answer accordingly as you wish, 
 tying `y` ("yes") if you wish to create a new input file or `n` ("no") otherwise.
 If the answer is `y`  the in-run input procedure will start,
otherwise the out-run input procedure will be performed. 

### In-run input 
Rikitake will ask the user 
~~~
Type the data in the form 'mu k N_steps x1_0 x2_0 y1_0 simulation_identifier'

~~~
via stanard output. The user will then enter the parameters they wish. These are:
- `mu`	 (*float*)	value of the *μ* parameter;
- `k`	(*float*)	value of the *k* parameter;
- `N_steps` (*int*)	number of integration steps you wish to perform;
- `x1_0`	(*float*)	value of the initial state for function *x<sub>1<sub/>*;
- `x2_0`	(*float*)	value of the initial state for function *x<sub>2<sub/>*;
- `y1_0`	(*float*)	value of the initial state for function *y<sub>1<sub/>*;
- `sim_ID` (*string*)	identifying string for the simulation.


The answer should be given writing all the values separated by a space ' ' 
character. 
*N_steps* determines for how many time steps the integration will be performed.
 The default time step is *dt*=1/256=0.00390625 (arbitrary time units), 
 if not specified by the user [see here](#switches).
 This means that the simultation will run until a time value `t=dt * N_steps`, 
 generating *N_steps* points as solution. As *N_steps* grows, 
 the lyapunov exponent estimate approaches  to the real value, 
 but it will take more computation time. 
 
 
*SimID* functions as a "name" for the simulation: 
every file that Rikitake will generate will have this string as initial characters.

With these inputs Rikitake will create a file called *input_values.txt* 
in the save directory. 
For more informations about these file see the 
[dedicated section](#Input-file-layout).


**Note**: if an "input_values.txt" already exists in the save directory, 
this procedure will overwrite it. 
In this case, Rikitake will always warn the user and ask for 
more confirmations before proceeding.


**Note**: if you run two different simulations with the same *Sim_ID*, 
the output of the former one will be overwritten, so be careful!


### Creation of the input file
 With these inputs Rikitake will create the two initial conditions for the system. The first one,
that from now on will be referred to as _unperturbed state_, 
is given by the triplet (x1_0, x2_0, y1_0). The second one,
that from now on will be referred to as _perturbed state_, 
is obtained from the perturbed one with a procedure descripted in the
[supplementary material](https://www.youtube.com/watch?v=dQw4w9WgXcQ&app=desktop). 


#### Input file layout 
The input file is a two-lines text file with the following layout:
~~~
μ	k 	N_steps		x1_0u	x2_0u	y1_0u SimID
μ	k 	N_steps		x1_0p	x2_0p	y1_0p SimID
~~~
Where *μ* (float) and *k* (float) are the parameters of the simulation, 
*N_steps* (integer) is the number of integration steps and 
*Sim_ID* (string) is the simulation identifier, that is the name that 
Rikitake will use to store and identify the outputs. 
These values must be equal between the two lines, otherwise Rikitake will end 
right after completing the integration (with exit
value 6, see [here](#Errors-and-exit-codes). 
The *x1_0u*,	*x2_0u*,	*y1_0u* (floats) are the initial states 
for the unperturbed state; *x1_0p*,	*x2_0p*,	*y1_0p* (floats) 
are the initial states for the perturbed
states. These triplets *should* be different, in order for the simulation to be
 meaningful. If the two initial states are equal Rikitake will not stop but it 
 won't be able to calculate Lyapunov exponents (output Lyapunov exponent will be -∞).
The user is free write its own *input_values.txt* file 
(a basic text editor is sufficient) and Rikitake will work perfectly, 
given the file follows the right layout.
**Note**: this file is explicitly searched by Rikitake with the exact name 
*input_values.txt*. Any other name will make the file invisible to the program.


### Out-run input 
Rikitake will read the existing *input_values.txt* file in the save directory 
and will start with the actual simulation. 
In this way the user is able to perform desired modifications to a 
previously-generated *input_values.txt* file. 
The user is also free to fully write its own input file 
(until it follows the [correct layout](#Input-file-layout)). 


## Integration

In this step, Rikitake reads the *input_values.txt* file.
Rikitake reads the first line, extracts the informations about the system and 
makes a Runge-Kutta 4th-order integration (see 
[supplementary material](https://www.youtube.com/watch?v=dQw4w9WgXcQ&app=desktop)
 for details about the precise algorithm).
 *N_Steps* integration steps are performed. 
The results are saved in .csv format, in a file named *SimID_0.csv*
 (where the string *SimID* will be replaced by the simulation identifier 
 given in input).
The same is done reading the second line of *input_values.txt* creating a file 
named
 *SimID_1.csv*. 
 More information about the structure of this output files [here](#The-outputs).

## Lyapunov exponents estimate

In this step, Rikitake reads the results of the two simulations
 and estimates the greatest Lyapunov exponent from these 
 (the calculation procedure is rather complex and will be omitted here. 
 You can find it in the [supplementary material](https://www.youtube.com/watch?v=dQw4w9WgXcQ&app=desktop)). 
Rikitake calculates the estimated Lyapunov exponent for _each_ timestep of the 
integration, thus creating a time series of estimated Lyapunov exponents. 
Given the asymptotical definition of the Lyapunov exponents, 
the last values are supposed to be the most meaningful, 
so Rikitake will calculate the mean of the last 100
values. This mean value will be stored in a file named *SimIDlyap.dat*. 
The time-series of the Lyapunov exponents will be plotted and saved as an image
 named 
*SimID_lyap_exp.png*

## Image generation

As final step, Rikitake creates 12 plots, 6 for each integration. The plots made 
for each integration are 
1. A 3-dimensional plot of the trajectory of the system in the phase-space
2. A projection of the trajectory in the *x<sub>1<sub/>* *x<sub>2<sub/>* plane
3. A projection of the trajectory in the *x<sub>1<sub/>* *y<sub>1<sub/>* plane
4. A projection of the trajectory in the *x<sub>2<sub/>* *y<sub>1<sub/>* plane
5. A *x<sub>1<sub/>* vs *time* plot
6. A *x<sub>2<sub/>* vs *time* plot

The file format is png. The file  naming follows the structure "SimID_"+"simulation number_"+"plot subject", 
where simulation number is 0 for the unperturbed solution, 1 for the perturbed solution.

Once image generation is complete, the simulation is over. Rikitake will ask the user if he wishes to perform another simulation.
If the answer is *yes*, Rikitake will start again from the 
[input reading and creation](#Input-reading-and-creation) step, 
otherwise it will shut down
with exit value 0 ( [more about exit values](#Errors-and-exit-codes)).

# The outputs

Rikitake will create 17 files 
(16 proper output files plus the  *input_values.txt* file).
 Each of them will be explained here. In all of these file names 
'SimID' will be replaced with the simulation ID you gave Rikitake. 
Files labeled with '0' refer to the unperturbed 
solution and files labeled with '1' refer to the perturbed solution.
1. SimID_0.csv
2. SimID_1.csv

Two *.csv* files that store the results of the integration, one for each state. 
The first line records the values of parameters *µ* and *k*.
 The second line is a header reporting the column structure. 
 From the third line on, the integration results are stored in the format
~~~
time;x_1;x_2;y_1;y_2
~~~


3. SimID_0_3Dplot.png
4. SimID_1_3Dplot.png

Two *.png* images showing the 3D plot of the trajectory of the solutions in the 
*x<sub>1<sub/>* *x<sub>2<sub/>* *y<sub>1<sub/>* space. 


5. SimID_0_X1time.png
6. SimID_1_X1time.png


Two *.png* images showing the *x<sub>1<sub/>* vs *time* plot for the solutions.


7. SimID_0_X2time.png
8. SimID_1_X2time.png


Two *.png* images showing the *x<sub>2<sub/>* vs *time* plot for the solutions.


9. SimID_0_X1X2.png
10. SimID_1_X1X2.png


Two *.png* images showing the projection of the trajectory in the 
*x<sub>1<sub/>* *x<sub>2<sub/>* plane.


11. SimID_0_X1Y1.png
12. SimID_1_X1Y1.png


Two *.png* images showing the projection of the trajectory in the 
*x<sub>1<sub/>* *y<sub>1<sub/>* plane.


13. SimID_0_X2Y1.png
14. SimID_1_X2Y1.png


Two *.png* images showing the projection of the trajectory in the 
*x<sub>2<sub/>* *y<sub>1<sub/>* plane.


15. SimIDlyap.dat


A *.dat* file storing the value of the estimated greatest lyapunov exponent of the 
system. This value is the mean of the last 100 Lyapunov exponents calculated.


16. SimID_lyap_exp.png


A *.png* image showing the *lyapunov exponent estimate* vs *time* plot.


# Switches

Rikitake accepts several switches. These commands can be given right from 
command line when calling the program.
- **Suppress images** command: `--NOimg`. 

Suppress all image generation, except for the Lyapunov exponent plot. 


- **Suppress integration** command: `--NOint`. 

Suppress the integration. Use this switch only 
if you already have the integration results, as the rest of the code relies upon them.

- **Suppress Lyapunov exponent estimate** command: `--NOly`. 


Suppress the Lyapunov exponent estimate. The Lyapunov exponent plot will also not be produced.

- **Turn on the alarm** command: `-a`, `--alarm`. 

Rikitake will produce an acustic signal when 
the process is completed. The sound is very annoying, so handle with care.

-  **Specify save directory** command: `--save-dir <path/to/dir>`

 Specify the directory
in which the results will be saved. *path/to/dir* has to be replace with the
 actual path of the save directory.
Default is current working directory.


- **Set time step** command: `--set-dt <VALUE>`

 Specify the time step for the integration. Replace
*VALUE* in the command with the desired value (it must be a number). 
Default value is 2^-8.


- **Verbose mode** command: `-v`, `--verbose`. 

Rikitake will inform the user with more outputs
in the standard output. Right now (v2.0.0) this flag doesn't really add much, 
but more will be implemented in the future. 




# Errors and exit codes
====================
When Rikitake terminates, wether it may be beacause the routine is over
or errors have been arised, returns an exit code, that is a number associated with 
a certain error in order to inform the user what happened. These exit codes are:
0. Rikitake ran succesfully without problems.
1. **Integration results could not be opened**. The files are missing or 
the user has not reading permissions. This may happen if the user uses the `--NOint`
flag without a prior integration.
2. **"input_values.txt" could not be opened**. This error happens wheter if the file has been deleted or if the user has not reading permissions.
3. **".temp_for_create_infiles.txt" file could not be opened**. '.temp_for_create_infiles.txt' is a temporary
file that in which Rikitake holds some useful in-run informations, and deletes it
 when the run is over.
This error happens wheter if the file has been deleted or if the user has not reading permissions.
4. **".temp_for_create_infiles.txt" is not written as expected**. Given that this file is directly created by Rikitake,
is very hard for this error to be raised.
5. **"input_values.txt" is not written as expected**. This happens when the layout of the file 
doen't respect the indications in [here](#Input-file-layout).
 Check if the two lines of the file have the same values (except 
for the initial conditions).
6. **Integration results are not written as expected**. In particular, the two result files
may have different values of *μ*, *k* or a different number of integration steps. This happens
if user-given integration results don't follow the proper layout.

**WARNINGS**: along with errors, Rikitake is provided with warnings for the user. 
These warnings will not stop Rikitake, and it may run flawlessly. 
These are usually due to the presence of unrecommended input values:
- *N_steps* < 20000 : This low number of integration steps could lead 
to the non-convergence of the Lyapunov exponent.
-  *μ* is not in the recommendend range of values, that is 0< μ< 10^2. This may cause
overflow or undeflow issues during integration. 
- *k* is not in the recommendend range of values, that is 10^(-2)< *k*< 10^(2). This may cause
overflow or undeflow issues during integration. 
- Sim_ID containing '.' character . This causes issues when the images are saved, 
cropping the SimID in
the file names (e.g. if the SimID is "abc.def", images will be saved as if the Sim_ID was only
"abc").


# Example usage

We want to use Rikitake to estimate the Lyapunov exponents of Rikitake geodynamo
with parameters *μ*=10, *k*= 2 and unperturbed initial conditions (1,1,1).
We want to perform 100000 integration steps. We choose "foo" as SimID.
Run Rikitake form command line:
~~~
rikitake
~~~
If a "input_values.txt" file already exists in the working directory the user 
will be asked (twice) if they still wish to create a new input file and overwrite the previous one.
If no such file already exists or if we answered 'yes' to the previous questions, 
Rikitake will ask us for the input data. Type in the command line:
~~~
10 2 100000 1 1 1 foo
~~~
Press enter and let Rikitake do its job. Once all the steps are completed, 
Rikitake will ask if the user wishes tu run another simulation. Answer as you wish.
We now have all the output files in our directory. In particular the file foolyap.dat contains the value
of the estimate of the Lyapunov exponent, that is, in our case, -0.2194168146332044.

**This is all you need to know** in order to make Rikitake work. If you have any feedback or suggestion
don't hesitate to contact me!
Thanks for reading and have fun with Rikitake!