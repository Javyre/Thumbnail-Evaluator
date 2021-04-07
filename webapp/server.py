from xdg.BaseDirectory import get_runtime_dir as xdg_runtime_dir
from flask import Flask, flash, request, g, redirect, render_template
from werkzeug.utils import secure_filename

from jinja2 import Environment
from hamlish_jinja import HamlishExtension

import os

from model import Model
from youtube import fetch_examples

# Setup environment
UPLOAD_DIR = os.path.join(xdg_runtime_dir(strict=False),
                          'thumbnail-evaluator')
if not os.path.isdir(UPLOAD_DIR):
    os.mkdir(UPLOAD_DIR)

ALLOWED_EXT = {'png', 'jpg', 'jpeg'}

# Setup Flask app
app = Flask(__name__)
app.jinja_options['extensions'] += [HamlishExtension]
app.config['UPLOAD_DIR'] = UPLOAD_DIR
app.config['MODEL_DIR'] = 'static/model.h5'

app.jinja_env.hamlish_enable_div_shortcut = True

def is_allowed_fname(fname):
    return '.' in fname and fname.rsplit('.', 1)[1].lower() in ALLOWED_EXT

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
        fname = os.path.join(app.config['UPLOAD_DIR'], fname)
        file.save(fname)

        if 'model' not in g:
            g.model = Model(app.config['MODEL_DIR'])

        prediction = g.model.predict(fname)
        os.remove(fname)
        return render_template('output.haml', output={
            'category': prediction,
            'examples': fetch_examples(prediction),
        })

    return 'invalid file'
