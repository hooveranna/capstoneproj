# capstoneproj
Capstone project, personality tester that will match your personality based on your text input with a personality of fictional character.

Need to install packages:
* Flask
* Numpy
* nltk (also need to download nltk data: punkt, maxent_ne_chunker, words, averaged_perceptron_tagger)
* ibm_watson
* ibm_cloud_sdk_core
* json
* pandas
* plotly
* kaleido
* beautiful soup
* Pillow
* WTForms
* flask_sqlalchemy
* flask_bcrypt
* flask_login
* flask_wtf

To initialize database, run in console:
from flask_app import db
db.create_all()