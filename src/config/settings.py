from pathlib import Path


TOKEN = '1891854677:AAGdDC2MEkq-EQOvwuiIdqz9Kn94xOUFHBI'

# this is the src folder 
BASE_DIR = Path(__file__).resolve().parent.parent

MYSQL_CONNECTION = {
    'user': 'root',
    'password': 'adelante5225',
    'host': '127.0.0.1',
    'use_pure':True,
    'connection_timeout':1000
}

QUERIES_DIR = BASE_DIR / 'queries'

VENV_FOLDERNAME = '.venv'

VENV_PYTHON_PATH = (BASE_DIR.parent / VENV_FOLDERNAME / "Scripts" / "python.exe")

BOTMAIN_FILENAME = 'bot_main'

BOT_MAIN_PATH = BASE_DIR/f'{BOTMAIN_FILENAME}.py'

REQUIREMENTS_FILENAME = 'requirements.txt'

DATABASE_NAME = 'new_schema'

NUMBER_OF_QUESTIONS = 5

CHECK_EMOJI = "⭕️"

NUMBER_OF_USERS_FOR_SESSION = 2