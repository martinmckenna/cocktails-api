from flask import Flask, request, Response, Blueprint
from settings import *
import json
import jwt
import datetime

from utils.set_headers import send_200, send_400, send_404, send_401
from utils.check_key_in_dict import value_in_dict_or_none
from utils.decorators import token_required

from models.users import *


users = Blueprint('users', __name__)


@users.route('/users')
@token_required
def get_users(current_user):
  if not current_user.admin:
    return send_401(location='/users/')
  # if a ?name="whatever" query string exists
  name_filter = request.args.get('name')

  try:
    page = int(request.args.get('page'))
  except:
    page = 1

  return User.get_all_users(name_filter=name_filter, _page=page)


@users.route('/users/<string:id>')
@token_required
def get_user(current_user, id):
  if not current_user.admin and not current_user.public_id == id:
    return send_401(location='/users/' + str(id))
  return User.get_user_by_id(id)


@users.route('/profile')
@token_required
def get_profile(current_user):
  if current_user.public_id is None:
    return send_401(location='/profile/')
  return User.get_user_by_id(current_user.public_id)


@users.route('/users', methods=['POST'])
def create_user():
  # check for valid JSON
  try:
      request_data = request.get_json()
  except:
      return post_error_payload(error_text="Invalid JSON")

  if request_data is None or not is_valid_user_object(request_data):
    return post_error_payload()

  """
  @todo
  1. Verify secure password
  """
  return User.add_new_user(
      _name=request_data['name'],
      _password=request_data['password'],
      _email=request_data['email']
  )


@users.route('/users/<string:id>', methods=['PUT'])
@token_required
def add_user_favorite(current_user, id):
  # only allow a user to add a favorite for themselves, unless they're an admin
  if not current_user.admin and not current_user.public_id == id:
    return send_401(location='/users/' + str(id))

  # check for valid JSON
  try:
    request_data = request.get_json()
  except:
    return put_error_payload(error_text="Invalid JSON")

  if request_data is None or not "cocktails" in request_data and is_valid_put_object(request_data):
    return put_error_payload()

  # at this point, we know we have an array of something
  return User.add_cocktail_to_user(id, value_in_dict_or_none('cocktails', request_data))


@users.route('/users/<string:id>/promote', methods=['PUT'])
@token_required
def update_user(current_user, id):
  if not current_user.admin:
    return send_401(location='/users/' + str(id) + '/promote/')
  return User.promote_user_by_id(id)


@users.route('/users/<string:id>', methods=['DELETE'])
@token_required
def delete_user(current_user, id):
  # only allow a user to delete themselves
  if not current_user.admin and not current_user.public_id == id:
    return send_401(location='/users/' + str(id))
  return User.delete_user_by_id(id)

@users.route('/login')
def login():
  auth = request.authorization

  # user did not supply a username and password
  if not auth or not auth.username or not auth.password:
    return send_400(error='Username or password not provided')

  user = User.query.filter_by(name=auth.username).first()

  # no user in the database
  if not user:
    return send_400(error='User does not exist')

  if check_password_hash(user.password, auth.password):
    # create our auth token
    token = jwt.encode({
        'public_id': user.public_id,
        'expiration': (datetime.datetime.utcnow() + datetime.timedelta(minutes=30)).isoformat(),
    }, app.config['SECRET_KEY']
    )

    return json.dumps({'token': token.decode('UTF-8')})

  # if passwords did not match
  return send_400(error='Password incorrect', field='password')

def is_valid_user_object(user_object):
  # return true if we are passed "name" and "ing_type" keys in the dictionary
  return "name" in user_object and "password" in user_object and "email" in user_object


def is_valid_put_object(put_object):
    return (
        False
        if put_object is None or len(put_object) == 0
        else True
    )


def post_error_payload(error_text="Invalid Payload", _path='/'):
  return send_400(error=error_text, location=_path)


def put_error_payload(error_text="Try following this format { 'cocktails': [1, 2, 3] }", path=''):
  return send_400(error=error_text, location=_path)
