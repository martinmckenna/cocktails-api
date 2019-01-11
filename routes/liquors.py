from flask import Flask, jsonify, request, Response, Blueprint

from utils.set_headers import send_200, send_400

from settings import *
from models.liquors import *
import json

liquors = Blueprint('liquors', __name__)


@liquors.route('/liquors')
def get_liquors():
    return send_200(Liquor.get_all_liquors())


def validLiquorObject(liquorObject):
  # return true if we are passed a "name" key in the dictionary
  return "name" in liquorObject


def post_error_payload(error_text="Invalid Payload"):
  return send_400(
      {
          "error": error_text,
          "meta": 'Try following this format { "name": "my_liquor" }'
      }
  )


@liquors.route('/liquors', methods=['POST'])
def add_liquor():
  try:
      request_data = request.get_json()
  except:
      return post_error_payload("Invalid JSON")
  if(validLiquorObject(request_data)):
    Liquor.add_liquor(request_data['name'])
    return send_200({})
  else:
    return post_error_payload()


@liquors.route('/liquors/<int:id>', methods=['PUT'])
def update_liquor(id):
  try:
    request_data = request.get_json()
  except:
    return post_error_payload("Invalid JSON")
  if(validLiquorObject(request_data)):
    Liquor.update_liquor_by_id(id, request_data['name'])
    return send_200(Liquor.get_liquor_by_id(id))
  else:
    return post_error_payload()
