import os

from lingtrain_aligner import preprocessor, splitter, aligner, resolver, reader, helper, vis_helper

from src.config import DB_PATH
from src.storage import FirstFile, SecondFile


def marks_parse():
    pass


def split_text(text: str, lang: str = 'ru'):
    text = text.split('\n')
    text_prepared = preprocessor.mark_paragraphs(text)
    return splitter.split_by_sentences_wrapper(text_prepared, lang)
    # splitted_to = splitter.split_by_sentences_wrapper(text2_prepared, lang_to)


def create_db():
    if os.path.isfile(DB_PATH):
        os.unlink(DB_PATH)

    print('=' * 30)
    print(FirstFile.LANGUAGE)
    print(SecondFile.LANGUAGE)
    print('=' * 30)

    aligner.fill_db(
        DB_PATH,
        FirstFile.LANGUAGE,
        SecondFile.LANGUAGE,
        FirstFile.DATA,
        SecondFile.DATA,
    )
