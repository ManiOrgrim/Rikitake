#include <iostream>
#include <stdlib.h>
#include <fstream>
#include <string>
#include <cmath>
using namespace std;

class dynamo {
double* x1;
double* x2;
double* y1;
double* y2;

double mi;
double A;
double k;

double dt;
int nsteps;

double k1x1 (int k) {return (-mi*x1[k]+y1[k]*x2[k]);}
double k1x2 (int k) {return (-mi*x2[k]+(y1[k]-A)*x1[k]);}
double k1y1 (int k) {return (1.-x1[k]*x2[k]);}

double k2x1 (int k) {return (-mi*(x1[k]+dt*k1x1(k)/6.)+(y1[k]+dt*k1y1(k)/6.)*(x2[k]+dt*k1x2(k)/6.));}
double k2x2 (int k) {return (-mi*(x2[k]+dt*k1x2(k)/6.)+((y1[k]+dt*k1y1(k)/6.-A)*(x1[k]+dt*k1x1(k)/6.)));}
double k2y1 (int k) {return (1.-(x1[k]+dt*k1x1(k)/6.)*(x2[k]+dt*k1x2(k)/6.));}

double k3x1 (int k) {return (-mi*(x1[k]+dt*k2x1(k)/3.)+(y1[k]+dt*k2y1(k)/3.)*(x2[k]+dt*k2x2(k)/3.));}
double k3x2 (int k) {return (-mi*(x2[k]+dt*k2x2(k)/3.)+((y1[k]+dt*k2y1(k)/3.-A)*(x1[k]+dt*k2x1(k)/3.)));}
double k3y1 (int k) {return (1.-(x1[k]+dt*k2x1(k)/3.)*(x2[k]+dt*k2x2(k)/3.));}

double k4x1 (int k) {return (-mi*(x1[k]+0.5*dt*k3x1(k))+(y1[k]+0.5*dt*k3y1(k))*(x2[k]+0.5*dt*k3x2(k)));}
double k4x2 (int k) {return (-mi*(x2[k]+0.5*dt*k3x2(k))+((y1[k]+0.5*dt*k3y1(k)-A)*(x1[k]+0.5*dt*k3x1(k))));}
double k4y1 (int k) {return (1.-(x1[k]+0.5*dt*k3x1(k))*(x2[k]+0.5*dt*k3x2(k)));}

double k5x1 (int k) {return (-mi*(x1[k]+2.*dt*k4x1(k)/3.)+(y1[k]+2.*dt*k4y1(k)/3.)*(x2[k]+2.*dt*k4x2(k)/3.));}
double k5x2 (int k) {return (-mi*(x2[k]+2.*dt*k4x2(k)/3.)+((y1[k]+2.*dt*k4y1(k)/3.-A)*(x1[k]+2.*dt*k4x1(k)/3.)));}
double k5y1 (int k) {return (1.-(x1[k]+2.*dt*k4x1(k)/3.)*(x2[k]+2.*dt*k4x2(k)/3.));}

double k6x1 (int k) {return (-mi*(x1[k]+5.*dt*k5x1(k)/6.)+(y1[k]+5.*dt*k5y1(k)/6.)*(x2[k]+5.*dt*k5x2(k)/6.));}
double k6x2 (int k) {return (-mi*(x2[k]+5.*dt*k5x2(k)/6.)+((y1[k]+5.*dt*k5y1(k)/6.-A)*(x1[k]+5.*dt*k5x1(k)/6.)));}
double k6y1 (int k) {return (1.-(x1[k]+5.*dt*k5x1(k)/6.)*(x2[k]+5.*dt*k5x2(k)/6.));}




double evx1 (int k) {return (x1[k]+dt*(k1x1(k)+k2x1(k)+k3x1(k)+k4x1(k)+k5x1(k)+k6x1(k))/6.);}
double evx2 (int k) {return (x2[k]+dt*(k1x2(k)+k2x2(k)+k3x2(k)+k4x2(k)+k5x2(k)+k6x2(k))/6.);}
double evy1 (int k) {return (y1[k]+dt*(k1y1(k)+k2y1(k)+k3y1(k)+k4y1(k)+k5y1(k)+k6y1(k))/6.);}

public:
dynamo (){}
void evolve () {for (int i=1; i<nsteps; i++){
			x1[i]=evx1(i-1);
			x2[i]=evx2(i-1);
			y1[i]=evy1(i-1);
			y2[i]=y1[i]-A;
			if (i%100000==0)cout << "Computing: Sono al "<< i*100./nsteps << "%\n";}

			}
void printresults (ofstream& out){
	out <<"mu ="<< mi <<"\tk="<<k<<'\n';
	out << "Time\tx_1\tx_2\ty_1\ty_2\n";
	for (int i=0; i<nsteps; i++){ 
	out << dt*i <<';'<<x1[i] <<';'<< x2[i]<<';'<< y1[i]<< ';' << y2[i] <<'\n'; 
	}}



dynamo (double K, double mu, double DT, int N, double x10, double x20, double y10) 	{k=K; mi=mu; A=mi*(k*k-1/(k*k)); dt=DT; nsteps=N; 
											x1=new double [N]; x2=new double [N]; 
											y1=new double [N]; y2=new double [N];
											x1[0]=x10; x2 [0]=x20; y1[0]=y10; y2[0]=y10-A;
											//cerr << "Sono il costruttore di dynamo\n"
											}};
void just_one (double mu, double k, double x10, double x20, double y10, int N_steps, string out_filename)
		{dynamo steve;
		steve=dynamo (k, mu, pow(2.,-6.), N_steps, x10,x20,y10);
		steve.evolve();
		ofstream out; out.open(out_filename);
					   steve.printresults(out);
					   out.close(); }



int main (int argc, char** argv) //double mu, double k, double x10, double x20, double y10, int N_steps, string outfile
	{double mu=atof(argv[1]);
	 double k=atof(argv[2]);
	 double x10=atof(argv[3]);
	 double x20=atof(argv[4]);
	 double y10=atof(argv[5]);
	 int N_steps=atoi(argv[6]);
	 string out_filename=argv[7];
	 just_one(mu, k, x10, x20, y10, N_steps, out_filename);}
	 















