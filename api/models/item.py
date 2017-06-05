#!/usr/bin/env python
from db import db

class ItemModel(db.Model):
    """Internal representation of an item"""
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        """Create a JSON representation of an item"""
        return {
                "name": self.name,
                "price": self.price
                }

    @classmethod
    def get_item(cls, name):
        """Retrieve an item from the database"""
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name LIMIT 1

    def save_to_db(self):
        """Store an item to the database"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Delete an item from the database"""
        db.session.delete(self)
        db.session.commit()
