import os

from lingtrain_aligner import preprocessor, splitter, aligner, resolver, reader, helper, vis_helper


def split_text(text: str, lang_from: str = 'ru'):
    return splitter.split_by_sentences_wrapper(text, lang_from)
    # splitted_to = splitter.split_by_sentences_wrapper(text2_prepared, lang_to)
