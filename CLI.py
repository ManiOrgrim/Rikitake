#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 16:23:55 2020

@author: mani
SONO LA CLI
"""
from plumbum import cli
import plumbum.cli.terminal as terminal
from subprocess import run
from subprocess import check_output
from subprocess import PIPE
import os

class Rikitake(cli.Application):
    """docstring to be written"""
    PROGNAME = "Rikitake"
    VERSION ="0.1"
    
    def create_infile(self):
        process=run(["python3", "create_infiles.py"] )
        assert process.returncode==0
    
    
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
    
    def main (self):
        if 'input_values.txt' in os.listdir():
            self.there_is_infile()
        else:
            self.there_is_not_infile()
        
        run(["python3","dynamo.py"])
        run(["python3","image_creator.py"])
        run(["python3","lyapunov.py"])
        
        if(terminal.ask("Run another simulation?")):
            print("Please rename/save elsewhere the present 'input_values.txt' if you will to change it for this simulation.")
            self.main()
        
        
if __name__=='__main__':
    Rikitake()