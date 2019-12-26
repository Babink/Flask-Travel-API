from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt
)
from passlib.hash import pbkdf2_sha256 as sha256
from models.BusModel import JSONEncoder
import json
from bson.objectid import ObjectId


class UserModel:
    username = ""
    email = ""
    password = ""

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def get_single_user(username):
        from app import db

        try:
            user = db.db.User.find_one({
                "username": username
            })

            user_data = {
                "_id": JSONEncoder().encode(user["_id"]),
                "username": user["username"],
                "email": user["email"],
                "password": user["password"]
            }

            return {
                "message": "Success",
                "data": user_data
            }

        except:
            return None

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_password(password, hash_password):
        return sha256.verify(password, hash_password)

    def create_accout(self):
        from app import db
        # get single user
        # if there's account , reject creating account and return message
        # otherwise create account

        user = self.get_single_user(self.username)

        if user == None:
            access_token = create_access_token(identity=self.username)
            refresh_token = create_refresh_token(identity=self.username)

            data = {
                "username": self.username,
                "email": self.email,
                "password": self.generate_hash(self.password)
            }

            try:
                db.db.User.insert_one(data)
                return {
                    "message": "Successfully Created User: {}".format(self.username),
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }

            except:
                return "Error while creating user account"
        else:
            return "User Already Exist with Name: {}".format(self.username)

    def login_user(self):
        from app import db

        user = self.get_single_user(self.username)
        if user == None:
            return user

        else:
            verify_user = self.verify_password(
                self.password, user["data"]["password"])
            return verify_user

    @staticmethod
    def get_all_user():
        from app import db
        all_user = []

        try:
            users = db.db.User.find()

            for user in users:
                data = {
                    "_id": JSONEncoder().encode(user["_id"]),
                    "username": user["username"],
                    "email": user["email"],
                    "password": user["password"]
                }

                all_user.append(data)

            return all_user

        except:
            return "Error while searching user"

    @staticmethod
    def delete_account(_id):
        from app import db

        try:
            db.db.User.delete_one({
                "_id": ObjectId(_id)
            })

            return "Successfully deleted User: {}".format(_id)

        except:
            return "Error while deleting user"
