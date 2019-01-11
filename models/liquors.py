from flask import Flask
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
        return ({
            "liquors": liquor_schema.dump(Liquor.query.all()).data
        })

    def get_liquor_by_id(_id):
        liquor_schema = LiquorSchema(strict=True, many=True)
        return liquor_schema.dump({
            Liquor.query.filter_by(id=_id).first()
        }).data

    def update_liquor_by_id(_id, _name):
        target_liquor = Liquor.query.filter_by(id=_id).first()
        target_liquor.name = _name
        db.session.commit()

    def delete_liquor_by_id(_id):
        Liquor.query.filter_by(id=_id).delete()
        db.session.commit()


# Necessary for transforming sqlalchemy data into serialized JSON
class LiquorSchema(ma.ModelSchema):
    class Meta:
      model = Liquor
