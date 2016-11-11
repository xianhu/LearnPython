# _*_ coding: utf-8 _*_

"""
python_decorator.py by xianhu
"""

import functools


# 构建不带参数的装饰器
def logging(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        print("%s called" % func.__name__)
        result = func(*args, **kwargs)
        print("%s end" % func.__name__)
        return result
    return decorator


# 使用装饰器
@logging
def test01(a, b):
    print("in function test01, a=%s, b=%s" % (a, b))
    return 1


# 使用装饰器
@logging
def test02(a, b, c=1):
    print("in function test02, a=%s, b=%s, c=%s" % (a, b, c))
    return 1


# 构建带参数的装饰器
def params_chack(*types, **kwtypes):
    def _outer(func):
        @functools.wraps(func)
        def _inner(*args, **kwargs):
            result = [isinstance(_param, _type) for _param, _type in zip(args, types)]
            assert all(result), "params_chack: invalid parameters"
            result = [isinstance(kwargs[_param], kwtypes[_param]) for _param in kwargs if _param in kwtypes]
            assert all(result), "params_chack: invalid parameters"
            return func(*args, **kwargs)
        return _inner
    return _outer


# 使用装饰器
@params_chack(int, (list, tuple))
def test03(a, b):
    print("in function test03, a=%s, b=%s" % (a, b))
    return 1


# 使用装饰器
@params_chack(int, str, c=(int, str))
def test04(a, b, c):
    print("in function test04, a=%s, b=%s, c=%s" % (a, b, c))
    return 1


# 在类的成员方法中使用装饰器
class ATest(object):
    @params_chack(object, int, str)
    def test(self, a, b):
        print("in function test of ATest, a=%s, b=%s" % (a, b))
        return 1


# 同时使用多个装饰器
@logging
@params_chack(int, str, (list, tuple))
def test05(a, b, c):
    print("in function test05, a=%s, b=%s, c=%s" % (a, b, c))
    return 1


# 构建不带参数的装饰器类
class Decorator(object):

    def __init__(self, func):
        self.func = func
        return

    def __call__(self, *args, **kwargs):
        print("%s called" % self.func.__name__)
        result = self.func(*args, **kwargs)
        print("%s end" % self.func.__name__)
        return result


# 使用装饰器
@Decorator
def test06(a, b, c):
    print("in function test06, a=%s, b=%s, c=%s" % (a, b, c))
    return 1


# 构建带参数的装饰器类
class ParamCheck(object):

    def __init__(self, *types, **kwtypes):
        self.types = types
        self.kwtypes = kwtypes
        return

    def __call__(self, func):
        @functools.wraps(func)
        def _inner(*args, **kwargs):
            result = [isinstance(_param, _type) for _param, _type in zip(args, self.types)]
            assert all(result), "params_chack: invalid parameters"
            result = [isinstance(kwargs[_param], self.kwtypes[_param]) for _param in kwargs if _param in self.kwtypes]
            assert all(result), "params_chack: invalid parameters"
            return func(*args, **kwargs)
        return _inner


# 使用装饰器
@ParamCheck(int, str, (list, tuple))
def test07(a, b, c):
    print("in function test06, a=%s, b=%s, c=%s" % (a, b, c))
    return 1


# 装饰器实例: 函数缓存
def funccache(func):
    cache = {}

    @functools.wraps(func)
    def _inner(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return _inner


# 使用装饰器
@funccache
def test08(a, b, c):
    # 其他复杂或耗时计算
    return a + b + c


# 使用Python自带的装饰器 @property
class Person(object):

    def __init__(self):
        self._name = None
        return

    def get_name(self):
        print("get_name")
        return self._name

    def set_name(self, name):
        print("set_name")
        self._name = name
        return

    name = property(fget=get_name, fset=set_name, doc="person name")


# 使用Python自带的装饰器 @property
class People(object):

    def __init__(self):
        self._name = None
        self._age = None
        return

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        return

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        assert 0 < age < 120
        self._age = age
        return


# 类静态方法和类方法
class A(object):
    var = 1

    def func(self):
        print(self.var)
        return

    @staticmethod
    def static_func():
        print(A.var)
        return

    @classmethod
    def class_func(cls):
        print(cls.var)
        cls().func()
        return
