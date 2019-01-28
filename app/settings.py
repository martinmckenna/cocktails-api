from flask import Flask
import os
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import create_database, database_exists
from flask_cors import CORS

app = Flask(__name__)
# prevent CORS errors
CORS(app)

url = 'mysql+pymysql://marty:h&PT93QX6SibJf#@db:3306/drinks'

# url = 'mysql+pymysql://root:PiercetheSQL.14@127.0.0.1/hosting'

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_SIZE'] = 100
app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
app.url_map.strict_slashes = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

from models.cocktails import Cocktail
from models.ingredients import Ingredient
from models.users import User

if not database_exists(url): 
  create_database(url)

db.create_all()
db.session.commit()