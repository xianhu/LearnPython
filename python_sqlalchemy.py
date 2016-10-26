# _*_ coding: utf-8 _*_

"""
python_sqlalchemy.py by xianhu
"""

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative

# 利用数据库字符串构造engine, echo为True将打印所有的sql语句, 其他数据库的链接方式可自行百度
# engine = sqlalchemy.create_engine("mysql+pymysql://username:password@hostname/dbname", encoding="utf8", echo=True)
engine = sqlalchemy.create_engine("mysql+pymysql://dba_0:mimadba_0@101.200.174.172/data_secret", encoding="utf8", echo=False)

"""
# 利用engine创建connection,因为使用了with所以不需要close操作,这部分不是重点
with engine.connect() as conn:
    # 最基础的用法
    result = conn.execute("select * from tablename limit 10;")
    for item in result:
        print(item)

    # execute的几种用法,这里具体还是得参考pymysql的用法,不需要执行commit操作
    conn.execute("insert into tablename(id, url, title) values(1, 'url1', 'title1');")
    conn.execute("insert into tablename(id, url, title) values(%s, %s, %s);", 2, "url2", "title2")
    conn.execute("insert into tablename(id, url, title) values(%s, %s, %s)", (3, "url3", "title3"))
    conn.execute("insert into tablename(id, url, title) values(%s, %s, %s)", [(31, "url31", "title31"), (32, "url32", "title32")])

    # 使用事务可以进行批量提交和回滚
    trans = conn.begin()
    try:
        conn.execute("insert into tablename(id, url, title) values(%s, %s, %s)", [(4, "url4", "title4"), (5, "url5", "title5")])
        trans.commit()
    except Exception as excep:
        trans.rollback()
        raise
    trans.close()
"""

# 首先需要生成一个BaseModel类,作为所有模型类的基类
BaseModel = sqlalchemy.ext.declarative.declarative_base()


