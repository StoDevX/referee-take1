import os.path

from flask import Flask
app = Flask(__name__)

app.config.from_object(__name__)
app.config.update({
    'SPECS_DIR': os.path.join(app.root_path, 'specs'),
})
app.config.from_envvar('REFEREE_SETTINGS', silent=True)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/hooks/git')
def git():
    return 'git message'
