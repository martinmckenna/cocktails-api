from settings import app
from flask import Flask
from routes.cocktails import cocktails
from routes.liquors import liquors

app.register_blueprint(cocktails)
app.register_blueprint(liquors)

app.run(port=5000, debug=True)
