from flask import Flask, jsonify, request, Response, Blueprint

from utils.set_headers import send_200

from settings import *
from models.cocktails import *
import json

cocktails = Blueprint('cocktails', __name__)


@cocktails.route('/cocktails')
def get_cocktails():
  return send_200(json.dumps(Cocktail.get_all_cocktails()))


def validCocktailObject(cocktailObject):
  # If "name" property is in the JSON object, return true
  return "name" in cocktailObject


def post_error_payload(error_text="Invalid Payload"):
    return Response(
        json.dumps({
            "error": error_text,
            "meta": 'Try following this format { "name": "my_cocktail" }'
        }),
        status=400,
        mimetype='application/json'
    )


@cocktails.route('/cocktails', methods=['POST'])
def add_cocktail():
  try:
      request_data = request.get_json()
  except:
      return post_error_payload("Invalid JSON")
  if(validCocktailObject(request_data)):
    Cocktail.add_cocktail(request_data['name'])
    return send_200({})
  else:
    return post_error_payload()
