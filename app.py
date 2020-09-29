from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate,identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
#from db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key="this should be a long secret_key"
api = Api(app)

@app.before_first_request #flask decorator, it will affect the method below it.
#it will run the method before 1st request into this app
def create_tables():
    db.create_all() #it looks into "import" to find what table to created
    #for example, it will look into Store in resource and find Store in models
    #then it will get table info

jwt = JWT(app,authenticate,identity) #jwt create a new endpoint /auth
#when call /auth, we send username and password, authenticate will take them
#if match, /auth returns a jwt token, jwt calls identity, uses token to get user_id and retrive user obj


api.add_resource(Store,"/store/<string:name>")
api.add_resource(StoreList,"/stores")
api.add_resource(Item,"/item/<string:name>") #this resource can be accessed via api
api.add_resource(ItemList,"/items")
api.add_resource(UserRegister,"/register") #add a new endpoint

from db import db
db.init_app(app)
if __name__ == "__main__":
#if we import app.py in other profile, all statement will execute
#to prevent this, add if statement here
    #from db import db
    #db.init_app(app)
    app.run(port=5000,debug=True)
