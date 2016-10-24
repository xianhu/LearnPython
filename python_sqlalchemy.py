# _*_ coding: utf-8 _*_

"""
python_sqlalchemy.py by xianhu
"""

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative

# 利用数据库字符串构造engine, echo为True将打印所有的sql语句
engine = sqlalchemy.create_engine("mysql+pymysql://username:password@hostname/dbname", encoding="utf8", echo=True)

# tset
"""
# 利用engine创建connection,这里不需要close操作
with engine.connect() as conn:
    # 最基础的用法
    result = conn.execute("select * from tablename limit 10;")
    for item in result:
        print(item)

    # execute的几种用法,这里具体还是得参考pymysql的用法,这里不需要执行commit操作
    conn.execute("insert into tablename(id, url, title) values(1, "url1", "title1");")
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
"""

# 利用ORM特性生成模型
Base = sqlalchemy.ext.declarative.declarative_base()


# 构建模型User
class User(Base):
    __tablename__ = "User"
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column("name", sqlalchemy.String(50), default="", unique=True)
    age = sqlalchemy.Column("age", sqlalchemy.Integer, nullable=False)

# 利用Session对象连接数据库
DBSessinon = sqlalchemy.orm.sessionmaker(bind=engine)   # 创建会话类
session = DBSessinon()                                  # 创建会话对象

# 创建表（如果表已经存在，则不会创建）
Base.metadata.create_all(engine)

try:
    # 清空数据,不需要commit操作
    session.query(User).filter(User.id != -1).delete()

    # 插入数据,这里的一个user只插入一次,第二次插入不生效
    user = User(name="tobi", age=20)
    session.add(user)
    session.commit()

    # 修改数据
    user.name = "allen"
    session.merge(user)                         # 使用merge方法,如果存在则修改,如果不存在则插入
    session.query(User).filter(User.id == user.id).update({"name": "carol"})    # 使用update方法

    # 查询数据
    users = session.query(User)                 # 返回全部结果
    for user in users:
        print(user.id, user.name, user.age)
    user = session.query(User).get(2)           # 返回结果集的第二项
    users = session.query(User)[1:3]            # 返回结果集中的第2-3项

    # 其他高级查询
    user = session.query(User).filter(User.id < 6).first()              # 条件查询
    users = session.query(User).order_by(User.name)                     # 排序查询
    users = session.query(User).order_by(sqlalchemy.desc(User.name))    # 排序查询之倒序
    users = session.query(User.id, User.name)                           # 只查询部分属性
    users = session.query(User.name.label("user_name")).all()           # 给结果集的列取别名
    for user in users: print(user.user_name)                            # 这里使用别名
    users = session.query(sqlalchemy.distinct(User.name)).all()         # 去重查询
    user_count = session.query(User.name).count()                       # 统计全部数量
    age_avg = session.query(sqlalchemy.func.avg(User.age)).first()      # 求平均值
    age_sum = session.query(sqlalchemy.func.sum(User.age)).first()      # 求和运算
    users = session.query(sqlalchemy.func.count(User.name).label("count"), User.age).group_by(User.age)    # 分组查询
    for user in users:
        print("age:{0}, count:{1}".format(user.age, user.count))

except Exception as excep:
    session.rollback()
    raise
