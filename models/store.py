#import sqlite3
from db import db

class StoreModel(db.Model):

    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship("ItemModel", lazy="dynamic") #a list of ItemModel

    def __init__(self,name):
        self.name = name

    def json(self):
        return {"name":self.name,"items":[item.json() for item in self.items.all()]}
        #use "self.items", need self here
        #when using lazy="dynamic", self.items is no longer a list, it's a query builder
        #need use ".all" to get items inside self.items

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
