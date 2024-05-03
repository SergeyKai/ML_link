from flask import Flask, render_template, request, redirect

from src.storage import FirstFile, SecondFile
from src.utils import split_text, create_db, alignment, get_conflicts, second_alignment, create_result_file_html

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
        batches = request.form.get('batches')
        shift = request.form.get('shift')
        windows = request.form.get('windows')

        alignment(
            batches=int(batches),
            shift=int(shift),
            windows=int(windows),
        )

        ctx['conflicts_1'], ctx['conflicts_2'] = get_conflicts()

    return render_template('align.html', **ctx)


@app.route('/secondary-align/', methods=['GET', 'POST'])
def second_alignment_view():
    if request.method == 'POST':
        return redirect('/align/')
    second_alignment()
    c_1, c_2 = get_conflicts()

    ctx = {
        'visualization_files': [f'alignment_visualisation/alignment_vis_{count}.png' for count in range(int(1))],
        'conflicts_1': c_1,
        'conflicts_2': c_2,
    }

    return render_template('align.html', **ctx)


@app.route('/grid/', methods=['GET', 'POST'])
def grid():
    ctx = {}
    if request.method == 'POST':
        current_format = request.form.get('format')

        if current_format == 'HTML':
            file_path, file_content = create_result_file_html()
            ctx = {
                'file_path': file_path,
                'file_content': file_content,
            }

    return render_template('grid.html', **ctx)


if __name__ == '__main__':
    app.run()
