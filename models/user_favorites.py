from flask import Flask
from settings import db, ma
from marshmallow import fields

from models.cocktails import Cocktail, CocktailSchema

class UserFavorites(db.Model):
    __tablename__ = 'user_favorites'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    cocktail_id = db.Column(db.Integer, db.ForeignKey('cocktails.id'), primary_key=True)

    cocktail = db.relationship(
        'Cocktail',
        backref=db.backref('user_favorites', lazy='joined', cascade='delete'),
    )

# Necessary for transforming sqlalchemy data into serialized JSON


class UserFavoritesSchema(ma.ModelSchema):
    cocktail = ma.Nested(CocktailSchema, strict=True)

    class Meta:
      model = UserFavorites
