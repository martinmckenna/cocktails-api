from flask import Flask
from settings import db, ma


class Cocktail(db.Model):
    __tablename__ = 'cocktails'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    glass = db.Column(db.String(20), nullable=False)
    finish = db.Column(db.String(20), nullable=True)

    def add_cocktail(_name, _glass, _finish=None):
        new_cocktail = Cocktail(name=_name, glass=_glass, finish=_finish)
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

    def update_cocktail_by_id(_id, _name, _glass, implicit_finish_null, _finish=None):
        target_cocktail = Cocktail.query.filter_by(id=_id).first()
        
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

    def delete_cocktail_by_id(_id):
        Cocktail.query.filter_by(id=_id).delete()
        db.session.commit()

# Necessary for transforming sqlalchemy data into serialized JSON


class CocktailSchema(ma.ModelSchema):
    class Meta:
      model = Cocktail
