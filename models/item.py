#import sqlite3
from db import db

class ItemModel(db.Model):

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    #store.id is table.column
    #item is linked to store.id, which is by sequence, if create item
    #with non-exist store.id, store won't be created
    store = db.relationship("StoreModel")

    def __init__(self,name,price,store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"name":self.name,"price":self.price}

    @classmethod
    def find_by_name(cls,name): #find item by item name
        return cls.query.filter_by(name=name).first()
        # same as "SELECT * FROM items WHERE name=name SELECT 1"
        #automatic return ItemModel object

    def save_to_db(self): #both insert and update
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
