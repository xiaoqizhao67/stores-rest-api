
from models.user import UserModel

def authenticate(username,password):
    user = UserModel.find_by_username(username)#here use get instead of []
    #get will have benefit of default value "None"
    if user and user.password == password:
        return user

def identity(payload): #payload is the content of jwt token
    user_id=payload["identity"]
    return UserModel.find_by_id(user_id) #retrive user by id
