import os

from lingtrain_aligner import preprocessor, splitter, aligner, resolver, reader, helper, vis_helper, saver
from src.config import DB_PATH, DEFAULT_MODEL, EMBED_BATCH_SIZE, IMG_OUTPUT_PATH, BATCH_SIZE, MAIN_CHAIN_LENGTH, \
    MAX_CONFLICTS_LEN, BATCH_ID, OUTPUT_FILE_PATH, OUTPUT_FILE_DIR_PATH
from src.storage import FirstFile, SecondFile


def marks_parse():
    pass


def split_text(text: str, lang: str = 'ru'):
    text = text.split('\n')
    text_prepared = preprocessor.mark_paragraphs(text)
    return splitter.split_by_sentences_wrapper(text_prepared, lang)


def create_db():
    # if os.path.isfile(DB_PATH):
    #     os.unlink(DB_PATH)

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
        batch_size=400,
        batch_ids=batch_ids,
        size=(800, 800),
    )


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


def get_conflicts():
    conflicts_to_solve, rest = resolver.get_all_conflicts(
        DB_PATH,
        min_chain_length=MAIN_CHAIN_LENGTH,
        max_conflicts_len=MAX_CONFLICTS_LEN,
        batch_id=BATCH_ID
    )

    print('=' * 30)
    print(conflicts_to_solve)
    print('=' * 30)

    conflicts_first_file = []
    conflicts_second_file = []

    for conflict in conflicts_to_solve:
        c_conf = resolver.show_conflict(DB_PATH, conflict)
        conflicts_first_file.extend([{k: v} for k, v in c_conf[0].items()])
        conflicts_second_file.extend([{k: v} for k, v in c_conf[1].items()])
        print(1)

    return conflicts_first_file, conflicts_second_file


def second_alignment():
    steps = 3
    batch_id = -1

    for i in range(steps):
        conflicts, rest = resolver.get_all_conflicts(
            DB_PATH,
            min_chain_length=2 + i,
            max_conflicts_len=6 * (i + 1),
            batch_id=batch_id,
            handle_start=True,
            handle_finish=True,
        )
        resolver.resolve_all_conflicts(
            DB_PATH,
            conflicts,
            DEFAULT_MODEL,
            show_logs=False
        )
        vis_helper.visualize_alignment_by_db(
            DB_PATH,
            output_path=IMG_OUTPUT_PATH,
            lang_name_from=FirstFile.LANGUAGE,
            lang_name_to=SecondFile.LANGUAGE,
            batch_size=400,
            size=(600, 600),
            plt_show=False,
        )

        if len(rest) == 0:
            break


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def create_result_file_html():
    current_file_path = OUTPUT_FILE_PATH + '.html'

    paragraphs, delimeters, metas, sent_counter = reader.get_paragraphs(
        DB_PATH, direction="to"
    )
    my_style = [
        '{"background": "#A2E4B8", "color": "black", "border-bottom": "0px solid red"}',
        '{"background": "#FFC1CC", "color": "black"}',
        '{"background": "#9BD3DD", "color": "black"}',
        '{"background": "#FFFCC9", "color": "black"}'
    ]

    lang_ordered = ["from", "to"]

    reader.create_book(
        lang_ordered=lang_ordered,
        paragraphs=paragraphs,
        delimeters=delimeters,
        metas=metas,
        sent_counter=sent_counter,
        output_path=current_file_path,
        template="pastel_fill",
        styles=my_style,
    )

    return current_file_path, read_file(current_file_path)


def create_result_file_TMX():
    current_file_path = OUTPUT_FILE_PATH + '.tmx'
    saver.save_tmx(DB_PATH, current_file_path, FirstFile.LANGUAGE, SecondFile.LANGUAGE)

    return current_file_path
