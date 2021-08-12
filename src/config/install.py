
'''Install the virtual environment and the reuqirements from the requirements file.'''



from src.config import settings
import subprocess


subprocess.check_call(['py', '-m', 'venv', settings.VENV_FOLDERNAME])
subprocess.check_call([str(settings.VENV_PYTHON_PATH), '-m','pip', 'install','-r', settings.REQUIREMENTS_FILENAME])

