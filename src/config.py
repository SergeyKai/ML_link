import os.path
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = os.path.join(BASE_DIR, 'my_book.db')

MODELS = ["sentence_transformer_multilingual", "sentence_transformer_multilingual_labse"]

DEFAULT_MODEL = MODELS[0]

EMBED_BATCH_SIZE = 10
BATCH_SIZE = 100

IMG_OUTPUT_NAME = 'alignment_vis.png'
IMG_OUTPUT_DIR_PATH = os.path.join(BASE_DIR, 'static/alignment_visualisation')
IMG_OUTPUT_PATH = os.path.join(IMG_OUTPUT_DIR_PATH, IMG_OUTPUT_NAME)

# Conflicts settings
MAIN_CHAIN_LENGTH = 2
MAX_CONFLICTS_LEN = 6
BATCH_ID = -1

OUTPUT_FILE_NAME = 'my_book'
OUTPUT_FILE_DIR_PATH = os.path.join(BASE_DIR, 'output_files')
OUTPUT_FILE_PATH = os.path.join(OUTPUT_FILE_DIR_PATH, OUTPUT_FILE_NAME)

FILE_UPLOAD_DIR_NAME = 'uploaded_files'
FILE_UPLOAD_PATH = os.path.join(BASE_DIR, FILE_UPLOAD_DIR_NAME)
