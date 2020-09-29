import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser() #parse json data
    parser.add_argument(
        "username",
        type = str, #str means string
        required = True,
        help = "this field cannot be blank"
    )
    parser.add_argument(
        "password",
        type = str,
        required = True,
        help = "this field cannot be blank"
    )
    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data["username"]): #make sure this is before data db connection
        #else it will return and connection never close
            return ({"message":"user with this username exists"},400)

        user = UserModel(**data) #data["username"],data["password"] is same
        user.save_to_db()


        return ({"message": "User created successfully"},201)
