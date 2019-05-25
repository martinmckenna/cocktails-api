from flask import Flask, request, Response, Blueprint

from utils.set_headers import send_400, send_401
from utils.check_key_in_dict import value_in_dict_or_none
from utils.convert_to_array import convert_to_array_of_ints
from utils.decorators import token_required

from settings import *
from models.cocktails import *

cocktails = Blueprint('cocktails', __name__)


@cocktails.route('/cocktails')
def get_cocktails():
  # if a ?name="whatever" query string exists
  name_filter = request.args.get('name')
  ing_list_filter = request.args.get('ing_list')
  # only set will_shop_filter if the client send "true" in the query string
  will_shop_filter = (
      True
      if request.args.get('will_shop') == 'true'
      else False
  )
  try:
    ing_list_as_array_of_ints = (
        None
        if ing_list_filter is None
        else convert_to_array_of_ints(ing_list_filter)
    )
  except:
    return send_400(error='ing_list param must be a string of numbers seperated by a string: (e.g: 1,2,3)')

  try:
    page = int(request.args.get('page'))
  except:
    page = 1

  return Cocktail.get_all_cocktails(
      name=name_filter,
      will_shop=will_shop_filter,
      ing_list=ing_list_as_array_of_ints,
      _page=page
  )


@cocktails.route('/cocktails/<int:id>')
def get_cocktail(id):
  return Cocktail.get_cocktail_by_id(id)


@cocktails.route('/cocktails', methods=['POST'])
@token_required
def add_cocktail(current_user):
  if not current_user.admin:
    return send_401(location='/cocktails/')
  # check for valid JSON
  try:
      request_data = request.get_json()
  except:
      return send_400(error="Invalid JSON")

  # if the user passed a "finish" key, make sure it's value is correct
  if request_data is None or 'finish' in request_data and not is_valid_finish_string(request_data['finish'], True):
    return send_400(error="The 'finish' key must either be 'shaken', 'stirred', 'stirred with ice', or 'shaken with ice'", field='finish')

  # finally, if we have the "name" and "glass" keys, update the DB
  if(is_valid_cocktail_object(request_data)):
    return Cocktail.add_cocktail(
        request_data['name'],
        request_data['glass'],
        request_data['ingredients'],
        value_in_dict_or_none('finish', request_data)
    )
  else:
    return send_400()


@cocktails.route('/cocktails/<int:id>', methods=['PUT'])
@token_required
def update_cocktail(current_user, id):
  if not current_user.admin:
    return send_401(location='/cocktails/' + str(id))
  try:
    request_data = request.get_json()
  except:
    return send_400(error="Invalid JSON")

  # if the user passed a "finish" key, make sure it's value is correct
  if request_data is None or 'finish' in request_data and not is_valid_finish_string(request_data['finish'], True):
    return send_400(error="The 'finish' key must either be 'shaken' or 'stirred'", field='finish')

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
@token_required
def delete_cocktail(current_user, id):
  if not current_user.admin:
    return send_401(location='/cocktails/' + str(id))
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
  lowercase_finish = finish.lower()
  allowed_values = ['shaken', 'stirred', 'stirred with ice', 'shaken with ice']
  print(lowercase_finish in allowed_values)
  return lowercase_finish in allowed_values or is_null_and_allowed


def is_valid_array_of_ingredients(ing_list):
  return (
      False
      if type(ing_list) is not list or ing_list is None or len(ing_list) == 0
      else True
  )
