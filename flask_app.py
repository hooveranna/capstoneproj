# from flask_ngrok import run_with_ngrok
from flask import Flask
from flask import render_template
from flask import (
    redirect, request, url_for
)
from TextPersonality import NLUPersonalityInterface
from StoreChars import DiscoveryCharDatabase
from chart import create_figure

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
# run_with_ngrok(app)   # starts ngrok when the app is run


@app.route("/", methods=('GET', 'POST'))
def home(name=None):
    if request.method == 'POST':
        username = request.form['name']
        usertext = request.form['usertext']
        return redirect(url_for('submit', username=username, usertext=usertext))
    return render_template('index.html', name=name)


@app.route("/submit/<username>/<usertext>")
def submit(username, usertext):
    file_name = "test_file.jpeg"
    nlu = NLUPersonalityInterface()
    this_dict = nlu.get_personality(usertext)
    create_figure(this_dict, file_name)
    # add condition to handle nlu error
    ddb = DiscoveryCharDatabase("Collection 1")
    char_match = ddb.search_char(this_dict)
    return render_template('output.html', username=username, character_name=char_match, file_name=file_name)

@app.route("/about-us")
def about(name=None):
    return render_template('about.html', name=name)

app.run()
