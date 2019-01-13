from flask import Flask, request, Response, Blueprint

from utils.set_headers import send_200, send_400, send_404
from utils.check_key_in_dict import value_in_dict_or_none

from settings import *
from models.cocktails import *

cocktails = Blueprint('cocktails', __name__)


@cocktails.route('/cocktails')
def get_cocktails():
  # if a ?name="whatever" query string exists
  name_filter = request.args.get('name')
  return Cocktail.get_all_cocktails(name_filter)


@cocktails.route('/cocktails/<int:id>')
def get_cocktail(id):
  return Cocktail.get_cocktail_by_id(id)


@cocktails.route('/cocktails', methods=['POST'])
def add_cocktail():
  # check for valid JSON
  try:
      request_data = request.get_json()
  except:
      return post_error_payload("Invalid JSON")

  # if the user passed a "finish" key, make sure it's value is correct
  if 'finish' in request_data and not is_valid_finish_string(request_data['finish']):
    return post_error_payload("The 'finish' key must either be 'shaken' or 'stirred'")

  # finally, if we have the "name" and "glass" keys, update the DB
  if(is_valid_cocktail_object(request_data)):
    return Cocktail.add_cocktail(
        request_data['name'],
        request_data['glass'],
        request_data['ingredients'],
        value_in_dict_or_none('finish', request_data)
    )
  else:
    return post_error_payload()


@cocktails.route('/cocktails/<int:id>', methods=['PUT'])
def update_cocktail(id):
  try:
    request_data = request.get_json()
  except:
    return post_error_payload("Invalid JSON")

  # if the user passed a "finish" key, make sure it's value is correct
  if 'finish' in request_data and not is_valid_finish_string(request_data['finish'], True):
    return post_error_payload("The 'finish' key must either be 'shaken' or 'stirred'")

  # allow the client to implicitly change the finish to "null"
  # if they're sending the key in the request
  implicit_finish_null = (
      True
      if 'finish' in request_data and request_data['finish'] is None
      else False
  )

  # If the cocktail was not found in the DB, send a 404
  return Cocktail.update_cocktail_by_id(
      id,
      value_in_dict_or_none('name', request_data),
      value_in_dict_or_none('glass', request_data),
      value_in_dict_or_none('ingredients', request_data),
      implicit_finish_null,
      value_in_dict_or_none('finish', request_data),
  )


@cocktails.route('/cocktails/<int:id>', methods=['DELETE'])
def delete_cocktail(id):
  return Cocktail.delete_cocktail_by_id(id)


def is_valid_cocktail_object(cocktail_object):
  return (
      "name" in cocktail_object
      and "glass" in cocktail_object
      and "ingredients" in cocktail_object
      and is_valid_array_of_ingredients(cocktail_object['ingredients'])
  )


def is_valid_finish_string(finish, null_allowed=False):
  # ensure finish is 'shaken' or 'stirred'
  # also, if we are allowing an implicit None, let the validation pass
  is_null_and_allowed = True if (
      finish is None and null_allowed is True) else False
  return finish == 'shaken' or finish == 'stirred' or is_null_and_allowed


def is_valid_array_of_ingredients(ing_list):
  return (
      False
      if ing_list is None or len(ing_list) == 0
      else True
  )


def post_error_payload(error_text="Invalid Payload", path='/'):
  return send_400(
      error_text,
      "Try following this format " +
      "{ 'name': 'my_cocktail', 'glass': 'rocks', 'finish': 'shaken', ing_list: [0, 1] }",
      path
  )
