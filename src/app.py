from flask import Flask, render_template, request

from src.utils import split_text

app = Flask(__file__)


@app.route('/', methods=['GET', 'POST'])
def index():
    ctx = {}

    if request.method == 'POST':
        file_1 = request.files.get('file_1')
        file_2 = request.files.get('file_2')

        if file_1 is not None:
            file_1.save(file_1.filename)

        if file_2 is not None:
            file_2.save(file_2.filename)

        for num, item in enumerate(request.files.items(), start=1):
            k, v = item
            with open(v.filename, 'r', encoding='utf-8') as file:
                data = split_text(file.read())
                print(num)
                ctx.setdefault(f'file_{num}', data)

    return render_template('index.html', **ctx)


@app.route('/align/')
def align():
    return render_template('align.html')


@app.route('/grid/')
def grid():
    return render_template('grid.html')


if __name__ == '__main__':
    app.run()
