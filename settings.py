from flask import Flask
import os
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import create_database, database_exists

app = Flask(__name__)

url = 'mysql+pymysql://root:PiercetheSQL.14@127.0.0.1/hosting'

app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

from models.cocktails import Cocktail
from models.liquors import Liquor

if not database_exists(url): 
  print('no database!')
  create_database(url)
else:
  print('else')

db.create_all()
db.session.commit()

