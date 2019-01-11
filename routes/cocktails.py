from flask import Flask, request, Response, Blueprint

from utils.set_headers import send_200, send_400

from settings import *
from models.cocktails import *

cocktails = Blueprint('cocktails', __name__)


@cocktails.route('/cocktails')
def get_cocktails():
  return send_200(Cocktail.get_all_cocktails())


def validCocktailObject(cocktailObject):
  return "name" in cocktailObject


def post_error_payload(error_text="Invalid Payload"):
  return send_400(
      {
          "error": error_text,
          "meta": 'Try following this format { "name": "my_cocktail" }'
      }
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


@cocktails.route('/cocktails/<int:id>', methods=['PUT'])
def update_cocktail(id):
  try:
    request_data = request.get_json()
  except:
    return post_error_payload("Invalid JSON")
  if(validCocktailObject(request_data)):
    Cocktail.update_cocktail_by_id(id, request_data['name'])
    return send_200(Cocktail.get_cocktail_by_id(id))
  else:
    return post_error_payload()
