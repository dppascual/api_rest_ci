#!/usr/bin/env python
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    """Item resource to manage requests belong to /item"""

    parser = reqparse.RequestParser()
    parser.add_argument(
            "price",
            type=float,
            required=True,
            help="This field cannot be left blank!"
            )

    def get(self, name):
        """method GET to send item back"""
        item = ItemModel.get_item(name)

        if item:
            return item.json()
        return {"message": "item not found"}, 404

    @jwt_required()
    def post(self, name):
        """method POST to create a new item"""
        row = ItemModel.get_item(name)
        if row:
            return {"message": "There is another item with this name"}, 422

        data = Item.parser.parse_args()
        item = ItemModel(name, data["price"])
        try:
            item.save_to_db()
        except:
            return {"message": "An error ocurred inserting the item."}, 500
        return item.json(), 200

    @jwt_required()
    def put(self, name):
        """method PUT to update or create an item"""
        data = Item.parser.parse_args()

        item = ItemModel.get_item(name)

        if item:
                item.price = data["price"]
        else:
                item = ItemModel(name, data["price"])
        try:
            item.save_to_db()
        except:
            return {"message": "An error ocurred inserting the item."}, 500
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        """method DELETE to remove an existing item"""
        item = ItemModel.get_item(name)

        if item:
            try:
                item.delete_from_db()
            except:
                return {"message": "An error ocurred trying to delete an item"}, 500
            return {"message:": "item has been deleted"}, 200
        return {"message": "item not found"}, 404


class ItemList(Resource):
    def get(self):
        """method GET to retrieve every item"""
        return {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}, 200
