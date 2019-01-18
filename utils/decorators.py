from flask import request
from functools import wraps
import jwt
from utils.set_headers import send_401
from settings import app

from models.users import User


def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = None

    if not 'x-access-token' in request.headers:
      return send_401(error='Auth token is missing')

    token = request.headers['x-access-token']

    try:
      data = jwt.decode(token, app.config['SECRET_KEY'])
      current_user = User.query.filter_by(public_id=data['public_id']).first()

      """
      not really sure how current_user ends up as none but need to document how to replicate
      """
      if current_user is None:
        return send_401(error='Invalid auth token')
    except:
      return send_401(error='Invalid auth token')

    return f(current_user, *args, **kwargs)

  return decorated
