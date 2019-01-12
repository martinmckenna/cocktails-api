from flask import Flask
from settings import db, ma


class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    ing_type = db.Column(db.String(20), nullable=False)

    def add_ingredient(_name, _type):
        new_ingredient = Ingredient(name=_name, ing_type=_type)
        db.session.add(new_ingredient)
        db.session.commit()

    def get_all_ingredients():
        ingredient_schema = IngredientSchema(strict=True, many=True)
        return ({
            "ingredients": ingredient_schema.dump(Ingredient.query.all()).data
        })

    def get_ingredient_by_id(_id):
        ingredient_schema = IngredientSchema(strict=True, many=True)
        return ingredient_schema.dump({
            Ingredient.query.filter_by(id=_id).first()
        }).data

    def update_ingredient_by_id(_id, _name, _type):
        target_ingredient = Ingredient.query.filter_by(id=_id).first()
        
        # set the new row cells if the client implicitly supplied these values
        target_ingredient.name = _name if _name is not None else target_ingredient.name
        target_ingredient.ing_type = _type if _type is not None else target_ingredient.ing_type
        db.session.commit()

    def delete_ingredient_by_id(_id):
        Ingredient.query.filter_by(id=_id).delete()
        db.session.commit()


# Necessary for transforming sqlalchemy data into serialized JSON
class IngredientSchema(ma.ModelSchema):
    class Meta:
      model = Ingredient
