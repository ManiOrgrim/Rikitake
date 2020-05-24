
from plumbum import cli
import plumbum.cli.terminal as terminal
from subprocess import run
from subprocess import check_output
from subprocess import PIPE
import os
import create_infiles
import dynamo
import image_creator
import lyapunov
import time


class Rikitake(cli.Application):
    """docstring to be written"""
    PROGNAME = "rikitake"
    VERSION ="0.1"

    def main (self):
        if 'input_values.txt' in os.listdir():
            self.there_is_infile()
        else:
            self.there_is_not_infile()
        current_time=time.time()
        dynamo.generate_data()
        image_creator.generate_images()
        lyapunov.lyapunov()
        print((time.time()-current_time)/60)
        if(terminal.ask("Run another simulation?")):
            print("Please rename/save elsewhere the present 'input_values.txt' if you will to change it for this simulation.")
            self.main()

    def create_infile(self):
        create_infiles.create_infile()
    
    
    def there_is_infile(self):
        answer=terminal.ask("Do you want to create a new 'input_values.txt' file?")
        if (answer):
            answer2=terminal.ask("This process will overwrite DEFINITEVELY 'input_values.txt'. Do you still want to proceed?")
            if (answer2):
                self.create_infile()
                
    def ask_for_simulation_ID(self):
        simulation_ID=terminal.prompt("Please choose a (string) simulation ID for the run." )
        return simulation_ID
    
    def there_is_not_infile(self):
        self.create_infile()

    
        
        
if __name__=='__main__':
    
    Rikitake.run()
    
