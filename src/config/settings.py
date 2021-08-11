from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
# print(BASE_DIR)
MYSQL_CONNECTION = {
    'user': 'root',
    'password': 'adelante5225',
    'host': '127.0.0.1',
}

QUERIES_DIR = BASE_DIR / 'queries'

VENV_PYTHON_PATH = (BASE_DIR.parent / ".venv" / "Scripts" / "python.exe")
BOT_MAIN_PATH = BASE_DIR/'bot_main.py'