
from plumbum import cli
import plumbum.cli.terminal as terminal
import os
import create_infiles
import dynamo
import image_creator
import lyapunov



class Rikitake(cli.Application):
    """docstring to be written"""
    PROGNAME = "rikitake"
    VERSION ="0.1"
    
    save_dir=os.getcwd() #if not changed, results will be saved in currently working directory
    dt=2**-8

    @cli.switch('--save-dir', str)
    def set_save_dir (self, path_to_dir):
        if path_to_dir not in os.listdir():
          os.mkdir(path_to_dir)
        self.save_dir=path_to_dir
    
    def main (self):
        if 'input_values.txt' in os.listdir(self.save_dir):
            self.there_is_infile()
        else:
            self.there_is_not_infile()
        dynamo.generate_data(self.save_dir, self.dt)
        image_creator.generate_images(self.save_dir)
        lyapunov.lyapunov(self.save_dir)
        if(terminal.ask("Run another simulation?")):
            print("Please rename/save elsewhere the present 'input_values.txt' if you will to change it for this simulation.")
            self.main()

    def create_infile(self):
        create_infiles.create_infile(self.save_dir)
    
    
    def there_is_infile(self):
        answer=terminal.ask("Do you want to create a new 'input_values.txt' file?")
        if (answer):
            answer2=terminal.ask("This process will overwrite DEFINITEVELY 'input_values.txt'. Do you still want to proceed?")
            if (answer2):
                self.create_infile()
    
    def there_is_not_infile(self):
        self.create_infile()


    
        
        
if __name__=='__main__':
    
    Rikitake.run()
    
