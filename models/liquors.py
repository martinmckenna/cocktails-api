from flask import Flask, jsonify
import json
from settings import db, ma

class Liquor(db.Model):
    __tablename__ = 'liquors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def add_liquor(_name):
        new_liquor = Liquor(name=_name)
        db.session.add(new_liquor)
        db.session.commit()

    def get_all_liquors():
      liquor_schema = LiquorSchema(strict=True, many=True)
      output = liquor_schema.dump(Liquor.query.all()).data
      return ({"liquors": output})

      # def __repr__(self):
      # return json.dumps({
      #     'id': self.id,
      #     'name': self.name
      # })


# Necessary for transforming sqlalchemy data into serialized JSON
class LiquorSchema(ma.ModelSchema):
    class Meta:
      model = Liquor
