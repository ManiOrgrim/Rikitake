
from plumbum import cli
import plumbum.cli.terminal as terminal
import os
import sys
from plumbum import colors

import create_infiles
import integrator
import image_creator
import lyapunov


class Rikitake(cli.Application):
    """This program integrates the Rikitake Dynamo differential equation system, 
    generates the images of the phase space projections
    and calculates the Lyapunov Exponents of the particular obtained solution."""
    
    PROGNAME = "rikitake"
    VERSION ="2.0.1"
    
    save_dir=os.getcwd() #if not changed, results will be saved in currently working directory
    dt=2**-8
    
    integration_completed=False
    images_created=False
    lyapuov= 'not calculated'
    

    def main (self):
        """This function leads the exectution of the program."""
        if 'input_values.txt' in os.listdir(self.save_dir):
            self.there_is_infile()
        else:
            self.there_is_not_infile()
        if not self.dont_perform_integration:
           self.integration_completed=integrator.generate_data(self.save_dir, self.dt)
        if not self.dont_calculate_lyapunov:
           self.lyap_exp_calculated=lyapunov.lyapunov(self.save_dir)
        if not self.dont_generate_images:
           self.images_created=image_creator.image_creator(self.save_dir)
        if (self.integration_completed and self.images_created and self.verbose):
            print(colors.green|"Process completed.")
        if(self.verbose):
            print(colors.green|"These processes have been performed:")
            print(colors.green|"INTEGRATION:",self.integration_completed)
            print(colors.green|"LYAPUNOV EPONENT:" ,self.lyapunov)
      
            print(colors.green|"IMAGE GENERATION:",self.images_created)
        if(self.alert):
            duration = 1  # seconds
            freq = 441  # Hz
            os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
        if(terminal.ask("Run another simulation?")):
            print("Please rename/save elsewhere the present 'input_values.txt' if you want to change it for this simulation.")
            self.main()
        else: sys.exit([0])
   
    dont_perform_integration=cli.Flag(["NOint"], help ="If given integration will not be performed.")
    dont_generate_images=cli.Flag(["NOimg"],help="If given phase space images will not be generated.")

    dont_calculate_lyapunov=cli.Flag(["NOly"], help="If given lyapunov exponents calculation will not be performed.")
    
    
    verbose = cli.Flag(["v", "verbose"], help = "If given the program will be very talkative.")
    alert= cli.Flag(["a", "alarm"], help="If given the program will ring an alert when it finishes running.")
    
            
    
    @cli.switch('--save-dir', str)
    def set_save_dir (self, path_to_dir):
        """Allows the user to specify the path in wich the results will be saved.
        If not specified results will be saved in current working directory."""
        if path_to_dir not in os.listdir():
          os.mkdir(path_to_dir)
        self.save_dir=path_to_dir
        
    @cli.switch('--set-dt', float)
    def set_dt (self, dt):
        """Allows the user to specify the time interval dt that will be used 
        during the integration.
        If not specified, the default value is dt=2^-8."""
        self.dt=dt

    
    
    def there_is_infile(self):
        """Asks the user if she wants to replace currently existing 'input_values.txt' file."""

        answer=terminal.ask("Do you want to create a new 'input_values.txt' file?")
        if (answer):
            answer2=terminal.ask(colors.yellow|"This process will overwrite DEFINITEVELY 'input_values.txt'. Do you still want to proceed?")
            if (answer2):
                self.create_infile()
    
    def there_is_not_infile(self):
        """If there is not 'input_values.txt' file in save_dir, the file will be created."""
        self.create_infile()

    def create_infile(self):
        """Creates a new 'input_values.txt' file in save_dir. 
        If such file exists it will be replaced."""
        create_infiles.create_infile(self.save_dir)

        
        
if __name__=='__main__':
    
    Rikitake.run()
    
