import os
import json
import hashlib
import gettext

from flask import Flask
from flask import request, redirect, send_from_directory, url_for
from werkzeug.utils import secure_filename

from turing_machine.constants import BY_STEP_MODE
from turing_machine.turing_machine import TuringMachine


app = Flask(__name__)


def get_md5(filename):
    with open(filename, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


@app.route('/js/<filename>')
def js_file(filename):
    return send_from_directory(app.config['JS_FOLDER'], filename)


@app.route('/css/<filename>')
def css_file(filename):
    return send_from_directory(app.config['CSS_FOLDER'], filename)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']

        if file and file.filename.endswith('.json'):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('view_machine', filename=filename))

    return '''
        <html>
        <head>
            <title>Turing machine viewer</title>
            <meta charset='utf-8'>
            <link rel="stylesheet" type="text/css" href="/css/styles.css?v={style}">
        </head>
        <body>
            <form action="" method="post" enctype="multipart/form-data">
                <h2>Turing machine viewer</h2>

                <input type="file" name="file" id="file" class="input-file" accept=".json" />
                <div><input type="submit" value="Upload file"></div>
            </form>
        </body>
        </html>
    '''.format(style=get_md5(app.config["CSS_FOLDER"] + "/styles.css"))


@app.route('/view-machine/<filename>', methods=['GET'])
def view_machine(filename):
    with open(app.config['UPLOAD_FOLDER'] + '/' + filename, encoding='utf-8') as f:
        config = json.load(f)

    turing_machine = TuringMachine(**config)
    result = turing_machine.run(mode=BY_STEP_MODE)

    return '''
    <html>
    <head>
        <title>{title}</title>
        <meta charset="utf-8">

        <link rel="stylesheet" type="text/css" href="/css/styles.css?v={style}">
    </head>

    <body>
        <div class='turing-machine'>
            <div class='margined'><b>Tape: </b><div class='tape' id='tape'></div></div>
            <div class='margined'><b>Alphabet: </b><div class='alphabet' id='alphabet'></div></div>
            <div><b>Rules:</b><br><div><table class='rules' id='rules'></table></div></div>
            <div class='button-box'><button onclick='Run()'>Show solve</button></div>
            <div id='result-box'></div>
        </div>

        <script src="/js/turing_machine.js?v={js}"></script>
        <script>
            let tape = '{tape}'
            let alphabet = '{alphabet}'
            let rules = {rules}
            let result = {result}

            let turing = new TuringMachine(alphabet, tape, rules)

            function Run() {{
                turing.Run(result)
            }}
        </script>
    </body>
    </html>
    '''.format(
        title=_('Turing machine emulator'),
        style=get_md5(app.config["CSS_FOLDER"] + "/styles.css"),
        js=get_md5(app.config["JS_FOLDER"] + "/turing_machine.js"),
        tape=config["tape"],
        alphabet=config["alphabet"],
        rules=config["rules"],
        result=result
    )


def main():
    path = os.path.dirname(__file__)
    gettext.install('turing_machine', localedir=path)

    host = "0.0.0.0"
    port = 5000
    debug = True

    app.config['JS_FOLDER'] = path + '/web/js'  # папка с js кодом
    app.config['CSS_FOLDER'] = path + '/web/css'  # папка со стилями
    app.config['UPLOAD_FOLDER'] = path + '/web/upload'  # папка с загрузками

    app.run(debug=debug, host=host, port=port)


if __name__ == '__main__':
    main()
