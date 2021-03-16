# from flask_ngrok import run_with_ngrok
from flask import Flask
from flask import render_template
from flask import (
    redirect, request, url_for, request, session, flash
)
from TextPersonality import NLUPersonalityInterface
from StoreChars import DiscoveryCharDatabase
from werkzeug.exceptions import InternalServerError
from chart import create_figure
import time
import random
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_user,current_user, logout_user, login_required

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
app.config['SECRET_KEY'] = 'my precious'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
# run_with_ngrok(app)   # starts ngrok when the app is run

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    #posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

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
        sentences = []
    book_title = personality.pop("title", "Unknown")
    emotions, concepts = get_emotions_from_dict(personality)
    create_figure(emotions, file_name3)
    # create_figure(personality, file_name4)
    return render_template('output.html', username=username, character_name=char_match, file_name=file_name, concepts=this_dict[1].keys(), file_name3=file_name3, char_concepts=personality.keys(), title=book_title, sentences=sentences)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
         return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


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
# if __name__ == '__main__':
#     app.run()
