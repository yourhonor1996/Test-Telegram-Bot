import sys
from django import setup
from django.conf import settings as dj_settings
from src.config import settings



def main():
    
    dj_settings.configure(
        DATABASES= settings.DJ_DATABASES,
        INSTALLED_APPS= settings.DJ_INSTALLED_APPS,
        BASE_DIR = settings.DJ_BASE_DIR,
        DEFAULT_AUTO_FIELD = settings.DJ_DEFAULT_AUTO_FIELD
    )
    setup()

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

        
if __name__ == '__main__':
    main()
