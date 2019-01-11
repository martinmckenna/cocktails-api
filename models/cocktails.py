from flask import Flask
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
      return ({
          "cocktails": cocktail_schema.dump(Cocktail.query.all()).data
      })

    def get_cocktail_by_id(_id):
        cocktail_schema = CocktailSchema(strict=True, many=True)
        return cocktail_schema.dump({
            Cocktail.query.filter_by(id=_id).first()
        }).data

    def update_cocktail_by_id(_id, _name):
        target_cocktail = Cocktail.query.filter_by(id=_id).first()
        target_cocktail.name = _name
        db.session.commit()

    def delete_cocktail_by_id(_id):
        Cocktail.query.filter_by(id=_id).delete()
        db.session.commit()

# Necessary for transforming sqlalchemy data into serialized JSON


class CocktailSchema(ma.ModelSchema):
    class Meta:
      model = Cocktail
