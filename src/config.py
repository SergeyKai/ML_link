import os.path
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = os.path.join(BASE_DIR, 'my_book.db')
