# _*_ coding: utf-8 _*_

"""
python_restful_api.py by xianhu
"""

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

ITEMS = {
    'item1': {'name': 'Allen', 'age': 19},
    'item2': {'name': 'Lily', 'age': 18},
    'item3': {'name': 'James', 'age': 20},
}


def abort_if_item_doesnt_exist(item_id):
    if item_id not in ITEMS:
        abort(404, message="Item {} doesn't exist".format(item_id))


def get_new_item_id():
    for key in ITEMS:
        item_id = 'item' + str(int(key.strip('item')) + 1)
        if item_id not in ITEMS:
            return item_id


parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='need name data')
parser.add_argument('age', type=int, required=True, help='need age data')


# 操作（put / get / delete）单一资源
class Todo(Resource):

    def put(self, item_id):
        args = parser.parse_args()
        item = {'name': args['name'], 'age': args['age']}
        ITEMS[item_id] = item
        return item, 201

    def get(self, item_id):
        abort_if_item_doesnt_exist(item_id)
        return ITEMS[item_id], 200

    def delete(self, item_id):
        abort_if_item_doesnt_exist(item_id)
        del ITEMS[item_id]
        return '', 204


# 操作（post / get）资源列表
class TodoList(Resource):

    def get(self):
        return ITEMS, 200

    def post(self):
        args = parser.parse_args()
        item_id = get_new_item_id()
        ITEMS[item_id] = {'name': args['name'], 'age': args['age']}
        return ITEMS[item_id], 201


# 设置路由
api.add_resource(TodoList, '/items')
api.add_resource(Todo, '/items/<item_id>')


if __name__ == '__main__':
    app.run(debug=True)
