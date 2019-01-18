from flask import Flask
from settings import db, ma
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import fields

from utils.set_headers import send_400, send_200, send_404
from utils.check_for_duplicate import check_for_duplicate
from utils.validate_array import is_array_of_ints, list_contains_none_elements

from models.user_favorites import UserFavorites, UserFavoritesSchema
from models.cocktails import Cocktail


class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  public_id = db.Column(db.String(50), unique=True)
  name = db.Column(db.String(50))
  password = db.Column(db.String(80))
  admin = db.Column(db.Boolean)
  favorites = db.relationship(
      'UserFavorites',
      backref=db.backref('users', lazy='joined'),
      cascade='all, delete-orphan'
  )

  def get_all_users(name_filter=None):
    user_schema = UserSchema(strict=True, many=True)

    try:
      # if the client passed a name to search by, use that
      # otherise, return all users
      fetched_users = (
          User.query
          if name_filter is None
          else User.query.filter(User.name.like('%'+name_filter+'%'))
      )
      users = user_schema.dump(
          fetched_users.all()
      ).data
      return send_200({"users": users}, '/users/')
    except:
      return send_400('Something went wrong', 'Error fetching data', '/users/')

  def get_user_by_id(_id):
    user_schema = UserSchema(strict=True, many=True)
    fetched_user = user_schema.dump({
        User.query.filter_by(public_id=_id).first()
    }).data
    return (
        # if result is an array with 1 empty dict, there was no table row found
        send_404('/users/')
        if len(fetched_user[0]) == 0
        else send_200(fetched_user[0], '/users/')
    )

  def add_new_user(_name, _password):
    user_schema = UserSchema(strict=True, many=True)

    # SELECT from users where the name is equal to the passed name
    # and put inside a list. If list[0] is None, it means this is not a duplicate
    already_exists = check_for_duplicate(User, 'name', _name)
    if already_exists:
        return send_400('Invalid Payload', 'User already exists')

    hashed_password = generate_password_hash(_password, method='sha256')

    new_user = User(
        public_id=str(uuid.uuid4()),
        name=_name,
        password=hashed_password,
        admin=False
    )

    db.session.add(new_user)
    db.session.commit()

    return send_200(user_schema.dump([new_user]).data[0], '/users/')

  def add_cocktail_to_user(_pub_id, list_of_cocktails):
    user_schema = UserSchema(strict=True, many=True)
    
    fetched_user = User.query.filter_by(public_id=_pub_id).first()
      
    # user not found
    if fetched_user is None:
      return send_404('/user/' + str(_id))

    # validate we have an array of ints
    if not is_array_of_ints(list_of_cocktails):
      return send_400(meta="Please match the following format: { 'cocktails': [1, 2, 3] }")

    # validate each cocktail id exists in the DB
    cocktails_to_commit = User.generate_cocktails_to_add_to_user(list_of_cocktails)
    if list_contains_none_elements(cocktails_to_commit) is True:
      return send_400('Invalid payload', 'Invalid cocktail ID passed', '/users/')
    else:
      fetched_user.favorites = cocktails_to_commit
      db.session.commit()


    return send_200(user_schema.dump([fetched_user]).data, '/users/' + str(_pub_id))

  def promote_user_by_id(_id):
    user_schema = UserSchema(strict=True, many=True)
    """
    currently only has one feature - to promote user
    to be an admin user
    """
    try:
      fetched_user = User.query.filter_by(public_id=_id).first()

      # user not found
      if fetched_user is None:
        return send_404('/user/' + str(_id))

      # promote user to admin role
      fetched_user.admin = True
      db.session.commit()
      return send_200(user_schema.dump([fetched_user]).data[0], '/users/' + str(_id))
    except:
      return send_400('Something went wrong', 'Could not update user entry')

  def delete_user_by_id(_id):
    try:
      user_to_delete = User.query.filter_by(public_id=_id).first()
      if user_to_delete is None:
          return send_404('/user/' + str(_id))
      db.session.delete(user_to_delete)
      db.session.commit()
      return send_200({}, '/users/' + str(_id))
    except:
      return send_400('Something went wrong', 'Could not delete entry')

  def generate_cocktails_to_add_to_user(list_of_ids):
    """
    client passes an array of ints - by now, we've validated that
    we need to iterate over this list, get the cocktail from the DB
    and append it to a result array or None if the cocktail doesn't exist
    """

    i = 0
    result = []
    while i < len(list_of_ids):
      cocktail_to_add = Cocktail.query.filter_by(
          id=list_of_ids[i]).first()
      (
          result.append(
              UserFavorites(
                  cocktail_id=list_of_ids[i],
              )
          )
          if cocktail_to_add is not None
          else result.append(None)
      )
      i += 1
    return result

# Necessary for transforming sqlalchemy data into serialized JSON


class UserSchema(ma.ModelSchema):
    # this is responsible for returning all the favorites on the user payload
    favorites = ma.Nested(UserFavoritesSchema, many=True, strict=True)
    favorites = fields.Method('concat_cocktail_dicts')

    def concat_cocktail_dicts(self, obj):
        result_list = []
        i = 0
        while (i < len(obj.favorites)):
          result_list.append({
            'id': obj.favorites[i].cocktail.id,
            'name': obj.favorites[i].cocktail.name,
            'finish': obj.favorites[i].cocktail.finish,
            'glass': obj.favorites[i].cocktail.glass
          })
          i += 1
        
        return result_list

        # return {
        #     'name': obj.favorites.cocktail.name,
        #     'finish': obj.favorites.cocktail.finish,
        #     'glass': obj.favorites.cocktail.glass
        # }

    class Meta:
      model = User
      
