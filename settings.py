from flask import Flask
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.dirname(os.path.abspath(__file__)) + '/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

