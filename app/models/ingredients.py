from flask import Flask
from settings import db, ma

from utils.set_headers import send_200, send_400, send_404
from utils.check_for_duplicate import check_for_duplicate


class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    ing_type = db.Column(db.String(20), nullable=False)

    def get_all_ingredients(name=None):
        ingredient_schema = IngredientSchema(strict=True, many=True)

        try:
            # if the client passed a name to search by, use that
            # otherise, return all ingredients
            fetched_ingredients = (
                Ingredient.query
                if name is None
                else Ingredient.query.filter(Ingredient.name.like('%'+name+'%'))
            )
            ingredients = ingredient_schema.dump(
                fetched_ingredients.all()).data
            return send_200({"ingredients": ingredients}, '/ingredients/')
        except:
            return send_400('Something went wrong', 'Error fetching data', '/ingredients/')

    def get_ingredient_by_id(_id):
        ingredient_schema = IngredientSchema(strict=True, many=True)
        fetched_ingredient = ingredient_schema.dump({
            Ingredient.query.filter_by(id=_id).first()
        }).data
        return (
            # if result is an array with 1 empty dict, there was no table row found
            send_404('/ingredients/')
            if len(fetched_ingredient[0]) == 0
            else send_200(fetched_ingredient[0], '/ingredients/')
        )

    def add_ingredient(_name, _type):
        ingredient_schema = IngredientSchema(strict=True, many=True)
        new_ingredient = Ingredient(name=_name, ing_type=_type)

        try:
            # SELECT from ingredients where the name is equal to the passed name
            # and put inside a list. If list[0] is None, it means this is not a duplicate
            already_exists = check_for_duplicate(Ingredient, 'name', _name)
            if already_exists:
                return send_400('Invalid Payload', 'Ingredient already exists')
            db.session.add(new_ingredient)
            db.session.commit()
            return send_200(ingredient_schema.dump([new_ingredient]).data[0], '/ingredients/')
        except:
            return send_400('Something went wrong', 'Error fetching data', '/ingredients/')

    def update_ingredient_by_id(_id, _name, _type):
        ingredient_schema = IngredientSchema(strict=True, many=True)
        target_ingredient = Ingredient.query.filter_by(id=_id).first()

        # ingredient could not be found in the DB
        if target_ingredient is None:
            return send_404('/ingredients/' + str(id))

        # SELECT from ingredients where the name is equal to the passed name
        # and put inside a list. If list[0] is None, it means this is not a duplicate
        already_exists = check_for_duplicate(Ingredient, 'name', _name)
        if already_exists:
            return send_400('Invalid Payload', 'Ingredient already exists')

        # set the new row cells if the client implicitly supplied these values
        target_ingredient.name = _name if _name is not None else target_ingredient.name
        target_ingredient.ing_type = _type if _type is not None else target_ingredient.ing_type
        db.session.commit()

        return send_200(ingredient_schema.dump([target_ingredient]).data[0], '/ingredients/' + str(_id))

    def delete_ingredient_by_id(_id):
        try:
            ingredient_to_delete = Ingredient.query.filter_by(id=_id).first()
            if ingredient_to_delete is None:
                return send_404('/ingredient/' + str(_id))
            db.session.delete(ingredient_to_delete)
            db.session.commit()
            return send_200({}, '/ingredients/' + str(_id))
        except:
            return send_400('Something went wrong', 'Could not delete entry')

# Necessary for transforming sqlalchemy data into serialized JSON


class IngredientSchema(ma.ModelSchema):
    class Meta:
      model = Ingredient
