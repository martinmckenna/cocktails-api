from flask import Flask
from settings import db, ma

from models.ing_in_cocktails import ing_in_cocktails
from models.ingredients import Ingredient, IngredientSchema

from utils.set_headers import send_200, send_400, send_404


class Cocktail(db.Model):
    __tablename__ = 'cocktails'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    glass = db.Column(db.String(20), nullable=False)
    finish = db.Column(db.String(20), nullable=True)
    ingredients = db.relationship(
        'Ingredient',
        secondary=ing_in_cocktails,
        backref=db.backref('cocktails', lazy='dynamic')
    )

    def get_all_cocktails():
      cocktail_schema = CocktailSchema(strict=True, many=True)
      cocktails = Cocktail.query.all()
      # will print kahluha
      print(cocktails[0].ingredients[0].name)

      try:
        cocktails = Cocktail.query.all()
        return send_200({
            "cocktails": cocktail_schema.dump(cocktails).data
        }, '/cocktails/'
        )
      except:
        return send_400({
            'error': 'Error fetching data'
        }, '/cocktails/')

    def get_cocktail_by_id(_id):
        cocktail_schema = CocktailSchema(strict=True, many=True)
        fetched_cocktail = cocktail_schema.dump({
            Cocktail.query.filter_by(id=_id).first()
        }).data
        return (
            # if result is an array with 1 empty dict, there was no table row found
            send_404('/cocktails/')
            if len(fetched_cocktail[0]) == 0
            else send_200(fetched_cocktail, '/cocktails/')
        )

    def add_cocktail(_name, _glass, ing_list, _finish=None):
        cocktail_schema = CocktailSchema(strict=True, many=True)
        new_cocktail = Cocktail(name=_name, glass=_glass, finish=_finish)

        # client passes an array of ids (ints)
        # map over that array
        # for each, get ingredient by ID
        # append the ingredient to the cocktail
        i = 0
        while i < len(ing_list):
            # expecting an array of ingredient ids
            # @todo be able to pass multiple ids
            ing_to_commit = Ingredient.get_ingredient_by_id(ing_list[i])
            new_cocktail.ingredients.append(
                Ingredient.query.filter_by(id=ing_list[i]).first()
            )
            i += 1

        # handle path of ingredients being empty
        has_invalid_ingredients = any(
            eachIngredient
            is None for eachIngredient
            in new_cocktail.ingredients
        )
        if has_invalid_ingredients is True:
            return send_400({
                'error': 'Invalid Payload',
                'meta': 'Invalid ingredient ID passed'
            }, '/cocktails/')

        db.session.add(new_cocktail)
        db.session.commit()

        return send_200(cocktail_schema.dump([new_cocktail]).data, '/cocktails/')

    def update_cocktail_by_id(_id, _name, _glass, implicit_finish_null, _finish=None):
        cocktail_schema = CocktailSchema(strict=True, many=True)
        target_cocktail = Cocktail.query.filter_by(id=_id).first()

        if target_cocktail is None:
            return send_404('/cocktails/' + str(_id))

        should_set_finish = (
            True
            if (_finish is None and implicit_finish_null is True) or _finish is not None
            else False
        )

        # if client did not supply these keys in the PUT request, don't PUT them
        target_cocktail.name = _name if _name is not None else target_cocktail.name
        target_cocktail.glass = _glass if _glass is not None else target_cocktail.glass
        target_cocktail.finish = _finish if should_set_finish else target_cocktail.finish
        db.session.commit()

        return send_200(cocktail_schema.dump([target_cocktail]).data, '/cocktails/' + str(_id))

    def delete_cocktail_by_id(_id):
        try:
            Cocktail.query.filter_by(id=_id).delete()
            db.session.commit()
        except:
            send_400({
                'error': 'Something went wrong',
                'meta': 'Could not delete entry'
            })


# Necessary for transforming sqlalchemy data into serialized JSON


class CocktailSchema(ma.ModelSchema):
    # this is responsible for returning all the ingredient data on the cocktail
    ingredients = ma.Nested(IngredientSchema, many=True, strict=True)

    class Meta:
      model = Cocktail
