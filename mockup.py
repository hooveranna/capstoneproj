# -*- coding: utf-8 -*-
"""Mockup.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lucJiMQUyLmduJ8yu98m3OqoVbukAzSU
"""

from flask_ngrok import run_with_ngrok
from flask import Flask
from flask import render_template
from flask import (
    redirect, request, url_for
)

app = Flask(__name__)
run_with_ngrok(app)   #starts ngrok when the app is run
@app.route("/", methods=('GET','POST'))
def home(name=None):
    if request.method == 'POST':
      return redirect(url_for('submit'))  
    return render_template('index.html', name=name)

@app.route("/submit")
def submit(name=None):
  return render_template('output.html', name=name)


app.run()