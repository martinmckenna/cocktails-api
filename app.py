from flask import Flask, jsonify, request, Response

from models.cocktails import *
from settings import *
import json


@app.route('/cocktails')
def get_cocktails():
  return json.dumps(Cocktail.get_all_cocktails())


def validCocktailObject(cocktailObject):
  if("name" in cocktailObject):
    return True
  else:
    return False


def post_error_payload(error_text="Invalid Payload"):
    return Response(
        json.dumps({
            "error": error_text,
            "meta": 'Try following this format { "name": "my_cocktail" }'
        }),
        status=400,
        mimetype='application/json'
    )


@app.route('/cocktails', methods=['POST'])
def add_cocktail():
  try:
      request_data = request.get_json()
  except:
      return post_error_payload("Invalid JSON")
  if(validCocktailObject(request_data)):
    Cocktail.add_cocktail(request_data['name'])
    response = Response("", 200, mimetype='application/json')
    response.headers['Location'] = '/cocktails/'
    return response
  else:
    return post_error_payload()


app.run(port=5000, debug=True)
