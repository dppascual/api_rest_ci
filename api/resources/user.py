#!/usr/bin/env python
import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    """Register resource to sign up"""

    parser = reqparse.RequestParser()
    parser.add_argument(
            "username",
            type=str,
            required=True,
            help="The username field cannot be left blank!"
            )
    parser.add_argument(
            "password",
            type=str,
            required=True,
            help="The password field cannot be left blank!"
            )

    def post(self):
        """method POST to create a new user"""
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "User already exists with this name."}, 422

        try:
            UserModel(**data).save_to_db()
        except:
            return {"message": "An error ocurred inserting a new user."}, 500
        return {"message": "User has been created succesfully."}, 201
