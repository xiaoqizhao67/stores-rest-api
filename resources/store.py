from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):

    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message" : "store not found"},404

    def post(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return {"message" : "store with name {} already exist".format(name)}, 400
        try:
            store=StoreModel(name)
            store.save_to_db()
        except:
            return {"message" : "error ocurred when creating store"},500
        return store.json(),201

    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if not store:
            return {"message" : "store not found"}
        store.delete_from_db()
        return {"message" : "store deleted"}


class StoreList(Resource):
    def get(self):
        return {"stores":[store.json() for store in StoreModel.query.all()]}
