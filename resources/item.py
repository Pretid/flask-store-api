from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class ItemList(Resource):
    def get(self):
        
        return {'items':[item.json() for item in ItemModel.query.all()]}
        #or list(map(lambda x:x.json(), ItemModel.query.all()))


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be blank")
    
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="This field cannot be blank")


    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':"item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message':'An item with name {} already exists'.format(name)}, 400
        
        #data = request.get_json()
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'],data['store_id'])
        try:
            item.save_to_db()
        except:
            return {'message':'An error occured while inserting'}, 500
        
        return item.json(), 201

    
    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        else:
            return {'message':'nothing to delete'}
        return {'message':'Item deleted'}

    def put(self, name):
        
        #data = request.get_json()
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()

    
