
from os import PathLike
from src.config.settings import BASE_DIR, VENV_PYTHON_PATH, BOT_MAIN_PATH
import subprocess
import sys
from pathlib import Path

# VENV_PYTHON_PATH = (BASE_DIR.parent / ".venv" / "Scripts" / "python.exe")



def main():
    # print(VENV_PYTHON_PATH)
    arguments = sys.argv
    length = len(arguments)
    if length == 2:
        if arguments[1] == 'runbot':
            subprocess.check_call([VENV_PYTHON_PATH, BOT_MAIN_PATH ])
        else:
            print('Command not liested.')

    elif length == 3:
        if arguments[1] == 'runfile':
            subprocess.check_call([VENV_PYTHON_PATH, BASE_DIR/arguments[2]])
        else:
            print('Command not liested.')
    else:
        print('Command not liested.')

        
if __name__ == '__main__':
    main()
