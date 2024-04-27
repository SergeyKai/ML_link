import os

from lingtrain_aligner import preprocessor, splitter, aligner, resolver, reader, helper, vis_helper

from src.config import DB_PATH, DEFAULT_MODEL, EMBED_BATCH_SIZE, IMG_OUTPUT_PATH, BATCH_SIZE
from src.storage import FirstFile, SecondFile


def marks_parse():
    pass


def split_text(text: str, lang: str = 'ru'):
    text = text.split('\n')
    text_prepared = preprocessor.mark_paragraphs(text)
    return splitter.split_by_sentences_wrapper(text_prepared, lang)


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


def visualize(batches: int, batch_ids):
    p = vis_helper.visualize_alignment_by_db(
        DB_PATH,
        output_path=IMG_OUTPUT_PATH,
        lang_name_from=FirstFile.LANGUAGE,
        lang_name_to=SecondFile.LANGUAGE,
        batch_size=batches * BATCH_SIZE,
        batch_ids=batch_ids,
        size=(800, 800),
    )

    print(p)


def alignment(
        batches: int,
        shift: int,
        windows: int,
):
    batch_ids = range(batches)
    aligner.align_db(DB_PATH,
                     DEFAULT_MODEL,
                     batch_size=batches * BATCH_SIZE,
                     window=windows,
                     batch_ids=batch_ids,
                     save_pic=False,
                     embed_batch_size=EMBED_BATCH_SIZE,
                     normalize_embeddings=True,
                     show_progress_bar=True,
                     shift=shift
                     )

    visualize(batches, batch_ids)
