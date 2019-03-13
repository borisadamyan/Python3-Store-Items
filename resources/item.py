from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='On add product field cannot be left blank!')
    parser.add_argument('store_id',
                        type=float,
                        required=True,
                        help='Every item need store id')

    @jwt_required()
    def get(self, name):
        # item = next(filter(lambda a: a['name'] == name, items), None)
        # return {'item': item}, 200 if item else 404
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        # if next(filter(lambda a: a['name'] == name, items), None) is not None:
        #  return {'message': 'An item with name {} already exist'.format(name)}
        if ItemModel.find_by_name(name):
            return {'message': 'An item with name {} already exist'.format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)
        # items.append(item)

        try:
            item.save_to_db()
        except:
            return {"message": "An error inserting the item"}, 500
        return item.json(), 201

    # @jwt_required()

    def delete(self, name):
        # global items
        # items = list(filter(lambda x: x['name'] != name, items))

        # item = {'name': name}
        # items.append(item)

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "DELETE FROM items WHERE name=?"
        #
        # cursor.execute(query, (name,))
        # connection.commit()
        # connection.close()
        #
        # return {'message': 'Item deleted'}

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db(name)
        return {'message': 'Item deleted'}

    def put(self, name):

        data = Item.parser.parse_args()

        # item = next(filter(lambda a: a['name'] == name, items), None)

        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])
        if item is None:
            # try:
            #     updated_item.instert()
            # except:
            #     return {"message": "An error occurred inserting item."}, 500
            item = ItemModel(name, **data)
        else:
            # try:
            #     updated_item.update()
            # except:
            #     return {"message": "An error occurred updating item."}, 500
            item.price = data['price']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items"

        # result = cursor.execute(query)
        # items = []
        # for row in result:
        #     items.append({"name": row[0], "price": row[1]})
        #
        # connection.close()
        # return {'items': items}

        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
        return {'items': item.json() for item in ItemModel.query.all()}
