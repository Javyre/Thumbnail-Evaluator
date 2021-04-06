from xdg.BaseDirectory import get_runtime_dir as xdg_runtime_dir
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

from jinja2 import Environment
from hamlish_jinja import HamlishExtension

import os

# Setup environment
UPLOAD_DIR = os.path.join(xdg_runtime_dir(strict=False),
                          'thumbnail-evaluator')
if not os.path.isdir(UPLOAD_DIR):
    os.mkdir(UPLOAD_DIR)

ALLOWED_EXT = {'png', 'jpg', 'jpeg'}

# Setup Flask app
app = Flask(__name__)
app.jinja_options['extensions'] += [HamlishExtension]
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR

app.jinja_env.hamlish_enable_div_shortcut = True

def is_allowed_fname(fname):
    return '.' in fname and fname.rsplit('.', 1)[1].lower() in ALLOWED_EXT

# def validate_file(req, fname):

@app.route('/')
def index():
    return render_template('index.haml')

@app.route('/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return 'invalid file'

    file = request.files['file']
    if file.filename == '':
        return 'invalid file'

    if file and is_allowed_fname(file.filename):
        fname = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
        return render_template('output.haml', output={
            'category': 1,
            'examples': [
                'https://www.youtube.com/watch?v=fHsa9DqmId8',
                'https://www.youtube.com/watch?v=fHsa9DqmId8',
                'https://www.youtube.com/watch?v=fHsa9DqmId8',
            ]
        })

    return 'invalid file'
