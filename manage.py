from os import PathLike
from src.config.settings import BASE_DIR, VENV_PYTHON_PATH, BOT_MAIN_PATH, BOTMAIN_FILENAME
import subprocess
import sys
from pathlib import Path



def main():
    
    '''Run commands from the commandline using this file and the relative commands.
        For running files inside the src folder, use the -m command in order for the 
        absolute and relative imports to work.'''
    arguments = sys.argv
    length = len(arguments)
    if length == 2:
        if arguments[1] == 'runbot':
            subprocess.check_call([VENV_PYTHON_PATH, '-m', f"src.{BOTMAIN_FILENAME}" ])
        else:
            print('Command not liested.')

    elif length == 3:
        if arguments[1] == 'runfile':
            subprocess.check_call([VENV_PYTHON_PATH, '-m', f"src.{arguments[2]}"])
        else:
            print('Command not liested.')
    else:
        print('Command not liested.')

        
if __name__ == '__main__':
    main()
