# from flask_ngrok import run_with_ngrok
from flask import Flask
from flask import render_template
from flask import (
    redirect, request, url_for
)
from TextPersonality import NLUPersonalityInterface
from StoreChars import DiscoveryCharDatabase
from werkzeug.exceptions import InternalServerError
from chart import create_figure
import time
import random

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
    # file_name2 = "test_file2.jpeg"
    file_name3 = "character_emotions.jpeg"
    # file_name4 = "character_concept.jpeg"
    nlu = NLUPersonalityInterface()
    this_dict = nlu.get_personality(usertext)
    create_figure(this_dict[0], file_name)
    # create_figure(this_dict[1], file_name2)
    ddb = DiscoveryCharDatabase("Collection 1")
    full_dict = dict(this_dict[0])
    full_dict.update(this_dict[1])
    char_match, personality = ddb.search_char(full_dict)
    if personality:
        sentences = personality.pop("sentences")
        if len(sentences) < 3:
            sentences = random.sample(sentences,1)
        else:
            sentences = random.sample(sentences,3)
    else:
        sentences = ["There are none"]
    book_title = personality.pop("title", "Unknown")
    emotions, concepts = get_emotions_from_dict(personality)
    create_figure(emotions, file_name3)
    # create_figure(personality, file_name4)
    return render_template('output.html', username=username, character_name=char_match, file_name=file_name, concepts=this_dict[1].keys(), file_name3=file_name3, char_concepts=personality.keys(), title=book_title, sentences=sentences)


@app.route("/about-us")
def about(name=None):
    return render_template('about.html', name=name)


@app.errorhandler(InternalServerError)
def handle_500(e):
    original = getattr(e, "original_exception", None)

    #if original is None:
    #    # direct 500 error, such as abort(500)
    #    return render_template("500.html"), 500

    # wrapped unhandled error
    return render_template("500_unhandled.html", e=original), 500


def get_emotions_from_dict(personality):
    emotions_dict = dict()
    emotions_dict["disgust"] = personality.pop("disgust", 0)
    emotions_dict["joy"] = personality.pop("joy", 0)
    emotions_dict["anger"] = personality.pop("anger", 0)
    emotions_dict["sadness"] = personality.pop("sadness", 0)
    emotions_dict["fear"] = personality.pop("fear", 0)
    return emotions_dict, personality


app.run()