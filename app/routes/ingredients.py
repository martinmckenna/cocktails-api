from flask import Flask, request, Response, Blueprint

from utils.set_headers import send_400
from utils.check_key_in_dict import value_in_dict_or_none
from utils.decorators import token_required

from settings import *
from models.ingredients import *
import json

ingredients = Blueprint('ingredients', __name__)


@ingredients.route('/ingredients')
def get_ingredients():
    # if a ?name="whatever" query string exists
    name_filter = request.args.get('name')
    try:
      page = int(request.args.get('page'))
    except:
      page = 1

    return Ingredient.get_all_ingredients(name_filter, _page=page)


@ingredients.route('/ingredients/<int:id>')
def get_ingredient(id):
  return Ingredient.get_ingredient_by_id(id)


@ingredients.route('/ingredients', methods=['POST'])
@token_required
def add_ingredient(current_user):
  if not current_user.admin:
    return send_401(location='/ingredients/')
  try:
      request_data = request.get_json()
  except:
      return post_error_payload("Invalid JSON")

  if request_data is None or not is_valid_ingredient_object(request_data):
    return post_error_payload()

  return Ingredient.add_ingredient(request_data['name'], request_data['ing_type'])


@ingredients.route('/ingredients/<int:id>', methods=['PUT'])
@token_required
def update_ingredient(current_user, id):
  if not current_user.admin:
    return send_401(location='/ingredients/' + str(id))
  try:
    request_data = request.get_json()
  except:
    return post_error_payload("Invalid JSON")

  if request_data is None:
    return post_error_payload('Invalid JSON')

  # If the ingredient was not found in the DB, send a 404
  return Ingredient.update_ingredient_by_id(
      id,
      value_in_dict_or_none('name', request_data),
      value_in_dict_or_none('ing_type', request_data)
  )


@ingredients.route('/ingredients/<int:id>', methods=['DELETE'])
@token_required
def delete_ingredient(current_user, id):
  if not current_user.admin:
    return send_401(location='/ingredients/' + str(id))

  return Ingredient.delete_ingredient_by_id(id)


def is_valid_ingredient_object(ingredient_object):
  # return true if we are passed "name" and "ing_type" keys in the dictionary
  return "name" in ingredient_object and "ing_type" in ingredient_object


def post_error_payload(error_text="Invalid Payload", path='/'):
  return send_400(error_text, "Try following this format { 'name': 'my_ingredient', 'ing_type': 'juice' }", path)
