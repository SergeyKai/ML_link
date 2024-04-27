from flask import Flask, render_template, request

from src.storage import FirstFile, SecondFile
from src.utils import split_text, create_db, alignment

app = Flask(__file__)


def form_file_upload_validation():
    pass


def prepare_ctx_text(filename: str, lang: str):
    """
    lang: str: 'ru' or 'en'
    """
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
        chars_count = len(text)
        data = split_text(text, lang)
        row_count = len(data)
        return {
            'text': text,
            'chars_count': chars_count,
            'data': data,
            'row_count': row_count,
            'filename': filename,
        }


@app.route('/', methods=['GET', 'POST'])
def index():
    ctx = {}

    if request.method == 'POST':
        print(request.form)
        file_1 = request.files.get('file_1')
        file_2 = request.files.get('file_2')

        langauge_first = request.form.get('langauge-first')
        langauge_second = request.form.get('langauge-second')

        if file_1 is not None:
            file_1.save(file_1.filename)

        if file_2 is not None:
            file_2.save(file_2.filename)

        first_file_data = prepare_ctx_text(file_1.filename, langauge_first)
        second_file_data = prepare_ctx_text(file_2.filename, langauge_second)

        FirstFile.save_data(**first_file_data, lang=langauge_first)
        SecondFile.save_data(**second_file_data, lang=langauge_second)

        ctx.setdefault('file_1', first_file_data)
        ctx.setdefault('file_2', second_file_data)

    else:
        ctx.setdefault(f'file_1', None)
        ctx.setdefault(f'file_2', None)

    return render_template('index.html', **ctx)


@app.route('/align/', methods=['GET', 'POST'])
def align():
    ctx = {
        'visualization_files': [f'alignment_visualisation/alignment_vis_{count}.png' for count in range(int(1))],
    }

    if FirstFile.FILE_NAME is not None and SecondFile.FILE_NAME is not None:
        create_db()

    if request.method == 'POST':
        print(request.form)
        batches = request.form.get('batches')
        shift = request.form.get('shift')
        windows = request.form.get('windows')

        alignment(
            batches=int(batches),
            shift=int(shift),
            windows=int(windows),
        )

        # ctx['visualization_files'].extend([f'alignment_vis_{count}.png' for count in range(int(batches))])

        print(batches)
        print(shift)
        print(windows)
    return render_template('align.html', **ctx)


@app.route('/grid/')
def grid():
    return render_template('grid.html')


if __name__ == '__main__':
    app.run()
