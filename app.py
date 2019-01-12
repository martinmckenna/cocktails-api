from settings import app
from flask import Flask
from routes.cocktails import cocktails
from routes.ingredients import ingredients

app.register_blueprint(cocktails)
app.register_blueprint(ingredients)

app.run(port=5000, debug=True)
