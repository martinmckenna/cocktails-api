from settings import app
from flask import Flask
from routes.cocktails import cocktails
from routes.ingredients import ingredients
from routes.users import users

app.register_blueprint(cocktails)
app.register_blueprint(ingredients)
app.register_blueprint(users)

app.run(host='0.0.0.0')
