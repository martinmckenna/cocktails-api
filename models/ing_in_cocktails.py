from flask import Flask
from settings import db, ma

ing_in_cocktails = db.Table(
    'ing_in_cocktails',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('cocktail_id', db.Integer, db.ForeignKey('cocktails.id')),
    db.Column('ing_id', db.Integer, db.ForeignKey('ingredients.id'))
)
