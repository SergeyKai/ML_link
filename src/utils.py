import os

from lingtrain_aligner import preprocessor, splitter, aligner, resolver, reader, helper, vis_helper

from src.config import DB_PATH


def marks_parse():
    pass


def split_text(text: str, lang_from: str = 'ru'):
    return splitter.split_by_sentences_wrapper(text, lang_from)
    # splitted_to = splitter.split_by_sentences_wrapper(text2_prepared, lang_to)


def create_db():
    if os.path.isfile(DB_PATH):
        os.unlink(DB_PATH)

    aligner.fill_db(DB_PATH, lang_from, lang_to, splitted_from, splitted_to)
