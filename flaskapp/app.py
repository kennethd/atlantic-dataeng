import argparse
import os
import sys

from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

from atldata.ingest import ingest_file


APP_DIR = os.path.dirname(os.path.realpath(__file__))
INST_DIR = os.path.dirname(APP_DIR)
DATA_DIR = os.environ.get('DATA_DIR', os.path.sep.join([INST_DIR, 'data']))
DATABASE = os.path.sep.join([DATA_DIR, 'atldata.db'])
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', os.path.sep.join([INST_DIR, 'uploads']))
ALLOWED_EXTENSIONS = ['tsv', 'csv']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def configured_app(config_module=None, debug=False):
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    # default config
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['DATABASE'] = DATABASE

    if config_module:
        app.config.from_object(config_module)
    else:
        app.config.from_envvar('FLASK_CONFIG', silent=True)

    if debug:
        app.debug = True

    @app.route('/', methods=['GET', 'POST'])
    def upload_customer_data():
        if request.method == 'POST':

            print(request.files)
            print(request.files['custdata'])
            print(dir(request.files['custdata']))

            if 'custdata' not in request.files:
                flash('No file uploaded')
                return redirect(request.url)

            f = request.files['custdata']

            if not f.filename:
                flash('No selected file')
                return redirect(request.url)

            if not allowed_file(f.filename):
                flash('Only {} files accepted'.format(', '.join(ALLOWED_EXTENSIONS)))
                return redirect(request.url)

            filename = secure_filename(f.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            try:
                f.save(filepath)
            except Exception as ex:
                # There are very few times I will accept bare exceptions,
                # this is mostly a concession to time constraints
                flash(str(ex))
                return redirect(request.url)

            msgs = ingest_file(filepath)
            for msg in msgs:
                flash(msg)
            return redirect(request.url)

        return render_template('index.html')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error404.html'), 404

    return app

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='webapp interface to atldata functions')
    parser.add_argument('--config', help="config module (as python path, e.g.  --config=config).  if not set, will look for FLASK_CONFIG")
    parser.add_argument('--debug', action="store_true", help="put app into debug mode")
    parser.add_argument('--port', type=int, default=8888, help="port number.  default 8888")
    args = parser.parse_args()

    app = configured_app(args.config, debug=args.debug)
    app.run(port=args.port)

