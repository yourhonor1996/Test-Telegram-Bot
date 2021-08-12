from pathlib import Path


TOKEN = '1891854677:AAEDNLc4q9cbtfHMI0JoBKviVx6gFLsApb4'

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

DATABASE_NAME = 'sakila'

# ---------------------------------------------------------------------------------
# Django Settings for using django ORM in the project

DJ_DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': DATABASE_NAME,
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'adelante5225',   
    }
}

DJ_INSTALLED_APPS = [
    'src.config.django_app_config.SRCConfig'
]

DJ_BASE_DIR = BASE_DIR.parent

DJ_DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
