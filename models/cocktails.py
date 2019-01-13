from flask import Flask
from settings import db, ma
from sqlalchemy import and_

from models.ing_in_cocktails import ing_in_cocktails
from models.ingredients import Ingredient, IngredientSchema

from utils.set_headers import send_200, send_400, send_404
from utils.check_for_duplicate import check_for_duplicate


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
  
    def get_all_cocktails(name=None):
      cocktail_schema = CocktailSchema(strict=True, many=True)
      # will print kahluha
      # print(cocktails[0].ingredients[0].name)

      # this will return a cocktail as long as any of the ingredients are in it
      # but what we actually want is for a cocktail to be returned ONLY if we have provided
      # all the ingredients
      thing = Cocktail.query.join(ing_in_cocktails).filter(ing_in_cocktails.columns.ing_id.in_([1, 2]))
      print(thing)
      print(thing.all())

      try:
        # if the client passed a name to search by, use that
        # otherise, return all cocktails
        fetched_cocktails = (
            Cocktail.query
            if name is None
            else Cocktail.query.filter(Cocktail.name.like('%'+name+'%'))
        )
        return send_200({
            "cocktails": cocktail_schema.dump(fetched_cocktails.all()).data
        }, '/cocktails/'
        )
      except:
        return send_400('Something went wrong', 'Error fetching data', '/cocktails/')

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

        # SELECT from ingredients where the name is equal to the passed name
        # and put inside a list. If list[0] is None, it means this is not a duplicate
        already_exists = check_for_duplicate(Cocktail, 'name', _name)
        if already_exists:
                return send_400('Invalid Payload', 'Cocktail already exists')

        ingredients_to_append = generate_ingredients_for_cocktail(ing_list)

        if contains_invalid_ingredients(ingredients_to_append) is True:
            return send_400('Invalid payload', 'Invalid ingredient ID passed', '/cocktails/')
        else:
            new_cocktail.ingredients = ingredients_to_append

        db.session.add(new_cocktail)
        db.session.commit()

        return send_200(cocktail_schema.dump([new_cocktail]).data, '/cocktails/')

    def update_cocktail_by_id(_id, _name, _glass, ing_list, implicit_finish_null, _finish=None):
        cocktail_schema = CocktailSchema(strict=True, many=True)
        target_cocktail = Cocktail.query.filter_by(id=_id).first()

        if target_cocktail is None:
            return send_404('/cocktails/' + str(_id))

        should_set_finish = (
            True
            if (_finish is None and implicit_finish_null is True) or _finish is not None
            else False
        )

        # SELECT from ingredients where the name is equal to the passed name
        # and put inside a list. If list[0] is None, it means this is not a duplicate
        already_exists = check_for_duplicate(Cocktail, 'name', _name)
        if already_exists:
                return send_400('Invalid Payload', 'Cocktail already exists')

        # list of ingredients we want to add
        if ing_list is not None and len(ing_list) != 0:
            ingredients_to_append = generate_ingredients_for_cocktail(ing_list)
            if contains_invalid_ingredients(ingredients_to_append) is True:
                return send_400('Invalid payload', 'Invalid ingredient ID passed', '/cocktails/')
            else:
                target_cocktail.ingredients = ingredients_to_append

        # if client did not supply these keys in the PUT request, don't PUT them
        target_cocktail.name = _name if _name is not None else target_cocktail.name
        target_cocktail.glass = _glass if _glass is not None else target_cocktail.glass
        target_cocktail.finish = _finish if should_set_finish else target_cocktail.finish
        db.session.commit()

        return send_200(cocktail_schema.dump([target_cocktail]).data, '/cocktails/' + str(_id))

    def delete_cocktail_by_id(_id):
        try:
            cocktail_to_delete = Cocktail.query.filter_by(id=_id).first()
            if cocktail_to_delete is None:
                return send_404('/cocktails/' + str(_id))
            db.session.delete(cocktail_to_delete)
            db.session.commit()
            return send_200({}, '/cocktails/' + str(_id))
        except:
            return send_400('Something went wrong', 'Could not delete entry', '/cocktails/' + str(_id))


def generate_ingredients_for_cocktail(ing_list):
    # client passes an array of ids (ints)
    # map over that array
    # for each, get ingredient by ID
    # append the ingredient to the cocktail
    i = 0
    result = []
    while i < len(ing_list):
        # expecting an array of ingredient ids
        # @todo be able to pass multiple ids
        ing_to_commit = Ingredient.get_ingredient_by_id(ing_list[i])
        result.append(
            Ingredient.query.filter_by(id=ing_list[i]).first()
        )
        i += 1
    return result


def contains_invalid_ingredients(ing_list):
    return any(
        eachIngredient
        is None for eachIngredient
        in ing_list
    )



# Necessary for transforming sqlalchemy data into serialized JSON
class CocktailSchema(ma.ModelSchema):
    # this is responsible for returning all the ingredient data on the cocktail
    ingredients = ma.Nested(IngredientSchema, many=True, strict=True)

    class Meta:
      model = Cocktail
