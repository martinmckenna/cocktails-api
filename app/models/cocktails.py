from flask import Flask
import json
from settings import db, ma
from sqlalchemy import and_, exists
from marshmallow import fields

from models.ing_in_cocktails import CocktailIngredient, CocktailIngredientSchema
from models.ingredients import Ingredient, IngredientSchema

from utils.set_headers import send_200, send_400, send_404
from utils.check_for_duplicate import check_for_duplicate
from utils.validate_array import list_contains_none_elements


class Cocktail(db.Model):
    __tablename__ = 'cocktails'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    glass = db.Column(db.String(20), nullable=False)
    finish = db.Column(db.String(20), nullable=True)
    ingredients = db.relationship(
        'CocktailIngredient',
        backref=db.backref('cocktails', lazy='joined'),
        cascade='all, delete-orphan'
    )

    def get_all_cocktails(
        name=None,
        ing_list=None,
        will_shop=False,
        _page=1,
        _page_size=25
    ):
      """
      gets all cocktails from cocktails DB along with the ingredients
      that go into the cocktail

      @param name: name of the cocktail to filter by (can be a partial match)
      
      @param ing_list: ingredients to filter by

      @param will_shop: if the client is willing to shop for more ingredients to make a
      cocktail. If this param is True and if the client passes "Gin" in the ing_list argument,
      then "Gin and Tonic" will return because the client is willing to go shopping for tonic.
      If False, passing "Gin" will not return "Gin And Tonic"
      """
      cocktail_schema = CocktailSchema(strict=True, many=True)
      base_query = Cocktail.query

      """
      check to see if client passed an ing_list to filter by
      and if they want more suggestions for cocktails that contain
      ingredients they don't own
      """
      if(ing_list is not None and will_shop is True):
          """
          this will return a cocktail as long as any of the ingredients passed are in the cocktail.
          So for example, if the client passed "Gin," then "Gin and Tonic" will return
          """
          base_query = Cocktail.query.join(
              CocktailIngredient
          ).filter(CocktailIngredient.ing_id.in_(ing_list))

      elif(ing_list is not None and will_shop is False):
          """
          this query will return a cocktail as long as the correct ingredients
          are passed. So for example, if the client passes 'Gin', 'Tonic', the
          "Gin and Tonic" cocktail will return. If the client only passes 'Gin',
          nothing will return. It's also worth nothing that if the client passes
          'Gin', 'Tonic', and 'Whiskey', 'Gin and Tonic' will still return
          """
          base_query = db.session.query(Cocktail).filter(
              ~exists().where(
                  and_(
                      CocktailIngredient.cocktail_id == Cocktail.id,
                      ~CocktailIngredient.ing_id.in_(ing_list)
                  )
              )
          )

      # if the client passed a name to search by, use that
      # otherise, return all cocktails
      fetched_cocktails_with_name = (
          base_query
          if name is None
          else base_query.filter(Cocktail.name.like('%'+name+'%'))
      )

      paginated_query = fetched_cocktails_with_name.paginate(page=_page, per_page=_page_size, error_out=False)

      return send_200({
          "data": cocktail_schema.dump(paginated_query.items).data,
          "pages": paginated_query.pages,
          "total_results": paginated_query.total
      }, '/cocktails/'
      )

    def get_cocktail_by_id(_id):
        cocktail_schema = CocktailSchema(strict=True, many=True)
        fetched_cocktail = cocktail_schema.dump({
            Cocktail.query.filter_by(id=_id).first()
        }).data
        return (
            # if result is an array with 1 empty dict, there was no table row found
            send_404('/cocktails/')
            if len(fetched_cocktail[0]) == 0
            else send_200(fetched_cocktail[0], '/cocktails/')
        )

    def add_cocktail(_name, _glass, ing_list, _finish=None):
        cocktail_schema = CocktailSchema(strict=True, many=True)
        new_cocktail = Cocktail(name=_name, glass=_glass, finish=_finish)

        # SELECT from ingredients where the name is equal to the passed name
        # and put inside a list. If list[0] is None, it means this is not a duplicate
        already_exists = check_for_duplicate(Cocktail, 'name', _name)
        if already_exists:
                return send_400(error='Cocktail already exists', field='name')

        if not ing_list_is_valid(ing_list):
          return send_400(
              error="Ingredient list invalid. Try the following format: " +
              "{ 'id': 1, 'ounces': 2.5, 'action': 'muddle', 'step': 1 }",
              field='ing_list'
          )

        ingredients_to_append = generate_ingredients_for_cocktail(ing_list)

        if list_contains_none_elements(ingredients_to_append) is True:
            return send_400(error='Invalid ingredient ID passed', location='/cocktails/', field='ing_list')
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
                return send_400(error='Cocktail already exists', field='name')

        # list of ingredients we want to add
        # check to see if client has passed ing_list and is not an empty array
        if ing_list is not None and type(ing_list) is list and len(ing_list) != 0:
           # ensure the ingredients is a list of dicts with the valid keys
            if not ing_list_is_valid(ing_list):
              return send_400(
                  error="Ingredient list invalid. Try the following format: " +
                  "{ 'id': 1, 'ounces': 2.5, 'action': 'muddle', 'step': 1 }",
                  field='ing_list'
              )

            ingredients_to_append = generate_ingredients_for_cocktail(ing_list)
            if list_contains_none_elements(ingredients_to_append) is True:
                return send_400(
                    error='Invalid ingredient ID passed',
                    location='/cocktails/',
                    field='ing_list'
                )
            else:
                target_cocktail.ingredients = ingredients_to_append

        # if client did not supply these keys in the PUT request, don't PUT them
        target_cocktail.name = _name if _name is not None else target_cocktail.name
        target_cocktail.glass = _glass if _glass is not None else target_cocktail.glass
        target_cocktail.finish = _finish if should_set_finish else target_cocktail.finish
        db.session.commit()

        return send_200(cocktail_schema.dump([target_cocktail]).data[0], '/cocktails/' + str(_id))

    def delete_cocktail_by_id(_id):
        cocktail_to_delete = Cocktail.query.filter_by(id=_id).first()
        if cocktail_to_delete is None:
            return send_404('/cocktails/' + str(_id))
        db.session.delete(cocktail_to_delete)
        db.session.commit()
        return send_200({}, '/cocktails/' + str(_id))


