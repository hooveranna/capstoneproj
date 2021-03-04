# from flask_ngrok import run_with_ngrok
from flask import Flask
from flask import render_template
from flask import (
    redirect, request, url_for
)
from TextPersonality import NLUPersonalityInterface
from StoreChars import DiscoveryCharDatabase
from werkzeug.exceptions import InternalServerError

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

@app.errorhandler(InternalServerError)
def handle_500(e):
    original = getattr(e, "original_exception", None)

    #if original is None:
    #    # direct 500 error, such as abort(500)
    #    return render_template("500.html"), 500

    # wrapped unhandled error
    return render_template("500_unhandled.html", e=original), 500



app.run()
