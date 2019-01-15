from flask import Flask
from settings import db, ma
from marshmallow import fields

from models.ingredients import Ingredient, IngredientSchema

class CocktailIngredient(db.Model):
    __tablename__ = 'ings_in_cocktail'
    ing_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), primary_key=True)
    cocktail_id = db.Column(db.Integer, db.ForeignKey('cocktails.id'), primary_key=True)
    ounces = db.Column(db.Float, nullable=False)
    action = db.Column(db.String(20), nullable=False)
    step = db.Column(db.Integer, nullable=False)

    ingredient = db.relationship(
        'Ingredient',
        backref=db.backref('ings_in_cocktail', lazy='joined', cascade='delete'),
    )

# Necessary for transforming sqlalchemy data into serialized JSON


class CocktailIngredientSchema(ma.ModelSchema):
    action = fields.String()
    ingredient = ma.Nested(IngredientSchema, strict=True)
    # ingredient = fields.Method("get_ingredients")

    # def get_ingredients(self, obj):
    #     print(obj.ingredients)
    #     return {**obj, **obj.ingredient}

    class Meta:
      model = CocktailIngredient