def generate_ingredients_for_cocktail(ing_list):
    # client passes an array of dicts:
    # [{
    #   "id": 1,
    #   "ounces": 2.5,
    #   "action": 'muddle',
    #   "step": 1
    # }]
    # map over that array
    # for each, validate
    # append the ingredient to the cocktail
    i = 0
    result = []
    while i < len(ing_list):
        ing_to_commit = Ingredient.query.filter_by(
            id=ing_list[i].get('id')).first()
        (
            result.append(
                CocktailIngredient(
                    ing_id=ing_to_commit.id,
                    ounces=ing_list[i].get('ounces'),
                    step=ing_list[i].get('step'),
                    action=ing_list[i].get('action')
                )
            )
            if ing_to_commit is not None
            else result.append(None)
        )
        i += 1
    return result


def ing_list_is_valid(ing_list):
  # checks to see if the list of ingredients is made up
  # of a dicts that have the following keys: id, ounces, action, and step

  results = []
  i = 0
  while i < len(ing_list):
    (
        results.append(True)
        if type(ing_list[i]) is dict
        and ing_list[i].get('id') is not None
        and ing_list[i].get('ounces') is not None
        and ing_list[i].get('action') is not None
        and ing_list[i].get('step') is not None
        else results.append(False)
    )
    i += 1
  return all(results)


# Necessary for transforming sqlalchemy data into serialized JSON
class CocktailSchema(ma.ModelSchema):
    # this is responsible for returning all the ingredient data on the cocktail
    ingredients = ma.Nested(CocktailIngredientSchema, many=True, strict=True)
    ingredients = fields.Method('concat_ingredients_dicts')

    """
    at this point the ingredients field on the cocktail object looks something like this

    ingredients: [{
        ingredient: {
            name: 'white russian',
            glass: 'rocks',
            finish: 'stirred'
        },
        ounces: 2,
        action: 'muddle',
        step: 1
    }]

    what we want is to concat this data so "ingredients" just turns
    into an list of dicts
    """
    def concat_ingredients_dicts(self, obj):
        result_ingredients_list = []
        i = 0
        while i < len(list(obj.ingredients)):
            # create a dict from the fields that live in the relational table
            relational_fields_dict = {
                'ounces': obj.ingredients[i].ounces,
                'action': obj.ingredients[i].action,
                'step': obj.ingredients[i].step
            }

            # create a dict from the fields on each ingredient in the cocktail
            ingredients_dict = obj.ingredients[i].ingredient.__dict__
            ingredients_dict_extracted_values = {
                'name': ingredients_dict.get('name'),
                'type': ingredients_dict.get('ing_type'),
                'id': ingredients_dict.get('id')
            }

            # merge the two dicts together
            merged = dict()
            merged.update(ingredients_dict_extracted_values)
            merged.update(relational_fields_dict)

            # append this merged dict a result array
            result_ingredients_list.append(merged)
            i += 1
        # return the array of ingredients
        return result_ingredients_list

    class Meta:
      model = Cocktail

