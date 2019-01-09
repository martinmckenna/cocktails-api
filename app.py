from settings import *
from flask import Flask
from routes.cocktails import cocktails

app.register_blueprint(cocktails)

app.run(port=5000, debug=True)
