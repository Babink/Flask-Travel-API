from flask_restful import Resource, reqparse
from models.UserModel import UserModel
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt
)
from blacklist import BlackList


class User(Resource):
    def get(self):
        users = UserModel.get_all_user()
        return users if len(users) >= 1 else "No User In Database"

    # Register user
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "username",
            type=str,
            required=True,
            help="Required Field"
        ),
        parser.add_argument(
            "email",
            type=str,
            required=True,
            help="Required Field"
        ),
        parser.add_argument(
            "password",
            type=str,
            required=True,
            help="Required Field"
        )

        data = parser.parse_args()
        user_model = UserModel(
            data["username"].lower(),
            data["email"],
            data["password"]
        )
        result = user_model.create_accout()

        return result

    # Login user
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "username",
            type=str,
            required=True,
            help="Required Field"
        ),
        parser.add_argument(
            "email",
            type=str,
            required=True,
            help="Required Field"
        ),
        parser.add_argument(
            "password",
            type=str,
            required=True,
            help="Required Field"
        )
        data = parser.parse_args()
        user_model = UserModel(
            data["username"].lower(),
            data["email"],
            data["password"]
        )
        result = user_model.login_user()

        if result == True:
            access_token = create_access_token(identity=user_model.username)
            refresh_token = create_refresh_token(identity=user_model.username)

            return {
                "message": "Success",
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        else:
            return {
                "message": "Unable to login user"
            }

    # delete user if needed
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "_id",
            type=str,
            required=True,
            help="Required Field"
        )

        data = parser.parse_args()
        result = UserModel.delete_account(data["_id"])
        return result

    @jwt_required
    # logout
    def put(self):
        # jti => JWT ID
        jwt = get_raw_jwt()["jti"]
        res = BlackList(jwt)
        result = res.add_to_blacklist()
        return {
            "message": "Removeed Access Token and {}".format(result),
        }

    @jwt_refresh_token_required
    def options(self):
        try:
            current_user = get_jwt_identity()
            print(current_user)
            print("CURRENT_USER")
            new_access_token = create_access_token(identity=current_user)
            return {
                "result": "Successfully deleted Refresh token",
                "access_token": new_access_token
            }
        except:
            return {
                "Result": "Unable to create new access token"
            }
