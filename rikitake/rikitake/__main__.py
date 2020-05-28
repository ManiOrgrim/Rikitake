
from plumbum import cli
import plumbum.cli.terminal as terminal
import os
import create_infiles
import integrator
import image_creator
import lyapunov



class Rikitake(cli.Application):
    """This program integrates the Rikitake Dynamo differential equation system, 
    generates the images of the phase space projections
    and calculates the Lyapunov Exponents of the particular obtained solution."""
    
    PROGNAME = "rikitake"
    VERSION ="0.1"
    
    save_dir=os.getcwd() #if not changed, results will be saved in currently working directory
    dt=2**-8
    
    integration_completed=False
    images_created=False
    lyap_exp_calculated=False

    def main (self):
        """This function leads the exectution of the program."""
        if 'input_values.txt' in os.listdir(self.save_dir):
            self.there_is_infile()
        else:
            self.there_is_not_infile()
        if not self.dont_perform_integration:
           self.integration_completed=integrator.generate_data(self.save_dir, self.dt)
        if not self.dont_generate_images:
           self.images_created=image_creator.generate_images(self.save_dir)
        if not self.dont_calculate_lyapunov:
           self.lyap_exp_calculated=lyapunov.lyapunov(self.save_dir)
        if (self.integration_completed and self.images_created and self.lyap_exp_calculated and self.verbose):
            print("All the process worked successfully.")
        elif(self.verbose):
            print("Only these processes have been performed:")
            print("INTEGRATION:",self.integration_completed)
            print("IMAGE GENERATION:",self.images_created)
            print("LYAPUNOV EXPONENTS:",self.lyap_exp_calculated)
        if(terminal.ask("Run another simulation?")):
            print("Please rename/save elsewhere the present 'input_values.txt' if you will to change it for this simulation.")
            self.main()
   
    dont_perform_integration=cli.Flag(["NOint","NOintegration"], help ="If given integration will not be performed.")
    dont_generate_images=cli.Flag(["NOimg","NOimages"],help="If given phase space images will not be generated.")
    dont_calculate_lyapunov=cli.Flag(["NOly","NOlyapunov"], help="If given lyapunov exponents calculation will not be performed.")
    verbose = cli.Flag(["v", "verbose"], help = "If given the program will be very talkative.")
   
    
            
    
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
            answer2=terminal.ask("This process will overwrite DEFINITEVELY 'input_values.txt'. Do you still want to proceed?")
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
    
