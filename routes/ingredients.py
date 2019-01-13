from flask import Flask, jsonify, request, Response, Blueprint

from utils.set_headers import send_200, send_400, send_404
from utils.check_key_in_dict import value_in_dict_or_none

from settings import *
from models.ingredients import *
import json

ingredients = Blueprint('ingredients', __name__)


@ingredients.route('/ingredients')
def get_ingredients():
    # if a ?name="whatever" query string exists
    name_filter = request.args.get('name')
    return Ingredient.get_all_ingredients(name_filter)


@ingredients.route('/ingredients/<int:id>')
def get_ingredient(id):
  return Ingredient.get_ingredient_by_id(id)


@ingredients.route('/ingredients', methods=['POST'])
def add_ingredient():
  try:
      request_data = request.get_json()
  except:
      return post_error_payload("Invalid JSON")

  if(is_valid_ingredient_object(request_data)):
    return Ingredient.add_ingredient(request_data['name'], request_data['ing_type'])
  else:
    return post_error_payload()


@ingredients.route('/ingredients/<int:id>', methods=['PUT'])
def update_ingredient(id):
  try:
    request_data = request.get_json()
  except:
    return post_error_payload("Invalid JSON")

  # If the ingredient was not found in the DB, send a 404
  return Ingredient.update_ingredient_by_id(
      id,
      value_in_dict_or_none('name', request_data),
      value_in_dict_or_none('ing_type', request_data)
  )


@ingredients.route('/ingredients/<int:id>', methods=['DELETE'])
def delete_ingredient(id):
  return Ingredient.delete_ingredient_by_id(id)


def is_valid_ingredient_object(ingredient_object):
  # return true if we are passed "name" and "ing_type" keys in the dictionary
  return "name" in ingredient_object and "ing_type" in ingredient_object


def post_error_payload(error_text="Invalid Payload"):
  return send_400(
      {
          "error": error_text,
          "meta": "Try following this format { 'name': 'my_ingredient', 'ing_type': 'juice' }"
      }
  )
