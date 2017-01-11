# _*_ coding: utf-8 _*_

"""
python_restful_api.py by xianhu
"""

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative
from flask import Flask, g
from flask_restful import reqparse, Api, Resource
from flask_httpauth import HTTPTokenAuth


# Flask相关变量声明
app = Flask(__name__)
api = Api(app)

# 认证相关
auth = HTTPTokenAuth(scheme="token")
TOKENS = {
    "fejiasdfhu",
    "fejiuufjeh"
}


@auth.verify_token
def verify_token(token):
    if token in TOKENS:
        g.current_user = token
        return True
    return False


# 数据库相关变量声明
engine = sqlalchemy.create_engine("mysql+pymysql://username:password@ip/db_name", encoding="utf8", echo=False)
BaseModel = sqlalchemy.ext.declarative.declarative_base()


# 构建数据模型User
class User(BaseModel):
    __tablename__ = "Users"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8",
    }

    # 表结构,具体更多的数据类型自行百度
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column("name", sqlalchemy.String(50), nullable=False)
    age = sqlalchemy.Column("age", sqlalchemy.Integer, nullable=False)


# 构建数据模型的json格式
def get_json(user):
    return {"id": user.id, "name": user.name, "age": user.age}


# 利用Session对象连接数据库
DBSessinon = sqlalchemy.orm.sessionmaker(bind=engine)
session = DBSessinon()
BaseModel.metadata.drop_all(engine)
BaseModel.metadata.create_all(engine)

# RESTfulAPI的参数解析 -- put / post参数解析
parser_put = reqparse.RequestParser()
parser_put.add_argument("name", type=str, required=True, help="need name data")
parser_put.add_argument("age", type=int, required=True, help="need age data")

# RESTfulAPI的参数解析 -- get参数解析
parser_get = reqparse.RequestParser()
parser_get.add_argument("limit", type=int, required=False)
parser_get.add_argument("offset", type=int, required=False)
parser_get.add_argument("sortby", type=str, required=False)


# 操作（put / get / delete）单一资源
class Todo(Resource):
    # 添加认证
    decorators = [auth.login_required]

    def put(self, user_id):
        """
        更新用户数据: curl http://127.0.0.1:5000/users/1 -X PUT -d "name=Allen&age=20" -H "Authorization: token fejiasdfhu"
        """
        args = parser_put.parse_args()
        user_ids_set = set([user.id for user in session.query(User.id)])
        print(user_ids_set)

        # 用户不存在，返回404
        if user_id not in user_ids_set:
            return None, 404

        # 更新用户数据
        user = session.query(User).filter(User.id == user_id)[0]
        user.name = args["name"]
        user.age = args["age"]
        session.merge(user)
        session.commit()

        # 更新成功，返回201
        return get_json(user), 201

    def get(self, user_id):
        """
        获取用户数据: curl http://127.0.0.1:5000/users/1 -X GET -H "Authorization: token fejiasdfhu"
        """
        users = session.query(User).filter(User.id == user_id)

        # 用户不存在，返回404
        if users.count() == 0:
            return None, 404

        # 返回用户数据
        return get_json(users[0]), 200

    def delete(self, user_id):
        """
        删除用户数据: curl http://127.0.0.1:5000/users/1 -X DELETE -H "Authorization: token fejiasdfhu"
        """
        session.query(User).filter(User.id == user_id).delete()
        return None, 204


# 操作（post / get）资源列表
class TodoList(Resource):
    # 添加认证
    decorators = [auth.login_required]

    def get(self):
        """
        获取全部用户数据: curl http://127.0.0.1:5000/users -X GET -d "limit=2&offset=0&sortby=name" -H "Authorization: token fejiasdfhu"
        """
        args = parser_get.parse_args()
        users = session.query(User)

        # 根据条件查询
        if "sortby" in args:
            users = users.order_by(User.name if args["sortby"] == "name" else User.age)
        if "offset" in args:
            users = users.offset(args["offset"])
        if "limit" in args:
            users = users.limit(args["limit"])

        # 返回结果
        return [get_json(user) for user in users], 200

    def post(self):
        """
        添加一个新用户: curl http://127.0.0.1:5000/users -X POST -d "name=Brown&age=20" -H "Authorization: token fejiasdfhu"
        """
        args = parser_put.parse_args()

        # 构建新用户
        user = User(name=args["name"], age=args["age"])
        session.add(user)
        session.commit()

        # 资源添加成功，返回201
        return get_json(user), 201


# 设置路由
api.add_resource(TodoList, "/users")
api.add_resource(Todo, "/users/<int:user_id>")


if __name__ == "__main__":
    app.run(debug=True)


""" 常见返回代码
200 OK - [GET]：服务器成功返回用户请求的数据
201 CREATED - [POST/PUT/PATCH]：用户新建或修改数据成功
202 Accepted - [*]：表示一个请求已经进入后台排队（异步任务）
204 NO CONTENT - [DELETE]：用户删除数据成功
400 INVALID REQUEST - [POST/PUT/PATCH]：用户发出的请求有错误，服务器没有进行新建或修改数据的操作
401 Unauthorized - [*]：表示用户没有权限（令牌、用户名、密码错误）
403 Forbidden - [*] 表示用户得到授权（与401错误相对），但是访问是被禁止的
404 NOT FOUND - [*]：用户发出的请求针对的是不存在的记录，服务器没有进行操作
406 Not Acceptable - [GET]：用户请求的格式不可得
410 Gone -[GET]：用户请求的资源被永久删除，且不会再得到的
422 Unprocesable entity - [POST/PUT/PATCH] 当创建一个对象时，发生一个验证错误
500 INTERNAL SERVER ERROR - [*]：服务器发生错误，用户将无法判断发出的请求是否成功
"""
