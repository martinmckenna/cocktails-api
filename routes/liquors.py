from flask import Flask, jsonify, request, Response, Blueprint

from settings import *
from models.liquors import *
import json

liquors = Blueprint('liquors', __name__)


@liquors.route('/liquors')
def get_liquors():
  return json.dumps(Liquor.get_all_liquors())


def validLiquorObject(liquorObject):
  if("name" in liquorObject):
    return True
  else:
    return False


def post_error_payload(error_text="Invalid Payload"):
    return Response(
        json.dumps({
            "error": error_text,
            "meta": 'Try following this format { "name": "my_liquor" }'
        }),
        status=400,
        mimetype='application/json'
    )


@liquors.route('/liquors', methods=['POST'])
def add_liquor():
  try:
      request_data = request.get_json()
  except:
      return post_error_payload("Invalid JSON")
  if(validLiquorObject(request_data)):
    Liquor.add_liquor(request_data['name'])
    response = Response("", 200, mimetype='application/json')
    response.headers['Location'] = '/liquors/'
    return response
  else:
    return post_error_payload()
