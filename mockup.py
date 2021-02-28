# from flask_ngrok import run_with_ngrok
from flask import Flask
from flask import render_template
from flask import (
    redirect, request, url_for
)
from TextPersonality import NLUPersonalityInterface
from StoreChars import DiscoveryCharDatabase

app = Flask(__name__)
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
    nlu = NLUPersonalityInterface()
    this_dict = nlu.get_personality(usertext)
    # add condition to handle nlu error
    ddb = DiscoveryCharDatabase("Collection 1")
    char_match = ddb.search_char(this_dict)
    return render_template('output.html', username=username, character_name=char_match)


app.run()
