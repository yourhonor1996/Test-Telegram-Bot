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

DATABASE_NAME = 'new_schema'

# ---------------------------------------------------------------------------------
# Django Settings for using django ORM in the project
DJANGO_SETTINGS = {
    'DATABASES': {
        'default': {
            'ENGINE': 'mysql.connector.django',
            'NAME': DATABASE_NAME,
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'USER': 'root',
            'PASSWORD': 'adelante5225',   
        }
    },
    
    'INSTALLED_APPS': [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'src.config.django_app_config.SRCConfig',
        
    ],
    
    'BASE_DIR': BASE_DIR.parent,
    
    'DEFAULT_AUTO_FIELD':'django.db.models.BigAutoField',
    
    'DEBUG': True,
    
    'SECRET_KEY': 'django-insecure-0s!ha@xf0y0l1+3=g(el%6p-c$u91juj6rc7b*qj%#y6p)epok',
    
    'TEMPLATES': [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        }
    ],
    'MIDDLEWARE' : [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        # 'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],
    
    'ROOT_URLCONF': 'src.urls'
}