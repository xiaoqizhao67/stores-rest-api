#import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource): #every Resource is a class
    #Resource will create a mapping about path
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price",
        type = float,
        required = True,
        help = "this field cannot be blank"
    )
    parser.add_argument(
        "store_id",
        type = int,
        required = True,
        help = "Every item needs a store id" #help shows up when this argument is empty
    )

    @jwt_required()
    def get(self,name): #get item from "items" db
        #if this function is decorated by @jwt_required().
        #1st need to /auth with username and password, then choose Authorization
        #JWT token
        #item = next(filter(lambda x: x["name"]==name,items),None) #filter function return a filter
        #next will return the 1st item, "None" will give next a default value, in case error
        #return {"item":item},200 if item else 404 #return a json format dict
        #no need to jsonify when using flash_restful
        item = ItemModel.find_by_name(name) #call classmethod by "self"
        #can also use Item.find_by_name(name)
        if item:
            return item.json()
        return ({"message":"item not found"},404)


    def post(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return {"message":"item with name {} already exists".format(name)},400 #400 is bad request
        data = Item.parser.parse_args() #use this method instead of get_json
        #this will parse json and get "price" related data
        item=ItemModel(name, **data) #item is a new ItemModel object
        #**data same as data["price"],data["store_id"]
        try:
            item.save_to_db()
        except:
            return ({"message":"error occurred when inserting item"},500)
            #500 is internal server error, request is fine, but the server has issue
            #400 is when something with the request

        return item.json(),201 #201 is created

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if not item:
            return {"message":"item not found"}
        item.delete_from_db()

        return {"messsage" : "item deleted"}

    def put(self,name): #put can create or update
        #data = request.get_json()
        data = Item.parser.parse_args() #use this method instead of get_json
        #this will parse json and get "price" related data
        #item = next(filter(lambda x : x["name"] == name, items), None)
        item = ItemModel.find_by_name(name)
        if not item:
            try:
                item = ItemModel(name,**data)
            except:
                return {"message":"error occurred inserting item"},500
        else:
            try:
                item.price=data["price"]
            except:
                return {"message":"error occurred updating item"},500
        item.save_to_db()
        return item.json()



class ItemList(Resource):
    def get(self):
        return {"items" : [item.json() for item in ItemModel.query.all()]}
        #list comprehension [expression for iter_val in iterable if cond_expr]
        #.all return all objects in database
        #can also use:
        #return {"items":list(map(lambda x: x.json(),ItemModel.query.all()))}
        #map(fun, iter)
        #fun : It is a function to which map passes each element of given iterable.
        #iter : It is a iterable which is to be mapped.
        #Returns a list of the results after applying the given function
        #to each item of a given iterable (list, tuple etc.)
