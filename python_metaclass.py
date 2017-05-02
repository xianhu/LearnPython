# _*_ coding: utf-8 _*_

"""
python_metaclass.py by xianhu
"""


class Foo(object):
    def hello(self):
        print("hello world!")
        return

foo = Foo()
print(type(foo))            # <class '__main__.Foo'>
print(type(foo.hello))      # <class 'method'>
print(type(Foo))            # <class 'type'>

temp = Foo                  # 赋值给其他变量
Foo.var = 11                # 增加参数
print(Foo)                  # 作为函数参数


# ========================================================================
def init(self, name):
    self.name = name
    return


def hello(self):
    print("hello %s" % self.name)
    return

Foo = type("Foo", (object,), {"__init__": init, "hello": hello, "cls_var": 10})
foo = Foo("xianhu")
print(foo.hello())
print(Foo.cls_var)

print(foo.__class__)
print(Foo.__class__)
print(type.__class__)
# ========================================================================


class Author(type):
    def __new__(mcs, name, bases, dict):
        # 添加作者属性
        dict["author"] = "xianhu"
        return super(Author, mcs).__new__(mcs, name, bases, dict)


class Foo(object, metaclass=Author):
    pass

foo = Foo()
print(foo.author)
