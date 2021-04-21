# from flask_ngrok import run_with_ngrok
from flask import Flask
from flask import render_template
from flask import (
    redirect, request, url_for, request, session, flash
)
from TextPersonality import NLUPersonalityInterface
from StoreChars import DiscoveryCharDatabase, get_emotions_from_dict
from werkzeug.exceptions import InternalServerError
from chart import create_figure
import random
from forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_user,current_user, logout_user, login_required
from forms import RegistrationForm, LoginForm, UpdateAccountForm
from datetime import datetime
import secrets
import os
from PIL import Image

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
    texts = db.relationship('Text', backref='author', lazy=True) # can user text.author to get user info

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) # user input name
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False) #user input text to do analyze
    character_name = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    personality = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Text('{self.name}', '{self.date_posted}', '{self.content}','{self.character_name}','{self.title}','{self.personality}', '{self.user_id}')"


@app.route("/", methods=('GET', 'POST'))
def home(name=None):
    if request.method == 'POST':
        username = request.form['char_name']
        usertext = request.form['movie_name']
        notAllowed = ['\\','/','=','+','_','{','[',']','}','|','<','>']
        for e in notAllowed:
            if e in usertext:
                return render_template('invalid_char.html', error=e)
        return redirect(url_for('submit', username=username, usertext=usertext))
    return render_template('index.html', name=name)


@app.route("/submit/<username>/<usertext>")
def submit(username, usertext):
    file_name = "test_file.jpeg"
    # file_name2 = "test_file2.jpeg"
    file_name3 = "character_emotions.jpeg"
    # file_name4 = "character_concept.jpeg"
    ddb = DiscoveryCharDatabase("Collection 2")
    full_dict =  ddb.find_char(username,usertext)
    if full_dict == "Not in database":
        return render_template("error.html", error="Character not in Database")
    user_emotions, _ = get_emotions_from_dict(full_dict)
    create_figure(user_emotions, file_name)
    # create_figure(this_dict[1], file_name2)
    char_match, personality = ddb.search_char(full_dict,username.upper())
    if personality:
        sentences = personality.pop("sentences")
        if len(sentences) < 3:
            sentences = random.sample(sentences, 1)
        else:
            sentences = random.sample(sentences, 3)
    else:
        sentences = []
    book_title = personality.pop("title", "Unknown")
    personality.pop("char_name", "Unknown")
    emotions, concepts = get_emotions_from_dict(personality)
    create_figure(emotions, file_name3)
    # create_figure(personality, file_name4)
    if current_user.is_authenticated:
        text = Text(name=username, content=usertext, character_name=char_match, title=book_title, personality=''.join(personality), user_id=current_user.id)
        db.session.add(text)
        db.session.commit()
    return render_template('output.html', username=username, character_name=char_match, file_name=file_name, concepts=full_dict.keys(), file_name3=file_name3, char_concepts=personality.keys(), title=book_title, sentences=sentences)

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


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('account'))
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    texts = Text.query.filter_by(user_id = current_user.id).all()
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form, texts=texts)


@app.route("/about-us")
def about(name=None):
    return render_template('about.html', name=name)


@app.errorhandler(InternalServerError)
def handle_500(e):
    original = getattr(e, "original_exception", None)

    # if original is None:
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


if __name__ == "__main__":
    app.run()
