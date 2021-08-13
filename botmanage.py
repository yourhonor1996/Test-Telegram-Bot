from src.config.settings import VENV_PYTHON_PATH, BOTMAIN_FILENAME
import subprocess
import sys


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
            print('Command not supported.')
    else:
        print('Command not supported.')

        
if __name__ == '__main__':
    main()
