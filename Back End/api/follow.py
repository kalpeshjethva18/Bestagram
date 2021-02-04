from flask_restful import Resource, reqparse
from user import *


class Follow(Resource):
    """
    Follow a user.
    """

    def post(self):
        """
        Query parameters :
            - id : If of the user

        Headers :
            - Authorization : Token of the current user.
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        parser.add_argument("Authorization", location="headers")
        params = parser.parse_args()

        if not (params["id"] and params["Authorization"]):
            return MissingInformation.get_response()

        try:
            user = User(token=params["Authorization"])
        except BestagramException as e:
            return e.get_response()

        try:
            user.follow(int(params["id"]))
        except BestagramException as e:
            return e.get_response()
        return {"success": True}, 200
