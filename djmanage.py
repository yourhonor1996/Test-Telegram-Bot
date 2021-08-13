import sys
from django import setup
from django.conf import settings as dj_settings
from src.config import settings



def main():
    
    dj_settings.configure(**settings.DJANGO_SETTINGS)
    setup()

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

        
if __name__ == '__main__':
    main()
