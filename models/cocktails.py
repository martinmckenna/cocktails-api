from flask import Flask, jsonify
import json
from settings import db, ma

class Cocktail(db.Model):
    __tablename__ = 'cocktails'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def add_cocktail(_name):
        new_cocktail = Cocktail(name=_name)
        db.session.add(new_cocktail)
        db.session.commit()

    def get_all_cocktails():
      cocktail_schema = CocktailSchema(strict=True, many=True)
      output = cocktail_schema.dump(Cocktail.query.all()).data
      return ({"cocktails": output})

      # def __repr__(self):
      # return json.dumps({
      #     'id': self.id,
      #     'name': self.name
      # })


# Necessary for transforming sqlalchemy data into serialized JSON
class CocktailSchema(ma.ModelSchema):
    class Meta:
      model = Cocktail