# 构建数据模型User
class User(BaseModel):
    __tablename__ = "Users"         # 表名
    __table_args__ = {
        "mysql_engine": "InnoDB",   # 表的引擎
        "mysql_charset": "utf8",    # 表的编码格式
    }

    # 表结构,具体更多的数据类型自行百度
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column("name", sqlalchemy.String(50), nullable=False)
    age = sqlalchemy.Column("age", sqlalchemy.Integer, default=0)

    # 添加角色id外键,关联到表Roles的id属性
    role_id = sqlalchemy.Column("role_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("Roles.id"))

    # 添加关系属性,关联到本实例的role_id外键属性上
    role = sqlalchemy.orm.relationship("Role", foreign_keys="User.role_id")

    # 添加关系属性,关联到本实例的role_id外键属性上,如果使用了这种方式,Role模型中的users可以省略
    # role = sqlalchemy.orm.relationship("Role", foreign_keys="User.role_id", backref=sqlalchemy.orm.backref("users"))


# 构建数据模型Role
class Role(BaseModel):
    __tablename__ = "Roles"         # 表名
    __table_args__ = {
        "mysql_engine": "InnoDB",   # 表的引擎
        "mysql_charset": "utf8",    # 表的编码格式
    }

    # 表结构,具体更多的数据类型自行百度
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column("name", sqlalchemy.String(50), unique=True)

    # 添加关系属性,关联到实例User的role_id外键属性上
    users = sqlalchemy.orm.relationship("User", foreign_keys="User.role_id")


# 利用Session对象连接数据库
DBSessinon = sqlalchemy.orm.sessionmaker(bind=engine)   # 创建会话类
session = DBSessinon()                                  # 创建会话对象


# 删除所有表
BaseModel.metadata.drop_all(engine)
# 创建所有表,如果表已经存在,则不会创建
BaseModel.metadata.create_all(engine)

try:
    # 清空数据,不需要commit操作
    session.query(User).filter(User.id != -1).delete()
    session.query(Role).filter(Role.id != -1).delete()
    # 删除数据的另外一种形式:session.delete()

    # 插入数据,这里的一个实例只插入一次,第二次插入不生效
    session.add(Role(id=1, name="student"))
    session.add(Role(id=2, name="teacher"))
    session.commit()

    session.add(User(name="James", age=20, role_id=1))
    session.add(User(name="Wade", age=40, role_id=2))
    session.commit()

    user = User(name="Kobe", age=24, role_id=1)
    session.add(user)
    session.commit()

    # 修改数据
    user.name = "Allen"
    session.merge(user)                         # 使用merge方法,如果存在则修改,如果不存在则插入
    session.query(User).filter(User.id == user.id).update({User.name: "Allen"})         # 使用update方法
    session.query(User).filter(User.id == user.id).update({User.age: User.age + 1})     # 使用update方法,自增操作

    # 查询数据
    roles = session.query(Role)                 # 返回全部结果
    for role in roles:
        print("Role:", role.id, role.name)

    users = session.query(User)                 # 返回全部结果
    for user in users:
        print("User:", user.id, user.name, user.age, user.role_id)

    # 其他获取数据的方式
    print("get(id):", session.query(User).get(1))                       # 返回结果集中id为1的项
    print("get[1:3]:", session.query(User)[1:3])                        # 返回结果集中的第2-3项

    # 其他高级查询,这里以Users表为例
    users = session.query(User).filter(User.id > 6)                     # 条件查询
    users = session.query(User).filter(User.id > 6).all()               # 条件查询,返回查询的全部数据
    user = session.query(User).filter(User.id > 6).first()              # 条件查询,返回查询数据的第一项
    users = session.query(User).filter(User.id > 6).limit(10)           # 条件查询,返回最多10条数据
    users = session.query(User).filter(User.id > 6).offset(2)           # 条件查询,从第3条数据开始返回

    users = session.query(User).filter(User.id > 6, User.name == "Kobe")                    # 条件查询,and操作
    users = session.query(User).filter(User.id > 6).filter(User.name == "Kobe")             # 条件查询,and操作
    users = session.query(User).filter(sqlalchemy.or_(User.id > 6, User.name == "Kobe"))    # 条件查询,or操作
    users = session.query(User).filter(User.id.in_((1, 2)))                                 # 条件查询,in操作
    users = session.query(User).filter(sqlalchemy.not_(User.name))                          # 条件查询,not操作

    user_count = session.query(User.id).count()                                             # 统计全部user的数量
    user_count = session.query(sqlalchemy.func.count(User.id)).scalar()                     # scalar操作返回第一行数据的第一个字段
    session.query(sqlalchemy.func.count("*")).select_from(User).scalar()                    # scalar操作返回第一行数据的第一个字段
    session.query(sqlalchemy.func.count(1)).select_from(User).scalar()                      # scalar操作返回第一行数据的第一个字段
    session.query(sqlalchemy.func.count(User.id)).filter(User.id > 0).scalar()              # filter() 中包含 User，因此不需要指定表

    session.query(sqlalchemy.func.sum(User.age)).scalar()                                   # 求和运算,运用scalar函数
    session.query(sqlalchemy.func.avg(User.age)).scalar()                                   # 求均值运算,运用scalar函数
    session.query(sqlalchemy.func.md5(User.name)).filter(User.id == 1).scalar()             # 运用md5函数

    users = session.query(sqlalchemy.distinct(User.name))               # 去重查询,根据name进行去重
    users = session.query(User).order_by(User.name)                     # 排序查询,正序查询
    users = session.query(User).order_by(User.name.desc())              # 排序查询,倒序查询
    users = session.query(User).order_by(sqlalchemy.desc(User.name))    # 排序查询,倒序查询的另外一种形式

    users = session.query(User.id, User.name)                           # 只查询部分属性
    users = session.query(User.name.label("user_name"))                 # 结果集的列取别名
    for user in users:
        print("label test:", user.user_name)                            # 这里使用别名

    users = session.query(sqlalchemy.func.count(User.name).label("count"), User.age).group_by(User.age)    # 分组查询
    for user in users:
        print("age:{0}, count:{1}".format(user.age, user.count))

    # 多表查询
    result = session.query(User, Role).filter(User.role_id == Role.id)
    for user, role in result:
        print("user %s's role is %s" % (user.name, role.name))
    users = session.query(User).join(Role, User.role_id == Role.id)
    for user in users:
        print("user join, name:", user.name)

    # 关联属性的用法
    roles = session.query(Role)
    for role in roles:
        print("role:%s users:" % role.name)
        for user in role.users:
            print("\t%s" % user.name)
    users = session.query(User)
    for user in users:
        print("user %s's role is %s" % (user.name, user.role.name))

except Exception as excep:
    session.rollback()
    raise

session.close()
